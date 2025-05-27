import os
import time
import sounddevice as sd
import soundfile as sf

def voice_record(
    duration=4,
    sample_rate=24000,
    filename="user_voice.wav",
    folder="/home/pi/guest_voice",
) -> str:
    # PulseAudio 환경변수 설정 (Python 프로세스 내에서만 유효)
    os.environ["XDG_RUNTIME_DIR"] = "/run/user/1000"
    os.environ["PULSE_SERVER"] = "unix:/run/user/1000/pulse/native"

    print("[voice_record] 시작")

    if not os.path.exists(folder):
        print(f"[voice_record] 폴더가 없어서 생성: {folder}")
        os.makedirs(folder)

    filepath = os.path.join(folder, filename)

    print(f"🎙️ 음성 녹음 시작... {duration}초간 말해주세요.")

    try:
        # 녹음 시작 (device=2는 USB 4K Live Camera 마이크)
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            device=2,
        )
        sd.wait()  # 녹음 완료 대기

        # 파일로 저장
        sf.write(filepath, recording, sample_rate)
        print(f"✅ 녹음 완료, 파일 저장: {filepath}")

        time.sleep(0.5)
        return filepath

    except Exception as e:
        print(f"[record_user_voice 오류] {e}")
        return ""

if __name__ == "__main__":
    # 직접 실행 시 테스트
    recorded_file = voice_record()
    if recorded_file:
        print(f"녹음 파일 위치: {recorded_file}")
    else:
        print("녹음 실패")
