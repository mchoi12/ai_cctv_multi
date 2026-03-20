import cv2
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# =========================
# 🔹 core 폴더 import 경로 추가
# =========================
BASE_DIR = Path(__file__).parent
CORE_DIR = BASE_DIR / "core"
sys.path.append(str(CORE_DIR))

from vlm_model import analyze_image

# =========================
# 🔹 출력 경로 설정 (요청 반영)
# =========================
OUTPUT_DIR = BASE_DIR / "output"
EVENTS_CSV = OUTPUT_DIR / "events_vlm.csv"
EVENT_IMAGES_DIR = OUTPUT_DIR / "events"

# 폴더 생성
OUTPUT_DIR.mkdir(exist_ok=True)
EVENT_IMAGES_DIR.mkdir(exist_ok=True)

# =========================
# 기본 설정
# =========================
# CAMERAS = ["cam1.mp4","cam2.mp4","cam3.mp4","cam4.mp4","cam5.mp4","cam6.mp4"]
BASE_DIR = Path(__file__).parent

# 영상 폴더
VIDEO_DIR = BASE_DIR / "videos"

CAMERAS = [
    VIDEO_DIR / "cam1.mp4",
    VIDEO_DIR / "cam2.mp4",
    VIDEO_DIR / "cam3.mp4",
    VIDEO_DIR / "cam4.mp4",
    VIDEO_DIR / "cam5.mp4",
    VIDEO_DIR / "cam6.mp4"
]

# =========================
# CSV 초기화
# =========================
if not EVENTS_CSV.exists():
    pd.DataFrame(columns=[
        "timestamp","camera_id","event_type","description","image_path"
    ]).to_csv(EVENTS_CSV, index=False)

# =========================
# 이벤트 처리
# =========================
def process_frame(frame, cam_id):
    try:
        # 🔹 VLM 분석
        result = analyze_image(frame)

        # 🔹 이벤트 판단
        event_type, description = None, None

        if result.get('people', 0) > 5:
            event_type = "overcrowd"
            description = f"{result['people']}명 감지됨"

        # 🔹 이벤트 발생 시 처리
        if event_type:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

            image_path = EVENT_IMAGES_DIR / f"{cam_id}_{timestamp}.png"
            cv2.imwrite(str(image_path), frame)

            # CSV append (동시 접근 안정화)
            new_row = pd.DataFrame([{
                "timestamp": timestamp,
                "camera_id": cam_id,
                "event_type": event_type,
                "description": description,
                "image_path": str(image_path)
            }])

            new_row.to_csv(EVENTS_CSV, mode='a', header=False, index=False)

            print(f"[EVENT] {cam_id} | {description}")

    except Exception as e:
        print(f"[ERROR] {cam_id}: {e}")

# =========================
# 메인 루프
# =========================
def main():
    caps = []

    # 🔹 카메라 열기
    for cam in CAMERAS:
        cap = cv2.VideoCapture(cam)
        if not cap.isOpened():
            print(f"[WARNING] {cam} 열기 실패")
        caps.append(cap)

    print("VLM CCTV 엔진 시작")
    print(f"로그 경로: {EVENTS_CSV}")
    print(f"🖼 이미지 경로: {EVENT_IMAGES_DIR}")

    while True:
        for idx, cap in enumerate(caps):
            ret, frame = cap.read()

            if not ret:
                continue

            process_frame(frame, f"cam{idx+1}")

            # 🔹 CPU 과부하 방지
            cv2.waitKey(1)

# =========================
# 실행
# =========================
if __name__ == "__main__":
    main()