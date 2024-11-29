import os
from PIL import Image
def cheksize(folder_path):
    max_width = 0
    max_height = 0 

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        img = Image.open(file_path)
        
        width, height = img.size
        
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height
    return  max_width, max_height


dataset = ["training", "validation", "test"]

for i in range(len(dataset)):
    folder_path = f'numberdata/{dataset[i]}/images'  # 원본 이미지가 있는 폴더 경로
    max_width, max_height = cheksize(folder_path)
        
    print(f"{dataset[i]} : {max_width}, {max_height}")
