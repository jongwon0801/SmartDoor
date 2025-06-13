from PIL import Image

# 이미지 경로
# img_path = "/Users/jongwon/test/home/img/logo.png"     # 파란색 wise   275 x 45 픽셀
# img_path = "/Users/jongwon/test/home/img/logo_w.png"   # 흰색 wise  471 x 77 픽셀
img_path = "/Users/jongwon/test/box01_text.png"  # 흰색 배경  496 x 54 픽셀

# 이미지 열기
img = Image.open(img_path)

# 크기 출력 (width, height)
print(f"이미지 크기: {img.size[0]} x {img.size[1]} 픽셀")
