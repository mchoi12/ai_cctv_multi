import cv2
import os
import time
import pandas as pd
import numpy as np

from core.detector import Detector
from core.event_engine import detect_event
from core.vlm_agent import generate_description

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VIDEO_PATHS = [
    os.path.join(BASE_DIR, "videos", "cam1.mp4"),
    os.path.join(BASE_DIR, "videos", "cam2.mp4"),
    os.path.join(BASE_DIR, "videos", "cam3.mp4"),
    os.path.join(BASE_DIR, "videos", "cam4.mp4"),
    os.path.join(BASE_DIR, "videos", "cam5.mp4"),
    os.path.join(BASE_DIR, "videos", "cam6.mp4"),
]

TARGET_SIZE = (640, 360)

# 폴더 생성
capture_dir = os.path.join(BASE_DIR, "output", "captures")
current_dir = os.path.join(BASE_DIR, "output", "current")

os.makedirs(capture_dir, exist_ok=True)
os.makedirs(current_dir, exist_ok=True)

csv_path = os.path.join(BASE_DIR, "output", "events.csv")

# CSV 초기 생성
if not os.path.exists(csv_path):
    pd.DataFrame(columns=[
        "time","camera","event","severity","persons","image","description"
    ]).to_csv(csv_path, index=False)

detector = Detector("models/yolo11n.pt")

# VideoCapture 안정화
caps = []
for v in VIDEO_PATHS:
    cap = cv2.VideoCapture(v)
    if not cap.isOpened():
        print(f"[ERROR] 영상 열기 실패: {v}")
    caps.append(cap)

events = []
MAX_EVENTS = 1000  # 메모리 보호

last_event_time = {}
last_save_time = 0

print("AI CCTV 시작")

# =========================
# 메인 루프
# =========================
while True:

    frames = []

    for i, cap in enumerate(caps):
        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        if not ret:
            frame = None

        frames.append(frame)

    processed = []

    for idx, frame in enumerate(frames):

        # frame 방어
        if frame is None or frame.size == 0:
            frame = np.zeros((360, 640, 3), dtype=np.uint8)
            cv2.putText(frame, f"CAM{idx} NO SIGNAL", (50,180),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        else:
            frame = cv2.resize(frame, TARGET_SIZE)

        persons, results = detector.detect(frame)

        for (x1, y1, x2, y2) in persons:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

        person_count = len(persons)
        event, severity = detect_event(person_count)

        now = time.time()

        # =========================
        # 이벤트 발생
        # =========================
        if event != "normal":
            last_time = last_event_time.get(idx, 0)

            if now - last_time > 3:
                last_event_time[idx] = now

                timestamp = time.strftime("%Y%m%d_%H%M%S")

                img_path = os.path.join(
                    capture_dir, f"cam{idx}_{timestamp}.jpg"
                )

                # 캡처 저장 (안정)
                ret_img = cv2.imwrite(img_path, frame)
                if not ret_img:
                    print(f"[ERROR] 캡처 저장 실패 CAM{idx}")

                desc = generate_description(event, person_count)

                print(f"CAM{idx} | {desc}")

                event_data = {
                    "time": timestamp,
                    "camera": idx,
                    "event": event,
                    "severity": severity,
                    "persons": person_count,
                    "image": img_path,
                    "description": desc
                }

                events.append(event_data)

                # 메모리 보호
                if len(events) > MAX_EVENTS:
                    events = events[-MAX_EVENTS:]

                # CSV 저장
                df = pd.DataFrame(events)
                df.to_csv(csv_path, index=False)

                cv2.putText(frame, "EVENT", (10,30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        cv2.putText(frame, f"CAM{idx}", (10,350),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        # 현재 프레임 저장 (완전 안정 방식)
        timestamp_ms = int(time.time() * 1000)
        current_path = os.path.join(current_dir, f"cam{idx}_{timestamp_ms}.jpg")

        ret_cur = cv2.imwrite(current_path, frame)
        if not ret_cur:
            print(f"[ERROR] 현재프레임 저장 실패 CAM{idx}")

        processed.append(frame)

    # GRID 표시
    if len(processed) == 6:
        row1 = cv2.hconcat(processed[:3])
        row2 = cv2.hconcat(processed[3:])
        grid = cv2.vconcat([row1, row2])
        cv2.imshow("AI CCTV", grid)

    # 오래된 파일 삭제 (중요)
    for i in range(6):
        files = sorted(
            [f for f in os.listdir(current_dir) if f.startswith(f"cam{i}_")],
            key=lambda x: os.path.getctime(os.path.join(current_dir, x))
        )
        if len(files) > 30:
            for f in files[:-30]:
                try:
                    os.remove(os.path.join(current_dir, f))
                except:
                    pass

    time.sleep(0.03)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
print("종료")