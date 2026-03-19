import streamlit as st
import pandas as pd
import time
import os
import glob
from PIL import Image

st.set_page_config(layout="wide")

st.title("VLM기반 AI CCTV 통합 관제 시스템")

REFRESH_INTERVAL = 2

# =========================
# 최신 이미지 찾기 함수 (핵심)
# =========================
def get_latest_image(cam_idx):
    files = glob.glob(f"output/current/cam{cam_idx}_*.jpg")
    if not files:
        return None
    return max(files, key=os.path.getctime)

# =========================
# 안전 이미지 출력
# =========================
def safe_image(path):
    try:
        img = Image.open(path)
        st.image(img, use_container_width=True)
    except:
        st.warning("이미지 로딩 실패")

# =========================
# CSV 안전 로드
# =========================
def safe_read_csv(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame(columns=[
            "time","camera","event","severity","persons","image","description"
        ])

# =========================
# 1. CCTV 6채널
# =========================
st.subheader("실시간 CCTV (6채널)")

cctv_cols = st.columns(3)

for i in range(6):
    with cctv_cols[i % 3]:
        img_path = get_latest_image(i)

        if img_path:
            safe_image(img_path)
            st.caption(f"CAM{i}")
        else:
            st.warning(f"CAM{i} NO SIGNAL")

# =========================
# 2. 이벤트 로그
# =========================
st.subheader("이벤트 로그")

csv_path = "output/events.csv"

if os.path.exists(csv_path):
    df = safe_read_csv(csv_path)
else:
    df = pd.DataFrame(columns=[
        "time","camera","event","severity","persons","image","description"
    ])

if df.empty:
    st.info("현재 이벤트 없음")

    df_display = pd.DataFrame([{
        "time": "-",
        "camera": "-",
        "event": "-",
        "severity": "-",
        "persons": 0,
        "image": "",
        "description": "이벤트 없음"
    }])
else:
    df = df.sort_values(by="time", ascending=False)
    df_display = df

# =========================
# 3. 이벤트 리스트
# =========================
col1, col2 = st.columns([2,1])

with col1:
    st.dataframe(df_display, use_container_width=True)

with col2:
    selected_index = st.selectbox("이벤트 선택", df_display.index)

# =========================
# 4. 이벤트 상세
# =========================
selected = df_display.loc[selected_index]

st.subheader("이벤트 상세")

d1, d2 = st.columns([1,2])

with d1:
    if selected["image"] and os.path.exists(selected["image"]):
        safe_image(selected["image"])
    else:
        st.warning("이미지 없음")

with d2:
    st.error(f"""
시간: {selected['time']}
카메라: CAM{selected['camera']}
이벤트: {selected['event']}
인원: {selected['persons']}명

AI 분석:
{selected['description']}
""")

# =========================
# 5. 통계
# =========================
if not df.empty:
    st.subheader("이벤트 통계")

    c1, c2 = st.columns(2)

    with c1:
        st.bar_chart(df["event"].value_counts())

    with c2:
        st.bar_chart(df["camera"].value_counts())

# =========================
# 자동 새로고침
# =========================
time.sleep(REFRESH_INTERVAL)
st.rerun()