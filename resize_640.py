import os
import cv2
import numpy as np

input_folder = '/home/ivis/yolov9/data/valid/images/'  # 이미지 폴더 경로
output_folder = '/home/ivis/yolov9/data/valid/resized_images/'  # 저장 폴더 (없으면 자동 생성)
target_size = 640

# 저장 폴더 없으면 생성
os.makedirs(output_folder, exist_ok=True)

# 지원하는 확장자
valid_exts = ['.jpg', '.jpeg', '.png', '.bmp']

for filename in os.listdir(input_folder):
    name, ext = os.path.splitext(filename)
    if ext.lower() not in valid_exts:
        continue

    img_path = os.path.join(input_folder, filename)
    img = cv2.imread(img_path)

    if img is None:
        print(f"이미지 로드 실패: {filename}")
        continue

    h, w = img.shape[:2]

    if h == target_size and w == target_size:
        # 크기 이미 맞는 경우 복사만
        cv2.imwrite(os.path.join(output_folder, filename), img)
        continue

    # 검정색 배경 생성
    padded_img = np.zeros((target_size, target_size, 3), dtype=np.uint8)

    # 중앙 정렬을 위한 시작점 계산
    x_offset = (target_size - w) // 2
    y_offset = (target_size - h) // 2

    # 이미지가 타겟보다 클 경우, 크기 조정
    if w > target_size or h > target_size:
        scale = min(target_size / w, target_size / h)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
        h, w = img.shape[:2]
        x_offset = (target_size - w) // 2
        y_offset = (target_size - h) // 2

    # 이미지 삽입
    padded_img[y_offset:y_offset+h, x_offset:x_offset+w] = img

    # 저장
    cv2.imwrite(os.path.join(output_folder, filename), padded_img)

print("모든 이미지 패딩 완료.")
