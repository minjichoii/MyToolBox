import os
import cv2
import numpy as np

# 배경 이미지 폴더 경로 설정
background_folder_path = "backgraound/image/path"
output_folder_path = "new/image/path"  # 리사이즈 및 패딩된 이미지 저장 경로
label_output_folder_path = "new/label/path"  # 라벨 파일 저장 경로

# 출력 폴더가 없으면 생성
os.makedirs(output_folder_path, exist_ok=True)
os.makedirs(label_output_folder_path, exist_ok=True)

# 배경 이미지를 640x640으로 패딩하고 검정화면이 아닌 부분을 라벨링
image_files = sorted([f for f in os.listdir(background_folder_path) if f.endswith(('.jpg', '.png'))])
print(f"총 {len(image_files)}개의 배경 이미지를 처리합니다.")

for idx, img_file in enumerate(image_files):
    print(f"Processing image {idx + 1}/{len(image_files)}: {img_file}")
    img_path = os.path.join(background_folder_path, img_file)
    img = cv2.imread(img_path)

    if img is None:
        print(f"이미지를 읽을 수 없습니다: {img_path}")
        continue

    # 원본 이미지 크기 가져오기
    height, width, _ = img.shape

    # 640x640 크기에 맞게 패딩 추가
    top = (640 - height) // 2 if height < 640 else 0
    bottom = 640 - height - top if height < 640 else 0
    left = (640 - width) // 2 if width < 640 else 0
    right = 640 - width - left if width < 640 else 0

    padded_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    # 패딩된 이미지 저장
    output_img_path = os.path.join(output_folder_path, img_file)
    cv2.imwrite(output_img_path, padded_img)

    # 검정 화면이 아닌 부분 라벨링
    if top > 0 or left > 0:  # 패딩이 추가된 경우에만 라벨링
        x_center = (left + width / 2) / 640
        y_center = (top + height / 2) / 640
        w_norm = width / 640
        h_norm = height / 640

        # 클래스 0 (배경)으로 라벨링
        label_line = f"0 {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n"
        label_file_path = os.path.join(label_output_folder_path, os.path.splitext(img_file)[0] + ".txt")

        # 라벨 파일 저장
        with open(label_file_path, 'w') as label_file:
            label_file.write(label_line)

print("모든 배경 이미지가 패딩되고 라벨링되었습니다.")
