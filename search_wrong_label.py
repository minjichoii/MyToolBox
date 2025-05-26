import os

def find_files_with_other_labels(folder_path):
    """
    지정된 폴더 내의 모든 라벨 파일을 검사하여,
    파일 내용 중 라벨(클래스 번호, 각 줄의 첫 번째 숫자)이
    0 또는 3이 아닌 경우가 하나라도 포함된 파일들의 이름을 리스트로 반환합니다.
    """
    files_with_other_labels = []

    # 1. 입력된 폴더 경로가 실제로 존재하는지 확인
    if not os.path.exists(folder_path):
        print(f"오류: 폴더를 찾을 수 없습니다 - {folder_path}")
        return files_with_other_labels # 빈 리스트 반환
    
    if not os.path.isdir(folder_path):
        print(f"오류: 다음 경로는 폴더가 아닙니다 - {folder_path}")
        return files_with_other_labels # 빈 리스트 반환

    # 2. 폴더 내 모든 파일에 대해 처리
    print(f"'{folder_path}' 폴더를 검사 중입니다...")
    processed_files_count = 0
    found_target_files_count = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 파일이고, 확장자가 .txt인 경우 (일반적인 YOLO 라벨 파일 형식)
        if os.path.isfile(file_path) and filename.lower().endswith('.txt'):
            processed_files_count += 1
            try:
                with open(file_path, 'r', encoding='utf-8') as f: # 인코딩 명시
                    lines = f.readlines()
                
                found_other_label_in_file = False # 현재 파일에서 다른 라벨을 찾았는지 여부
                for line_number, line in enumerate(lines, 1): # 줄 번호도 함께 확인 (디버깅용)
                    parts = line.strip().split()
                    if parts: # 빈 줄이 아닌 경우에만 처리
                        label_class = parts[0]
                        # 첫 번째 부분이 숫자인지, 그리고 0 또는 3이 아닌지 확인
                        if label_class.isdigit() and label_class not in ['0', '1']:
                            files_with_other_labels.append(filename)
                            found_target_files_count +=1
                            # print(f"  -> 파일 '{filename}'의 {line_number}번째 줄에서 라벨 '{label_class}' 발견.")
                            found_other_label_in_file = True
                            break # 해당 파일에서 이미 찾았으므로 다음 파일로 넘어감
                
            except Exception as e:
                print(f"파일 처리 중 오류 발생 ({filename}): {e}")
                
    print(f"총 {processed_files_count}개의 .txt 파일을 검사했습니다.")
    return files_with_other_labels

# --- ★★★★★ 사용자 설정 부분 ★★★★★ ---
# 라벨 파일들이 있는 폴더 경로를 아래 변수에 직접 할당하세요.
# Linux/macOS 예시:
label_folder_path = '/home/ivis/yolov9/data/valid/labels' 
# Windows 예시:
# label_folder_path = r'C:\Users\YourUser\Desktop\my_dataset\labels' # Windows 경로는 r'' 또는 '\\' 사용

# --- 실행 부분 ---
if label_folder_path: # 변수에 경로가 할당되었는지 확인
    result_files = find_files_with_other_labels(label_folder_path)

    if result_files:
        print(f"\n총 {len(result_files)}개의 파일에서 라벨이 0 또는 1이 아닌 경우가 발견되었습니다:")
        for fname in result_files:
            print(fname)
    elif os.path.exists(label_folder_path) and os.path.isdir(label_folder_path): # 폴더는 존재하지만 해당 파일이 없는 경우
        print(f"\n'{label_folder_path}' 폴더 내에 라벨이 0 또는 3이 아닌 파일을 찾지 못했습니다.")
    # 폴더가 존재하지 않거나 폴더가 아닌 경우는 find_files_with_other_labels 함수 내에서 이미 메시지 출력됨

else:
    print("오류: 'label_folder_path' 변수에 폴더 경로가 설정되지 않았습니다. 코드를 수정해주세요.")

