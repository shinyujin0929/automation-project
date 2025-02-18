import cv2
import os
# 저장할 디렉토리 생성
save_dir = '/home/er/ws_project3/project3_aruco/Images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
# 카메라 장치 열기 (0은 기본 카메라를 의미, 필요시 장치 번호 변경)
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()
img_count = 1
while True:
    # 카메라에서 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break
    # 현재 프레임을 창에 표시
    cv2.imshow('Camera', frame)
    # 엔터 키 입력 감지
    key = cv2.waitKey(1)
    if key == 13:  # 엔터 키의 ASCII 코드
        # 이미지 저장
        img_path = os.path.join(save_dir, f'image_{img_count}.jpg')
        cv2.imwrite(img_path, frame)
        print(f"{img_count}번째 이미지가 저장되었습니다: {img_path}")
        img_count += 1
    elif key == 27:  # ESC 키를 누르면 종료
        break
# 자원 해제
cap.release()
cv2.destroyAllWindows()
