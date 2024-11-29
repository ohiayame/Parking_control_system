import os
from PIL import Image

def resize_image_with_padding(image_path, target_width, target_height):
    # 이미지 열기
    img = Image.open(image_path)
    
    # 원본 이미지 크기
    width, height = img.size
    
    # 비율 유지하며 이미지 리사이즈
    img.thumbnail((target_width, target_height))
    
    # 새로운 이미지 크기 계산
    new_width, new_height = img.size
    
    # 배경을 검은색으로 채운 새로운 이미지 생성
    new_img = Image.new("RGB", (target_width, target_height), (0, 0, 0))
    
    # 리사이즈된 이미지를 중앙에 배치
    left = (target_width - new_width) // 2
    top = (target_height - new_height) // 2
    new_img.paste(img, (left, top))
    
    return new_img

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
target_width = 674
target_height = 340

for i in range(len(dataset)):
    folder_path = f'numberdata/{dataset[i]}/images'  # 원본 이미지가 있는 폴더 경로
    output_path = f'Resize/numberdata/{dataset[i]}/images'  # 리사이즈된 이미지를 저장할 폴더 경로
    
    resize_images_in_folder(folder_path, output_path, target_width, target_height)
