import os
from PIL import Image
import cv2

def resize_image_with_padding(image_path, target_width, target_height):
    # 이미지 열기
    image = Image.open(image_path)
    
    # 원본 이미지 크기 가져오기
    old_width, old_height = image.size  # PIL에서는 size로 (너비, 높이)를 가져옵니다.

    # 비율 유지하면서 크기 조정
    ratio = min(target_width / old_width, target_height / old_height)
    new_width = int(old_width * ratio)
    new_height = int(old_height * ratio)
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # 검은색 배경의 새 이미지 생성
    new_image = Image.new("RGB", (target_width, target_height), (0, 0, 0))  # 검은색 배경
    # 리사이즈된 이미지를 중앙에 배치
    new_image.paste(resized_image, ((target_width - new_width) // 2, (target_height - new_height) // 2))

    return new_image

def resize_images_in_folder(folder_path, output_path, target_width, target_height):
    # output_path 폴더가 없으면 생성
    if not os.path.exists(output_path):
        os.makedirs(output_path)     
    
    # 폴더 내 모든 파일에 대해 작업
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # 파일이 이미지 파일인지 확인 (확장자 필터)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            resized_image = resize_image_with_padding(file_path, target_width, target_height)
            
            # 리사이즈된 이미지 저장 (원본 이름에 "_resized" 추가)
            new_file_path = os.path.join(output_path, f"{filename}")
            resized_image.save(new_file_path)
            print(f"리사이즈된 이미지 저장됨: {new_file_path}")
    

# 예시: 폴더 경로와 원하는 크기 설정
dataset = ["training", "validation", "test"]
target_width = 325
target_height = 325

for i in range(len(dataset)):
    folder_path = f'NumData/{dataset[i]}/images'  # 원본 이미지가 있는 폴더 경로
    output_path = f'Resize_Zoom/NumData/{dataset[i]}/images'  # 리사이즈된 이미지를 저장할 폴더 경로
    
    resize_images_in_folder(folder_path, output_path, target_width, target_height)
