import pytesseract
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from matplotlib import pyplot as plt
import re
# Tesseractの実行ファイルのパスを指定
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = r"c:\Users\USER\Pictures\KakaoTalk_20240906_153151441.jpg"
image = Image.open(image_path)

# 言語コード 認識
custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789'
text = pytesseract.image_to_string(image, lang='eng', config=custom_config)
# clean_text = re.sub(r'[^\w\s]', '', text)
print(text)