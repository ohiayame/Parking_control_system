# from PIL import Image
# from pytesseract import *
# try:
#     # Tesseractのパスを設定（引用符で囲む）
#     filename =  r"C:\Users\USER\Pictures\Screenshots\test_number2.png"

#     # 画像を開く
#     image = Image.open(filename)

#     # 画像からテキストを抽出（日本語）
#     text = image_to_string(image, lang= 'kor+eng' )

#     # # 抽出したテキストを表示
#     # print(text)
#     if text.strip():
#             print(text)
#     else:
#         print("画像からテキストを認識できませんでした。")
# except Exception as e:
#     print(f"エラーが発生しました: {e}")

import pytesseract
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

# Tesseractの実行ファイルのパスを指定
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # 画像をグレースケールに変換
    gray_image = ImageOps.grayscale(image)
    # コントラストを調整
    enhancer = ImageEnhance.Contrast(gray_image)
    contrast_image = enhancer.enhance(2)  # コントラストを2倍にする
      # 明るさを調整（必要に応じて）
    brightness_enhancer = ImageEnhance.Brightness(contrast_image)
    bright_image = brightness_enhancer.enhance(1.5)  # 明るさを1.5倍にする
    # 画像を二値化
    bin_image = bright_image.point(lambda x: 0 if x < 128 else 255, '1')

    # 画像のノイズを除去
    clean_image = bin_image.filter(ImageFilter.MedianFilter())

    # エッジを強調
    edge_image = clean_image.filter(ImageFilter.EDGE_ENHANCE)

    return edge_image

def recognize_text(image_path):
        # 画像の読み込み
        image = Image.open(image_path)
        print("画像が正常に読み込まれました。")

        # 画像の前処理
        preprocessed_image = preprocess_image(image)

        # 言語コードを英語に設定（数字のみ認識）
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(preprocessed_image, lang='kor', config=custom_config)
        print(text)


# 画像ファイルのパスを指定
image_path = r"C:\Users\USER\Pictures\Screenshots\test_number2.png"
recognize_text(image_path)

# 가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주아바사자하허호배
