import requests
import cairosvg

# Mermaid 다이어그램 코드
diagram = """
graph LR;

%% 클라우드 브로커
MQTT[MQTT Broker (Cloud)] 

%% 스마트도어 컨테이너
subgraph SD[Smart Door Container (Tornado)]
    PIR_OUT[PIR Sensor (Outside)]
    PIR_IN[PIR Sensor (Inside)]
    CAM[Camera]
    BELL[Bell]
    SPEAKER[Speaker]
    MIC[Microphone]
    GPIO[GPIO Devices]
end

%% 홈어시스턴트 컨테이너
subgraph HA[Home Assistant Container]
    LIGHT[Light]
    CURTAIN[Curtain]
    SWITCH[Switch]
    PLUG[Smart Plug]
    SENSOR[Various Sensors]
end

%% 모바일 앱
MOBILE[Mobile App]

%% 웹 브라우저
BROWSER[Web Browser UI]

%% 스마트도어 통신
SD -->|MQTT| MQTT
SD -->|HTTP REST| MOBILE
SD -->|WebSocket| BROWSER

%% 홈어시스턴트 통신
HA -->|MQTT| MQTT
HA -->|HTTP REST| MOBILE
"""


def mermaid_to_png_post(graph, filename="diagram.png"):
    """
    Mermaid 코드를 POST로 보내서 PNG로 저장
    """
    url = "https://mermaid.ink/img/svg/"
    data = {"code": graph}

    response = requests.post(url, json=data)
    response.raise_for_status()

    # SVG 저장
    svg_file = filename.replace(".png", ".svg")
    with open(svg_file, "wb") as f:
        f.write(response.content)
    print(f"Saved {svg_file}")

    # PNG로 변환
    cairosvg.svg2png(url=svg_file, write_to=filename)
    print(f"Saved {filename}")


# 실행
mermaid_to_png_post(diagram, "smartdoor_homeassistant_network.png")
