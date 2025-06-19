import elcsoft.controller.cmd
import elcsoft.controller.cmd.doorsystem
import threading
import lib
import logger
import mqtt_subscribe
import screen
import pir_inside
import pir_outside
import elcsoft.model.user
import elcsoft.model.smartdoor_guestkey
import elcsoft.controller.user
import elcsoft.controller.smartdoor
import elcsoft.controller.smartdoor_cmd
import elcsoft.controller.pir.inside
import elcsoft.controller.pir.outside
import elcsoft.controller.cmd.doorcloser
import elcsoft.controller.ws.weather
import elcsoft.controller.sound
import elcsoft.controller.smartdoor_guestkey
import elcsoft.controller.msg.smartdoor_cmd
import msgbox
import hione
import time
import network
import button
import RPi.GPIO as GPIO  # 버튼 핀 상태 직접 확인용


class WikiSmartdoor:
    smartdoorObj = None
    websocket = None
    doorStatus = 0  # 0:닫힘 1:여는중 2:열림 3: 닫는중
    doorlockStatus = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            logger.Logger.create_logger()
            logger.Logger._LOGGER.info("WikiSmartdoor __new__ is called\n")
            cls._instance = super().__new__(cls)
            cls.websocket = None
            cls.doorStatus = 0
            cls.doorlockStatus = False
            cls.exitThread = False
            cls.isPlayingDoorbell = False

        return cls._instance

    def __init__(self, *args, **kwargs):
        logger.Logger._LOGGER.info("WikiSmartdoor __init__ is called\n")
        self.config = lib.getConfigByJsonFile("/home/pi/www/python/config.json")

        # 네트워크 연결이 안되면 웹소켓으로 네트워크 연결 요청
        if not network.isInternet():
            msg = {"request": "setupWifi", "data": network.getWifies()}
            self.sendWebsocket(msg)
        else:
            # 스마트도어 정보
            self.smartdoorObj = elcsoft.controller.smartdoor.getSmartdoorObj()

            # MQTT
            self.mqtt = mqtt_subscribe.MqttSubscribe(**self.config["mqtt"])
            self.mqtt.wikismartdoor = self

            try:
                self.subscribe()
            except Exception as e:
                logger.Logger._LOGGER.info(f"토픽정보가 없습니다. : {e}")

            # 모니터
            self.screen = screen.Screen()
            self.screen.wikismartdoor = self

            # 내측 스피커
            self.insideSpeaker = None
            elcsoft.controller.sound.initInsideSpeaker(
                self, self.config["insideSpeakerDevice"]["player"]
            )
            # self.insideSpeaker.load_sound_cache(**self.config['doorbell'])

            # 외측 스피커
            self.outsideSpeaker = None
            elcsoft.controller.sound.initOutsideSpeaker(
                self, self.config["outsideSpeakerDevice"]["player"]
            )

            # 내측 PIR
            self.config["pir_inside"]["moved_callback"] = self.pir_inside_moved
            self.config["pir_inside"]["finished_callback"] = self.pir_inside_finished
            self.pir_inside = pir_inside.PirInside(**self.config["pir_inside"])

            # 외측 PIR
            self.config["pir_outside"]["pushed_callback"] = self.pir_outside_pushed
            self.config["pir_outside"]["moved_callback"] = self.pir_outside_moved
            self.config["pir_outside"]["finished_callback"] = self.pir_outside_finished
            self.config["pir_outside"]["wikismartdoor"] = self
            self.pir_outside = pir_outside.PirOutside(**self.config["pir_outside"])

            # 도어락
            self.doorlock = hione.Hione(port=self.config["doorlock"])

            # 도어시스템
            # self.doorsystem = doorsystem.DoorSystem(device=self.config['doorlock'], dooropened_callback=self.doorOpend, doorclosed_callback=self.doorClosed)

    # 백그라운드로 계속 실행할 것들
    def run(self):
        # 네트워크 연결이 안되면 웹소켓으로 네트워크 연결 요청
        if not network.isInternet():
            msg = {"request": "setupWifi", "data": network.getWifies()}
            self.sendWebsocket(msg)
        else:
            self.syncDataAll()
        # threading.Thread(target=self.syncDataAll, daemon=True).start()
        threading.Thread(target=self.mqtt.run, daemon=True).start()
        threading.Thread(target=self.polling, daemon=True).start()
        threading.Thread(target=self.pir_inside.run, daemon=True).start()
        threading.Thread(target=self.pir_outside.run, daemon=True).start()

        # 버튼 초기화
        self.initialize_button()

    def setStatus(self, results):
        lib.log(f"Status changed: {results}")

        # 도어락 열림, 문 열림
        if results["isDoorlock"] and results["isDooropen"]:
            self.doorStatus = 2
            self.doorlockStatus = True
        # 도어락 열림, 문 잠김 - 문여는중
        elif results["isDoorlock"] and not results["isDooropen"]:
            self.doorStatus = 1
            self.doorlockStatus = True
        # 도어락 잠김, 문 열림 - 발생할 수 없는 상황
        elif not results["isDoorlock"] and not results["isDooropen"]:
            self.doorStatus = 0
            self.doorlockStatus = False

    def polling(self):
        lib.log("Doorlock polling started")

        self.setStatus(self.doorlock.isDoorOpen())

        while not self.exitThread:
            try:
                # 실제 도어 상태 조회
                door_open = self.doorlock.isDoorOpen()

                # 문열기 상태로 변경된경우
                if door_open["isDoorlock"] and self.doorStatus == 0:
                    lib.log("Door is now OPEN.")
                    open = threading.Thread(target=self.doorOpend)
                    open.start()
                    open.join()
                # 문닫기 상태로 변경된 경우
                elif not door_open["isDoorlock"] and self.doorStatus == 2:
                    self.doorStatus = 0  # 닫힘 상태
                    lib.log("Door is now CLOSED.")
                    close = threading.Thread(target=self.doorClosed)
                    close.start()
                    close.join()

                self.setStatus(door_open)
                # 상태 로그 출력
                lib.log(f"Current door status: {'OPEN' if door_open else 'CLOSED'}")
            except Exception as e:
                lib.log(f"Error checking door status : ")
                lib.log(e)

            time.sleep(1)  # 비동기적으로 대기

        lib.log("Doorlock Polling Thread Exit!")

    ################################################################################################################################
    #####
    #####   메세지 전송관련
    #####
    ################################################################################################################################
    def sendWebsocket(self, message):
        isWebsocket = False

        lib.log(
            "--------------------------------- send websocket --------------------------------"
        )
        lib.log(f"websocket : {self.websocket}")
        lib.log(f"message : {message}")
        lib.log(f"type of message : {type(message)}")

        try:
            if isinstance(message, (dict, list)):
                message = lib.jsonencode(message)
        except Exception as e:
            logger.Logger._LOGGER.exception(
                f"message converting error: {message} {type(message)} {e}"
            )

        try:
            self.websocket.write_message(message)
            lib.log(f"직접 메세지 발송 성공")
        except Exception as e:
            lib.log(f"메세지발송 실패 메세지박스 재전송")
            msgbox.sendMsg(cmd="websocket", msg=message)

        lib.log(
            "--------------------------------- send websocket --------------------------------"
        )

    def sendKiosk(self, message, json=None):
        data = {"request": "sendKiosk", "response": message}
        if json is not None:
            data["data"] = json

        self.sendWebsocket(data)

    def sendKioskAlert(self, message):
        data = {
            "request": "sendKiosk",
            "response": "alert",
            "result": False,
            "message": message,
        }
        self.sendWebsocket(data)

    def sendMqtt(self, topic, message):
        lib.log(
            "--------------------------------- send mqtt --------------------------------"
        )
        lib.log(f"message : {message}")
        lib.log(f"type of message : {type(message)}")

        try:
            if isinstance(message, (dict, list)):
                message = lib.jsonencode(message)
        except Exception as e:
            lib.log(f"message converting error: {message} {type(message)} {e}")

        try:
            self.mqtt.publish(topic, message)
        except Exception as e:
            msgbox.sendMsg("mqtt", topic, message)
        lib.log(
            "--------------------------------- send mqtt --------------------------------"
        )

    def sendMqttTrue(self, topic, json=None):
        data = {"result": True}
        if json is not None:
            data["data"] = json
        self.sendMqtt(topic, data)

    def sendMqttFalse(self, topic, message):
        msg = {"result": False, "message": message}
        self.sendMqtt(topic, msg)

    def sendMqttAll(self, message):
        users = elcsoft.controller.user.getUsers()
        for user in users["lists"]:
            # print(user)
            topic = elcsoft.controller.smartdoor.getUserTopic(user["user_id"])
            # print(topic)
            self.sendMqtt(topic, message)

    def subscribe(self):
        topic = elcsoft.controller.smartdoor.getDoorTopic()
        self.mqtt.subscribe(topic=topic)

    ################################################################################################################################
    #####
    #####   문열기 관련
    #####
    ################################################################################################################################

    # 도어락상태조회
    def isDoorlock(self):
        if self.doorlock is None:
            raise Exception("도어락이 연결되지 않았습니다.")

        # 락이 잠금해제된 경우, 문이 열릴수도 있고 닫혀 있을 수 있음
        self.setStatus(self.doorlock.isDoorOpen())

        return self.doorlockStatus

    # 문상태조회
    def isDoorOpen(self):
        if self.doorStatus == 0:
            return False
        elif self.doorStatus == 1:
            return False
        elif self.doorStatus == 2:
            return True
        elif self.doorStatus == 3:
            return True
        else:
            raise Exception("도어 상태를 알 수 없습니다.")

    # 문열기
    def doorOpenProcess(self):
        response = dict()
        response["data"] = dict()

        if self.doorlock is None:
            response["response"] = "unlockFail"
            response["data"]["result"] = False
            response["data"]["message"] = "도어락이 연결되지 않았습니다."
        elif self.isDoorlock():
            response["response"] = "unlocked"
            response["data"]["result"] = False
            response["data"]["message"] = "이미 도어락이 열렸습니다."
        else:
            try:
                th = threading.Thread(target=self.doorlock.doorOpenProcess)
                th.start()
                th.join()
            except Exception as e:
                lib.log(e)

            response["response"] = "unlocked"
            response["data"]["result"] = True
            response["data"]["isDoorlock"] = self.isDoorlock()

        self.sendMqttAll(lib.jsonencode(response))

        return True

    # 문닫기
    def doorCloseProcess(self):
        response = dict()
        response["data"] = dict()

        lib.log("문상태 ; %s" % self.doorlockStatus)

        if self.doorlock is None:
            response["response"] = "lockFail"
            response["data"]["result"] = False
            response["data"]["message"] = "도어락이 연결되지 않았습니다."
        elif not self.isDoorlock():
            response["response"] = "locked"
            response["data"]["result"] = False
            response["data"]["message"] = "이미 도어락이 잠겨있습니다."
        else:
            try:
                th = threading.Thread(target=self.doorlock.doorCloseProcess)
                th.start()
                th.join()
            except Exception as e:
                lib.log(e)

            response["response"] = "locked"
            response["data"]["result"] = True
            response["data"]["isDoorlock"] = self.isDoorlock()

        self.sendMqttAll(lib.jsonencode(response))

        return True

    # 문열기 상태 처리
    def doorOpenStatusProcess(self, smartdoor_cmd_id=None):
        try:
            if self.isDoorOpen():
                elcsoft.controller.smartdoor_cmd.doorOpenedProcess(smartdoor_cmd_id)
            else:
                elcsoft.controller.smartdoor_cmd.doorOpenFailProcess(smartdoor_cmd_id)
        except Exception as e:
            logger.Logger._LOGGER.info(e)

    # 문닫기 상태 처리
    def doorCloseStatusProcess(self, smartdoor_cmd_id=None):
        try:
            if not self.isDoorOpen():
                elcsoft.controller.smartdoor_cmd.doorClosedProcess(smartdoor_cmd_id)
            else:
                elcsoft.controller.smartdoor_cmd.doorCloseFailProcess(smartdoor_cmd_id)
        except Exception as e:
            logger.Logger._LOGGER.info(e)

    # QR코드로 문열기
    def doorOpenByQrProcess(self, pkValue):
        if type(pkValue) == str:
            pkValue = int(pkValue)

        if pkValue <= 0:
            raise Exception("게스트키 정보가 없습니다.")

        obj = elcsoft.model.smartdoor_guestkey.SmartdoorGuestkey()
        obj.getData(pkValue)

        if obj.__pkValue__ <= 0:
            elcsoft.controller.smartdoor_guestkey.downloadProcess()

        obj.getData(pkValue)

        if obj.__pkValue__ <= 0:
            raise Exception("존재하지 않는 게스트키 정보입니다.")

        if lib.isCurrentTimeAfter(obj.startDate):
            raise Exception("게스트키 사용은 %s 부터입니다." % obj.startDate)

        if lib.isCurrentTimeBefore(obj.stopDate):
            raise Exception("만료된 게스트키입니다.")

        obj = elcsoft.controller.smartdoor_cmd.smartdoorCmdProcess(95)
        self.doorOpenProcess()
        self.doorOpenStatusProcess(obj.__pkValue__)

    # KIOSK에서 문열기
    def doorOpenAtKioskProcess(self):
        obj = elcsoft.controller.smartdoor_cmd.smartdoorCmdProcess(96)
        self.doorOpenProcess()
        self.doorOpenStatusProcess(obj.__pkValue__)

    # KIOSK에서 문닫기
    def doorCloseAtKioskProcess(self):
        obj = elcsoft.controller.smartdoor_cmd.smartdoorCmdProcess(97)
        self.doorCloseProcess()
        self.doorCloseStatusProcess(obj.__pkValue__)

    # APP에서 문열기
    def doorOpenAtAppProcess(self, user_id):
        if type(user_id) == str:
            user_id = int(user_id)

        if user_id == None or user_id <= 0:
            raise Exception("회원정보가 없어 APP으로 문열기를 수행할 수 없습니다.")

        obj = elcsoft.model.user.User()
        obj.getData(user_id)

        if obj.__pkValue__ <= 0:
            raise Exception("존재하지 않는 회원정보입니다.")

        obj = elcsoft.controller.smartdoor_cmd.smartdoorCmdProcess(98, user_id)
        self.doorOpenProcess()
        self.doorOpenStatusProcess(obj.__pkValue__)

    # App에서 문닫기
    def doorCloseAtAppProcess(self, user_id):
        if type(user_id) == str:
            user_id = int(user_id)

        if user_id == None or user_id <= 0:
            raise Exception("회원정보가 없어 APP으로 문닫기를 수행할 수 없습니다.")

        obj = elcsoft.controller.smartdoor_cmd.smartdoorCmdProcess(99, user_id)
        self.doorCloseProcess()
        self.doorCloseStatusProcess(obj.__pkValue__)

    # APP에서 문열기
    def doorOpenAtWebProcess(self, user_id):
        logger.Logger._LOGGER.info(f"user_id : {user_id}")
        if type(user_id) == str:
            user_id = int(user_id)

        if user_id == None or user_id <= 0:
            raise Exception("회원정보가 없어 WEB으로 문열기를 수행할 수 없습니다.")

        obj = elcsoft.model.user.User()
        obj.getData(user_id)

        if obj.__pkValue__ <= 0:
            raise Exception("존재하지 않는 회원정보입니다.")

        obj = elcsoft.controller.smartdoor_cmd.smartdoorCmdProcess(92, user_id)
        self.doorOpenProcess()
        self.doorOpenStatusProcess(obj.__pkValue__)

    # App에서 문닫기
    def doorCloseAtWebProcess(self, user_id):
        if type(user_id) == str:
            user_id = int(user_id)

        if user_id == None or user_id <= 0:
            raise Exception("회원정보가 없어 WEB으로 문닫기를 수행할 수 없습니다.")

        obj = elcsoft.controller.smartdoor_cmd.smartdoorCmdProcess(93, user_id)
        self.doorCloseProcess()
        self.doorCloseStatusProcess(obj.__pkValue__)

    # mqtt로 관리자가 문열기
    def doorOpenByAdminProcess(self):
        self.doorOpenProcess()

    # mqtt로 관리자가 문열기
    def doorCloseByAdminProcess(self):
        self.doorCloseProcess()

    # FACE로 문열기
    def doorOpenByFaceProcess(self, user_id):
        if type(user_id) == str:
            user_id = int(user_id)

        if user_id == None or user_id <= 0:
            raise Exception("회원정보가 없어 페이스로 문열기를 수행할 수 없습니다.")

        obj = elcsoft.model.user.User()
        obj.getData(user_id)

        if obj.__pkValue__ <= 0:
            raise Exception("존재하지 않는 회원정보입니다.")

        obj = elcsoft.controller.smartdoor_cmd.smartdoorCmdProcess(94, user_id)
        self.doorOpenProcess()
        self.doorOpenStatusProcess(obj.__pkValue__)

    ################################################################################################################################
    #####
    #####   사운드 관련
    #####
    ################################################################################################################################

    # 도어벨 소리
    def play_doorbell(self):
        logger.Logger._LOGGER.info(
            "--------------------------------- 도어벨 사운드 실행 start ---------------------------------"
        )
        playlists = [
            {
                "file": self.config["doorbell"]["file"],
                "count": self.config["doorbell"]["count"],
                "speed": 1,
            }
        ]
        elcsoft.controller.sound.playInsideSpeaker(self, playlists)
        logger.Logger._LOGGER.info(
            "--------------------------------- 도어벨 사운드 실행 stop ---------------------------------"
        )

    # 문열림 안내
    def play_dooropen(self):
        logger.Logger._LOGGER.info(
            "--------------------------------- 자동문 안내 사운드 start ---------------------------------"
        )
        playlists = [{"file": self.config["dooropend"]["file"], "count": 1, "speed": 1}]
        # elcsoft.controller.sound.playOutsideSpeaker(self, playlists)
        elcsoft.controller.sound.playOutsideSpeaker(self, playlists)
        logger.Logger._LOGGER.info(
            "--------------------------------- 자동문 안내 사운드 stop ---------------------------------"
        )

    # 음성 안내 시작
    def ttsStart(self):
        logger.Logger._LOGGER.info(
            "--------------------------------- tts 사운드 start ---------------------------------"
        )
        playlists = []
        playlists.extend(lib.search_files(self.config["tts"]["path"], "notice"))
        playlists.extend(lib.search_files(self.config["tts"]["path"], "schedule"))
        playlists.extend(lib.search_files(self.config["tts"]["path"], "message"))
        playlists.extend(lib.search_files(self.config["tts"]["path"], "item"))

        # 기본 반복 횟수와 속도로 추가
        elcsoft.controller.sound.playInsideSpeaker(self, playlists)
        logger.Logger._LOGGER.info(
            "--------------------------------- tts 사운드 stop ---------------------------------"
        )

    # 음성 안내 중단
    def ttsStop(self):
        self.insideSpeaker.stop()

    ################################################################################################################################
    #####
    #####   기능 관련
    #####
    ################################################################################################################################

    # 도어벨 푸시 액션
    def doorbellPush(self):
        logger.Logger._LOGGER.info(
            "--------------------------------- doorbellPush start ---------------------------------"
        )

        try:
            threading.Thread(target=self.screenOn()).start()
            logger.Logger._LOGGER.info("doorbellPush : 스크린 켜기")
        except Exception as e:
            logger.Logger._LOGGER.info("스크린 error : %s" % e)

        try:
            threading.Thread(
                target=self.sendKiosk, args=("doorbellPushProcess",)
            ).start()
            logger.Logger._LOGGER.info("doorbellPush : 키오스크 메세지 발송")
        except Exception as e:
            logger.Logger._LOGGER.info("키오스크전송 error : %s" % e)

        try:
            threading.Thread(target=self.play_doorbell).start()
            # self.play_doorbell()
            logger.Logger._LOGGER.info("doorbellPush : 도어벨 플레이")
        except Exception as e:
            logger.Logger._LOGGER.info("도어벨 error : %s" % e)

        try:
            threading.Thread(
                target=elcsoft.controller.smartdoor.doorbellPushProcess
            ).start()
            logger.Logger._LOGGER.info("푸시 메세지 발송")
        except Exception as e:
            logger.Logger._LOGGER.info("FCM발송 error : %s" % e)

        logger.Logger._LOGGER.info(
            "--------------------------------- doorbellPush stop ---------------------------------"
        )

    # 스크린켜기
    def screenOn(self):
        if self.screen is None:
            self.screen = screen.Screen()
            self.screen.wikismartdoor = self

        # threading.Thread(target=self.screen.run).start()
        self.screen.run()

    # 스크린끄기
    def screenOff(self):
        if self.screen is None:
            self.screen = screen.Screen()
            self.screen.wikismartdoor = self

        # threading.Thread(target=self.screen.off).start()
        self.screen.off()

    # 동기화
    def syncDataAll(self):
        threading.Thread(target=elcsoft.controller.smartdoor.syncProcess).start()

    ################################################################################################################################
    #####
    #####   콜백함수 관련
    #####
    ################################################################################################################################

    def pir_inside_moved(self):
        logger.Logger._LOGGER.info(
            f"------------------------- 내측 PIR Moved Start -------------------------"
        )
        elcsoft.controller.pir.inside.moved_callback(self)
        logger.Logger._LOGGER.info(
            f"------------------------- 내측 PIR Moved Stop -------------------------"
        )

    def pir_inside_finished(self):
        logger.Logger._LOGGER.info(
            f"------------------------- 내측 PIR Finished Start -------------------------"
        )
        elcsoft.controller.pir.inside.finished_callback(self)
        logger.Logger._LOGGER.info(
            f"------------------------- 내측 PIR Finished Stop -------------------------"
        )

    # 외측 PIR 버튼 누름
    def pir_outside_pushed(self):
        logger.Logger._LOGGER.info(
            f"------------------------- 외측 벨 푸시 Start -------------------------"
        )
        elcsoft.controller.pir.outside.pushed_callback(self)
        logger.Logger._LOGGER.info(
            f"------------------------- 외측 벨 푸시 Stop -------------------------"
        )

    # 외측 PIR 움직임 반응
    def pir_outside_moved(self):
        logger.Logger._LOGGER.info(
            f"------------------------- 외측 PIR Moved Start -------------------------"
        )
        elcsoft.controller.pir.outside.moved_callback(self)
        logger.Logger._LOGGER.info(
            f"------------------------- 외측 PIR Moved Stop -------------------------"
        )

    # 외측 PIR 움직임 종료
    def pir_outside_finished(self):
        logger.Logger._LOGGER.info(
            f"------------------------- 외측 PIR Finished Start -------------------------"
        )
        elcsoft.controller.pir.outside.finished_callback(self)
        logger.Logger._LOGGER.info(
            f"------------------------- 외측 PIR Finished Stop -------------------------"
        )

    # 도어클로저 작동
    def doorcloser_openProcess(self):
        logger.Logger._LOGGER.info(
            f"------------------------- 도어크로저 문열기 Start -------------------------"
        )
        elcsoft.controller.cmd.doorcloser.openProcess(self)
        logger.Logger._LOGGER.info(
            f"------------------------- 도어크로저 문열기 Stop -------------------------"
        )

    # 도어클로저 안전모드
    def doorcloser_safeModeProcess(self):
        logger.Logger._LOGGER.info(
            f"------------------------- 도어크로저 안전모드 Start -------------------------"
        )
        elcsoft.controller.cmd.doorcloser.safeModeProcess(self)
        logger.Logger._LOGGER.info(
            f"------------------------- 도어크로저 안전모드 Stop -------------------------"
        )

    # 문이 열렸을때 작동하는 함수
    def doorOpend(self):
        logger.Logger._LOGGER.info(
            f"------------------------- Door Opened Start -------------------------"
        )
        elcsoft.controller.cmd.doorsystem.doorOpend(self)
        logger.Logger._LOGGER.info(
            f"------------------------- Door Opened Stop -------------------------"
        )

    # 문이 닫혔을때 작동하는 함수
    def doorClosed(self):
        logger.Logger._LOGGER.info(
            f"------------------------- Door Closed Start -------------------------"
        )
        elcsoft.controller.cmd.doorsystem.doorClosed(self)
        logger.Logger._LOGGER.info(
            f"------------------------- Door Closed Stop -------------------------"
        )

    ################################################################################################################################
    #####
    #####   버튼 관련
    #####
    ################################################################################################################################

    import os
    import button
    import RPi.GPIO as GPIO  # 버튼 핀 상태 직접 확인용

    def on_button_pressed(channel):
        logger.Logger._LOGGER.info("🟢 버튼 눌림 감지됨")
        start_time = time.time()

        # 버튼이 눌린 상태 유지되는 동안 대기
        while GPIO.input(channel) == GPIO.LOW:
            time.sleep(0.1)

        press_duration = time.time() - start_time
        logger.Logger._LOGGER.info(f"버튼 누름 지속 시간: {press_duration:.2f}초")

        if press_duration >= 3:
            logger.Logger._LOGGER.info("🔴 시스템 종료 요청됨 (3초 이상 버튼 누름)")
            os.system("sudo shutdown now")
        else:
            logger.Logger._LOGGER.info("🟡 시스템 재부팅 요청됨 (짧게 버튼 누름)")
            os.system("sudo reboot")

    def initialize_button():
        button.setup_button(on_button_pressed)
        logger.Logger._LOGGER.info("✅ 버튼 이벤트 기반 초기화 완료")

    def cleanup_button():
        button.cleanup()
        logger.Logger._LOGGER.info("🧹 GPIO 정리 완료 및 프로그램 종료")

