import imageio
import os

video_path = '/home/ivis/Data_video/elevator/20240711_133516_merged.avi'

# 추출된 프레임이 저장될 경로
output_folder = '/home/ivis/Data_video/elevator/extracted_framse'

# 프레임 저장 간격 설정 (1은 모든 프레임, 10은 10프레임마다 한 장씩)
frame_interval = 1

def extract_frames(video_file_path, output_dir, interval=1):
    # 출력 폴더가 존재하지 않으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"폴더 생성: '{output_dir}'")

    try:
        # 비디오 파일 읽기
        reader = imageio.get_reader(video_file_path)
    except FileNotFoundError:
        print(f"오류: 비디오 파일을 찾을 수 없음- '{video_file_path}'")
        return
    except Exception as e:
        print(f"오류: 비디오 파일을 읽는 중 문제 발생- {e}")
        return

    saved_frame_count = 0
    total_frame_processed = 0

    print(f"비디오 파일 처리 시작: '{video_file_path}'")
    print(f"프레임 저장 간격: {interval} 프레임마다")

    for i, frame_data in enumerate(reader):
        total_frame_processed += 1
        if i % interval == 0:
            # 저장할 파일 이름 생성 (예: frame_0000.jpg, frame_0010.jpg 등)
            frame_filename = os.path.join(output_dir, f'frame_{i:06d}.jpg') # 6자리 숫자로 포맷팅
            try:
                # imageio로 읽은 frame은 numpy array이므로, imageio.imwrite로 저장
                imageio.imwrite(frame_filename, frame_data)
                saved_frame_count += 1
                if saved_frame_count % 100 == 0: # 100장 저장할 때마다 로그 출력
                    print(f"{saved_frame_count}개의 프레임 저장 완료")
            except Exception as e:
                print(f"오류: 프레임 저장 중 문제 발생 ({frame_filename}): {e}")
    
    reader.close()

    print(f"  총 처리된 프레임 수: {total_frame_processed}")
    print(f"  총 저장된 프레임 수: {saved_frame_count}")
    print(f"  프레임 저장 폴더: '{os.path.abspath(output_dir)}'") 

if __name__ == '__main__':
    if video_path == '/path/to/your/video_file.mp4' or not video_path:
        print("주의: 'video_path' 변수에 실제 비디오 파일 경로를 설정해주세요.")
    else:
        extract_frames(video_path, output_folder, frame_interval)

