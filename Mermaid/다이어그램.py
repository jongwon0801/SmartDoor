import base64
import io
import requests
from PIL import Image
import matplotlib.pyplot as plt

def mermaid_to_png(graph, filename="diagram.png"):
    """
    Mermaid 코드를 받아서 PNG로 저장하고 화면에 표시하는 함수
    """
    # Mermaid 코드를 base64로 변환
    graph_bytes = graph.encode("utf-8")
    base64_bytes = base64.urlsafe_b64encode(graph_bytes)
    base64_string = base64_bytes.decode("ascii")

    # Mermaid API에서 이미지 가져오기
    url = f"https://mermaid.ink/img/{base64_string}"
    response = requests.get(url)
    response.raise_for_status()  # 요청 실패 시 에러

    # 이미지 열기
    img = Image.open(io.BytesIO(response.content))

    # 파일로 저장
    img.save(filename)
    print(f"Saved diagram as {filename}")

    # 화면에 표시
    plt.imshow(img)
    plt.axis("off")
    plt.show()


# Mermaid 다이어그램 코드
diagram = """
graph LR;

%% 스마트도어 컨테이너
subgraph SD[Smart Door Container]
    PIR_OUT[PIR Sensor (Outside)]
    PIR_IN[PIR Sensor (Inside)]
    CAM[Camera]
    BELL[Bell]
    SPEAKER[Speaker]
    MIC[Microphone]
    GPIO[GPIO Devices]
    
    PIR_OUT --> SD
    PIR_IN --> SD
    CAM --> SD
    BELL --> SD
    SPEAKER --> SD
    MIC --> SD
    GPIO --> SD
end

%% 홈어시스턴트 컨테이너
subgraph HA[Home Assistant Container]
    LIGHT[Light]
    CURTAIN[Curtain]
    SWITCH[Switch]
    PLUG[Smart Plug]
    SENSOR[Various Sensors]
    
    LIGHT --> HA
    CURTAIN --> HA
    SWITCH --> HA
    PLUG --> HA
    SENSOR --> HA
end

%% 컨테이너 간 연결
SD --> MQTT[MQTT Broker] <-- HA
"""

# PNG로 변환 및 표시
mermaid_to_png(diagram, "smartdoor_homeassistant_detailed.png")
