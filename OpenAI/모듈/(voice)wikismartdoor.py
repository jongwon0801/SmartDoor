
    ################################################################################################################################
    #####
    #####   보이스 관련
    #####
    ################################################################################################################################

    def play_audio(self, filepath):
        logger.Logger._LOGGER.info(f"[play_audio] 재생할 파일: {filepath}")
        playlists = [{"file": filepath, "count": 1, "speed": 1}]
        elcsoft.controller.sound.playOutsideSpeaker(self, playlists)

    def voice_record(
        self,
        duration=4,
        sample_rate=24000,
        filename="user_voice.wav",
        folder="/home/pi/guest_voice",
    ) -> str:
        import os
        import time
        import sounddevice as sd
        import soundfile as sf
        import logger

        logger.Logger._LOGGER.info("[voice_record] 시작")

        # 장치 정보 로그 출력
        try:
            devices = sd.query_devices()
            logger.Logger._LOGGER.info("[voice_record] 사용 가능한 오디오 장치 목록:")
            for idx, device in enumerate(devices):
                logger.Logger._LOGGER.info(
                    f"  [{idx}] {device['name']} - Input Channels: {device['max_input_channels']}"
                )

            default_input = sd.default.device[0]
            logger.Logger._LOGGER.info(
                f"[voice_record] 기본 입력 장치 번호: {default_input}"
            )
        except Exception as e:
            logger.Logger._LOGGER.warning(f"[voice_record] 장치 정보 조회 실패: {e}")

        # 폴더 확인 및 생성
        if not os.path.exists(folder):
            logger.Logger._LOGGER.info(f"[voice_record] 폴더가 없어서 생성: {folder}")
            os.makedirs(folder)

        filepath = os.path.join(folder, filename)
        logger.Logger._LOGGER.info(
            f"[voice_record] 🎙️ 음성 녹음 시작... {duration}초간 말해주세요."
        )

        try:
            # 기본 입력 장치 사용
            recording = sd.rec(
                int(duration * sample_rate), samplerate=sample_rate, channels=1
            )
            sd.wait()

            # 녹음 파일 저장
            sf.write(filepath, recording, sample_rate)
            logger.Logger._LOGGER.info(
                f"[voice_record] ✅ 녹음 완료, 파일 저장: {filepath}"
            )

            time.sleep(0.5)
            return filepath

        except Exception as e:
            logger.Logger._LOGGER.error(f"[voice_record 오류] {e}")
            return ""

    def voice_text(self, audio_path: str, model: str = "whisper-1") -> str:
        import os
        import openai
        import requests

        logger.Logger._LOGGER.info(f"[voice_text] 시작, audio_path: {audio_path}")

        # ✅ 보안상 하드코딩된 API 키는 실제 운영에서는 제거하세요!
        openai.api_key = "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"  # ⚠️ 실제 코드에서는 환경변수 등으로 관리하세요
        API_KEY = openai.api_key

        if not os.path.isfile(audio_path):
            logger.Logger._LOGGER.error(
                f"[voice_text] 오류: 파일이 없습니다: {audio_path}"
            )
            return ""

        try:
            with open(audio_path, "rb") as audio_file:
                response = requests.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    files={"file": (os.path.basename(audio_path), audio_file)},
                    data={"model": model},
                )
        except Exception as e:
            logger.Logger._LOGGER.error(f"[voice_text] 요청 중 예외 발생: {e}")
            return ""

        if response.ok:
            try:
                text = response.json().get("text", "")
                logger.Logger._LOGGER.info(f"[voice_text] 변환된 텍스트: {text}")
                return text
            except Exception as e:
                logger.Logger._LOGGER.error(f"[voice_text] JSON 파싱 실패: {e}")
                return ""
        else:
            logger.Logger._LOGGER.error(
                f"[voice_text] API 호출 실패: {response.status_code} {response.text}"
            )
            return ""

    def voice_intent(self, user_text: str) -> str:
        import openai
        import json

        logger.Logger._LOGGER.info(f"[voice_intent] 사용자 텍스트: {user_text}")

        try:
            # ✅ 보안상 API 키는 환경변수로 관리하는 것을 권장합니다
            # openai.api_key = os.getenv("OPENAI_API_KEY")
            openai.api_key = "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"
            messages = [
                {
                    "role": "system",
                    "content": (
                        "당신은 스마트 도어 시스템의 음성 명령 의도를 분류하는 AI입니다. "
                        "가능한 의도는 'door_open', 'call_owner', 'password_input', 'unknown'입니다. "
                        '오직 JSON 형식으로 {"intent": "의도키워드"}만 응답하세요.'
                    ),
                },
                {
                    "role": "user",
                    "content": f"사용자 발화: '{user_text}'. 이 발화의 의도를 알려주세요.",
                },
            ]

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages, temperature=0
            )

            intent_str = response.choices[0].message.content.strip()
            logger.Logger._LOGGER.info(f"[voice_intent] GPT 응답: {intent_str}")

            intent_json = json.loads(intent_str)
            intent = intent_json.get("intent", "unknown")
            logger.Logger._LOGGER.info(f"[voice_intent] 파싱된 intent: {intent}")

            return intent

        except Exception as e:
            logger.Logger._LOGGER.error(f"[voice_intent 오류] {e}")
            return "unknown"

    def voice_process(self):
        logger.Logger._LOGGER.info("[voice_process] 시작")
        try:
            # 안내 음성 재생 후 3초 대기
            self.play_audio("/home/pi/guest_voice/info.wav")
            time.sleep(3)

            # 음성 녹음 시작
            self.play_audio("/home/pi/guest_voice/voice_start.wav")
            time.sleep(2)
            voice_path = self.voice_record()
            if not voice_path:
                logger.Logger._LOGGER.info("[voice_process] 음성 녹음 실패")
                self.play_audio("/home/pi/guest_voice/voice_record_no.wav")
                time.sleep(4)
                return

            # 텍스트 변환
            user_text = self.voice_text(voice_path)
            if not user_text:
                logger.Logger._LOGGER.info("[voice_process] 텍스트 변환 실패")
                self.play_audio("/home/pi/guest_voice/voice_text_no.wav")
                time.sleep(4)
                return

            lowered = user_text.lower()
            logger.Logger._LOGGER.info(
                f"[voice_process] 인식된 텍스트 소문자 변환: {lowered}"
            )

            # 의도 판단
            if "문 열" in lowered or "열어" in lowered:
                intent = "door_open"
                logger.Logger._LOGGER.info(
                    "[voice_process] 조건문으로 door_open 인텐트 결정"
                )
            elif "입주자" in lowered or "주인" in lowered or "호출" in lowered:
                intent = "call_owner"
                logger.Logger._LOGGER.info(
                    "[voice_process] 조건문으로 call_owner 인텐트 결정"
                )
            else:
                intent = self.voice_intent(user_text)

            # 결과 처리
            if intent == "door_open":
                logger.Logger._LOGGER.info("[voice_process] door_open 인텐트 처리 시작")
                self.doorOpenProcess()
            elif intent == "call_owner":
                logger.Logger._LOGGER.info(
                    "[voice_process] call_owner 인텐트 처리 시작"
                )
                self.play_audio("/home/pi/guest_voice/call_owner.wav")
                # self.call_owner()
            else:
                logger.Logger._LOGGER.info(
                    "[voice_process] 알 수 없는 인텐트, 다시 시도 안내 음성 재생"
                )
                self.play_audio("/home/pi/guest_voice/intent_no.wav")
                time.sleep(4)

        except Exception as e:
            logger.Logger._LOGGER.error(f"[voice_process 오류] {e}")
            self.play_audio("/home/pi/guest_voice/exception.wav")
            time.sleep(2)
