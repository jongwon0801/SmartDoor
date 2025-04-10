# -*- coding: utf-8 -*-
import argparse
import urllib
import lib
import mqtt_client
import elcsoft.controller.mqtt.smartdoor_cmd
import elcsoft.controller.mqtt.smartdoor_user
import elcsoft.controller.mqtt.smartdoor_notice
import elcsoft.controller.mqtt.smartdoor_schedule
import elcsoft.controller.mqtt.smartdoor_item
import elcsoft.controller.mqtt.smartdoor_message
import elcsoft.controller.mqtt.smartdoor_vod
import elcsoft.controller.mqtt.admin
import elcsoft.controller.mqtt.user
import threading

class MqttSubscribe(mqtt_client.MqttClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.wikismartdoor = kwargs.get('wikismartdoor', None)

        if self.wikismartdoor is not None:
            if self.wikismartdoor.mqtt is None :
                self.wikismartdoor.mqtt = self
        
        # 요청에 대한 처리 함수 매핑
        self.request_handlers = {
            "/Smartdoor/isDoorOpen": elcsoft.controller.mqtt.smartdoor_cmd.isDoorOpen,
            "/Smartdoor/doorOpenByAppProcess": elcsoft.controller.mqtt.smartdoor_cmd.doorOpenAtAppProcess,
            "/Smartdoor/doorOpenAtAppProcess": elcsoft.controller.mqtt.smartdoor_cmd.doorOpenAtAppProcess,
            "/Smartdoor/doorCloseAtAppProcess": elcsoft.controller.mqtt.smartdoor_cmd.doorCloseAtAppProcess,
            "/Smartdoor/doorOpenAtWebProcess": elcsoft.controller.mqtt.smartdoor_cmd.doorOpenAtWebProcess,
            "/Smartdoor/doorCloseAtWebProcess": elcsoft.controller.mqtt.smartdoor_cmd.doorCloseAtWebProcess,
            "/Smartdoor/doorOpenByAdminProcess": elcsoft.controller.mqtt.smartdoor_cmd.doorOpenByAdminProcess,
            "/Smartdoor/doorCloseByAdminProcess": elcsoft.controller.mqtt.smartdoor_cmd.doorCloseByAdminProcess,
            "/Smartdoor/guestkeyJoinProcess": elcsoft.controller.mqtt.smartdoor_cmd.guestkeyJoinProcess,
            "/Smartdoor/channelJoinProcess": elcsoft.controller.mqtt.smartdoor_cmd.channelJoinProcess,
            #관리자용
            "/Admin/doorOpenByAdminProcess": elcsoft.controller.mqtt.admin.doorOpenByAdminProcess,
            "/Admin/initProcess": elcsoft.controller.mqtt.admin.initProcess,
            "/Admin/refresh": elcsoft.controller.mqtt.admin.refresh,
            #사용자용
            "/User/faceUpdateProcess": elcsoft.controller.mqtt.user.faceUpdateProcess,
            "/User/faceDeleteProcess": elcsoft.controller.mqtt.user.faceDeleteProcess,
            "/User/updateProcess": elcsoft.controller.mqtt.user.updateProcess,
            #스마트도어 사용자용
            "/SmartdoorUser/joinProcess": elcsoft.controller.mqtt.smartdoor_user.joinProcess,
            "/SmartdoorUser/updateProcess": elcsoft.controller.mqtt.smartdoor_user.updateProcess,
            "/SmartdoorUser/deleteProcess": elcsoft.controller.mqtt.smartdoor_user.deleteProcess,
            "/SmartdoorUser/me": elcsoft.controller.mqtt.smartdoor_user.me,
            #공지사항
            "/SmartdoorNotice/joinProcess": elcsoft.controller.mqtt.smartdoor_notice.joinProcess,
            "/SmartdoorNotice/updateProcess": elcsoft.controller.mqtt.smartdoor_notice.updateProcess,
            "/SmartdoorNotice/deleteProcess": elcsoft.controller.mqtt.smartdoor_notice.deleteProcess,
            #일정
            "/SmartdoorSchedule/joinProcess": elcsoft.controller.mqtt.smartdoor_schedule.joinProcess,
            "/SmartdoorSchedule/updateProcess": elcsoft.controller.mqtt.smartdoor_schedule.updateProcess,
            "/SmartdoorSchedule/deleteProcess": elcsoft.controller.mqtt.smartdoor_schedule.deleteProcess,
            #소지품
            "/SmartdoorItem/joinProcess": elcsoft.controller.mqtt.smartdoor_item.joinProcess,
            "/SmartdoorItem/updateProcess": elcsoft.controller.mqtt.smartdoor_item.updateProcess,
            "/SmartdoorItem/deleteProcess": elcsoft.controller.mqtt.smartdoor_item.deleteProcess,
            #일정
            "/SmartdoorMessage/joinProcess": elcsoft.controller.mqtt.smartdoor_message.joinProcess,
            "/SmartdoorMessage/updateProcess": elcsoft.controller.mqtt.smartdoor_message.updateProcess,
            "/SmartdoorMessage/deleteProcess": elcsoft.controller.mqtt.smartdoor_message.deleteProcess,
            #녹화영상
            "/SmartdoorVod/streamProcess": elcsoft.controller.mqtt.smartdoor_vod.streamProcess,
            "/SmartdoorVod/unstreamProcess": elcsoft.controller.mqtt.smartdoor_vod.unstreamProcess,
        }

    def on_message(self, client, userdata, msg):
        lib.log(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

        try:
            #lib.log(msg.payload.decode('utf-8'))
            #lib.log(urllib.parse.unquote(msg.payload.decode('utf-8')))

            d = dict()
            d['topic'] = msg.topic
            d['qos'] = msg.qos
            d['retain'] = msg.retain
            d['msg'] = lib.jsondecode(urllib.parse.unquote(msg.payload.decode('utf-8')))

            if hasattr(msg, 'properties') and hasattr(msg.properties, 'ResponseTopic'):
                d['resTopic'] = msg.properties.ResponseTopic
            elif 'resTopic' in d['msg']:
                d['resTopic'] = d['msg']['resTopic']

            # print(d)
            #lib.log(f"MQTT - Received {d}")
            if 'resTopic' in d['msg'] and 'msg' in d['msg']:
                result = d['msg']['msg']
            else:
                result = d['msg']

            request = result.get('request')

            # 요청에 따라 적절한 핸들러 호출
            if request in self.request_handlers:
                method = self.request_handlers[request]
                method(self.wikismartdoor, d['msg'])
                #th = threading.Thread(target=method, args=(self.wikismartdoor, d['msg'],))
                #th.start()  # 데몬 스레드로 설정하지 않음
            else:
                lib.log(f"Unknown request: {request}")
        except Exception as e:
            lib.log(f"Error processing message: {e}")
