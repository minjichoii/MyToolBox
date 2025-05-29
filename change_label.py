import os

def change_label_in_folder(folder_path):
    # 폴더 내 모든 파일에 대해 처리
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if parts[0] == '15':
                    parts[0] = '0'
                elif parts[0] == '17':
                    parts[0] = '1'
                elif parts[0] == '16':
                    parts[0] = '2'
                new_lines.append(' '.join(parts))

            with open(file_path, 'w') as f:
                f.write('\n'.join(new_lines) + '\n')  # 마지막에 개행 추가

    return f"Processed {len(os.listdir(folder_path))} files in '{folder_path}'"


# 사용 예시
folder = '/home/ivis/yolov9/data/valid/resized_images/labels'  # 라벨 파일들이 있는 폴더 경로로 변경하세요
result = change_label_in_folder(folder)
print(result)
