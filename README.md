# 번호판 인식 모델 학습
  
- [TRDG2DTRB](https://github.com/ohiayame/Parking_control_system_TRDG2DTRB) : deep-text-recognition-benchmark 프로젝트에서 요구하는 데이터 구조로 변환
- [deep-text-recognition-benchmark](https://github.com/ohiayame/Parking_control_system_deep-text-recognition-benchmark) : 모델 학습
- [EasyOCR](https://github.com/ohiayame/Parking_control_system_EasyOCR) : 데이터 수집 및 모델 성능 확인
## 1. 번호판 데이터 수집
### 1. [AI-Hub](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=172) : 실제 자동차 번호판 데이터 (80,000장)
**파일명 구조** :
  - 00가0000.jpg
  - 000가0000.jpg
  - 같은 번호의 데이터가 여러 개 있는 경우 **-2, -3** 등 뒤에 붙이고 분류\
- [TRDG2DTRB](https://github.com/ohiayame/Parking_control_system_TRDG2DTRB)의 Modify_File_Name.py로 output의 구조로 변환
```
/input
├── 12가3456.jpg
├── 234나5678.jpg
├── 234나5678-2.jpg
└── ...
```
```
/output
#   [gt]_[idx].[ext]
├── 12가3456_00001.jpg
├── 234나5678_00002.jpg
├── 234나5678_00003.jpg
└── ...
```
- 7 : 1.5 : 1.5 비율로 나눈 경우
  - **Training** : 약 70% → 38,575장
  - **Validation** : 약 15% → 8,266장
  - **Test** : 약 15% → 8,264장
### 2. 모형 데이터
**데이터 수집 방법** 
- [EasyOCR](https://github.com/ohiayame/Parking_control_system_EasyOCR) 의 	<ins> 촬영.py	 </ins>로 deep-text-recognition-benchmark 프로젝트에서 요구하는 데이터 구조에 맞춰서 이미지를 저장
  - 숫자 4개의 번호판 데이터 -> NumData
  - ~~한글이 있는 번호판 데이터 -> NumKo~~
    
## 2. 데이터셋 생성
### 1. [TRDG2DTRB](https://github.com/ohiayame/Parking_control_system_TRDG2DTRB)로 한 폴더에 images폴더와 gt.txt파일을 생성
```
/input
#   [gt]_[idx].[ext]
├── 12가3456_00001.jpg
├── 234나5678_00002.jpg
├── 234나5678_00003.jpg
└── ...
```
```
/output
├── gt.txt
|   ├── images/image_00001.jpg   12가3456
|   ├── images/image_00002.jpg   234나5678
|   ├── images/image_00003.jpg   234나5678
|   └── ...
|
└── images
    ├── image_00001.jpg
    ├── image_00002.jpg
    ├── image_00003.jpg
    └── ...
```
**Train:**     
```
python TRDG2DTRB\convert.py --input_path (이미지 데이터 폴더 경로) --output_path ( 주소 / training or validation)

```
 - 스스로 구현한 기능
   
   **convert_datast** :  validation와 test의 저장 수와 경로를 지정하고 output_path주소를 training폴더로 설정해 실행하면 3폴더로 나눠서 저장 됨

### 2. 데이터를 lmdb 포맷으로 변환 (data.mdb, lock.mdb 파일생성)
- 1 에서 생성한 폴더(images폴더, gt.txt)를 lmdb 포맷으로 변환
- [deep-text-recognition-benchmark](https://github.com/ohiayame/Parking_control_system_deep-text-recognition-benchmark)에 lmdb폴더를 생성해 create_lmdb_dataset.py를 실행
```
deep-text-recognition-benchmark
└── lmdb    
    ├── training
    |      └── MyDataset
    |             ├── data.mdb
    |             └── lock.mdb
    └── validation
          ├── data.mdb
          └── lock.mdb
```
**Train:**     
```
    python create_lmdb_dataset.py  --inputPath C:/Users/USER/ 주소 /(training or validation) --gtFile C:/Users/USER/ 주소 /(training or validation) /gt.txt  --outputPath C:/Users/USER/ 주소 /deep-text-recognition-benchmark/lmdb/(training/MyDataset or validation) 
```

 
    
## 학습 모델
### 1_onlyNum
  - 모형 숫자 번호판 (NumData)
    - training 2,223장
    - validation 806장
    - num_iter 10,000
      
  **Train:**
```
 python train.py --train_data lmdb/training  --valid_data lmdb/validation   --select_data MyDataset  --batch_ratio 1.0 --Transformation None   --FeatureExtraction VGG  --SequenceModeling BiLSTM   --Prediction CTC  --FT   --workers 0   --lr 0.0001  --adam --num_class 10 --rgb
```

### 2_NumKo
  - 모형 한글 번호판 (NumKo)
    - ~~Training set: 26종류의 번호판 × 30장 = 총 **780장**~~
    - ~~Validation set: 8종류의 번호판 × 30장 = 총 **240장**~~
    - training 3종류 90장
    - validation 1종류 30장
    - num_iter 500
      
  **Train:**
```
 python train.py --train_data lmdb/training  --valid_data lmdb/validation   --select_data MyDataset   --batch_ratio 1.0 --Transformation None   --FeatureExtraction VGG  --SequenceModeling BiLSTM   --Prediction CTC  --FT   --workers 0   --lr 0.0001  --adam --num_class 10
```

### 3_NumAnd
  - 실제 번호판과 모형 숫자 번호판 Mix (NumAnd)
    - training 13,269장
    - validation 4,440장
    - num_iter 300,000
    
  **Train:**
```
 python train.py --train_data lmdb/training  --valid_data lmdb/validation   --select_data MyDataset  --batch_ratio 1.0 --Transformation None   --FeatureExtraction VGG  --SequenceModeling BiLSTM   --Prediction CTC  --FT   --workers 0   --lr 0.0001  --adam --num_class 10 --rgb
```
### 4_Num과적합
 - 모형 숫자 번호판, 실제 사용하는 rccar와 상환에서 촬영
 - 다른 모델과 비교하기 위해 과적합 실험
   - training 7종 210장
   - num_iter 300
   - validation을 training데이터셋과 동일하게 설정하여 실행
     
     
### 5_NumCar
  - AI-Hub 데이터
    - training 38,575장
    - validation 8,266장
    - num_iter 100,000
    - character 가거고구나노더도두라러마머모배버보부사서소아어오우자저조주하허호울경기강원충남북전제대광산세종인천
    
  **Train:**
 ```
 python train.py --train_data lmdb/training  --valid_data lmdb/validation   --select_data MyDataset  --batch_ratio 1.0 --Transformation None   --FeatureExtraction VGG  --SequenceModeling BiLSTM   --Prediction CTC  --FT   --workers 0   --lr 0.0001  --adam --num_class 10 --rgb
```
