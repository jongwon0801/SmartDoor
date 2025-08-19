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

"""

# PNG로 변환 및 표시
mermaid_to_png(diagram, "smartdoor_homeassistant_detailed.png")
