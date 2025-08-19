import base64
import io
import requests
from PIL import Image
import matplotlib.pyplot as plt

# -------------------------------
# Mermaid 다이어그램 코드 (라즈베리 중심 + 통신)
# -------------------------------
diagram = """
graph LR;

%% 라즈베리 파이
subgraph RPi[Raspberry Pi]
    %% 스마트도어 컨테이너
    subgraph SD[Smart Door]
        PIR[PIR Sensor]
        CAM[Camera]
        BELL[Bell]
        SPEAKER[Speaker]
        MIC[Microphone]
    end

    %% 홈어시스턴트 컨테이너
    subgraph HA[Home Assistant]
        LIGHT[Light]
        CURTAIN[Curtain]
        SWITCH[Switch]
        PLUG[Smart Plug]
    end
end

%% 클라우드 서버와 MQTT/HTTP
SERVER[Cloud Server]
RPi -->|MQTT| SERVER
PHONE[Mobile App]
RPi -->|MQTT| PHONE
PHONE -->|HTTP REST| SERVER
"""


# -------------------------------
# Mermaid → PNG 변환 함수 (GET 방식)
# -------------------------------
def mermaid_to_png_get(graph, filename="diagram.png"):
    graph_bytes = graph.encode("utf-8")
    base64_bytes = base64.urlsafe_b64encode(graph_bytes)
    base64_string = base64_bytes.decode("ascii")

    url = f"https://mermaid.ink/img/{base64_string}"
    response = requests.get(url)
    response.raise_for_status()

    img = Image.open(io.BytesIO(response.content))
    img.save(filename)
    print(f"Saved {filename}")

    plt.imshow(img)
    plt.axis("off")
    plt.show()


# -------------------------------
# 실행
# -------------------------------
mermaid_to_png_get(diagram, "smartdoor_rpi_mqtt_http.png")
