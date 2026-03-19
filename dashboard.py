import streamlit as st
import pandas as pd
import os
import glob
from PIL import Image
from streamlit_autorefresh import st_autorefresh  # pip install streamlit-autorefresh

st.set_page_config(layout="wide")
st.title("VLM기반 AI CCTV 통합 관제 시스템")

# =========================
# 1. 자동 새로고침
# =========================
st_autorefresh(interval=2000, limit=None, key="cctv_refresh")  # 2초마다 새로고침

# =========================
# 2. 함수 정의
# =========================
def safe_read_csv(path):
    """CSV 안전 로드"""
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame(columns=[
            "time","camera","event","severity","persons","image","description"
        ])

def get_latest_image(cam_idx):
    """카메라 최신 이미지 가져오기"""
    files = glob.glob(f"output/current/cam{cam_idx}_*.jpg")
    files = [f for f in files if os.path.exists(f)]
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def safe_image(path, width="stretch"):
    """이미지 안전 출력"""
    if path and os.path.exists(path):
        img = Image.open(path)
        st.image(img, width=width)
    else:
        st.warning("이미지 없음")

# =========================
# 3. CSV 로드
# =========================
csv_path = "output/events.csv"
df = safe_read_csv(csv_path)

# =========================
# 4. CCTV 6채널
# =========================
st.subheader("실시간 CCTV (6채널)")
cols = st.columns(3)
for i in range(6):
    with cols[i % 3]:
        img_path = get_latest_image(i)
        safe_image(img_path)
        st.caption(f"CAM{i}" if img_path else f"CAM{i} NO SIGNAL")

# =========================
# 5. AI 이벤트 분석
# =========================
st.subheader("AI 이벤트 분석")
if df.empty:
    st.info("이벤트 없음")
else:
    latest_event = df.iloc[0]
    col1, col2 = st.columns([1,2])

    with col1:
        safe_image(latest_event.get("image", None))

    with col2:
        st.markdown("### AI 분석 결과")
        st.markdown(f"""
        <div style="
            background-color:#f7f7f7;
            padding:20px;
            border-radius:12px;
            border-left:6px solid #ff4b4b;
            font-size:16px;
        ">
        <b>시간:</b> {latest_event['time']}<br>
        <b>카메라:</b> CAM{latest_event['camera']}<br>
        <b>이벤트:</b> {latest_event['event']}<br>
        <b>인원:</b> {latest_event['persons']}명<br><br>
        <b>AI 설명:</b><br><br>
        {latest_event['description']}
        </div>
        """, unsafe_allow_html=True)

# =========================
# 6. 이벤트 로그
# =========================
st.subheader("이벤트 로그")
if df.empty:
    st.info("현재 이벤트 없음")
else:
    df_sorted = df.sort_values(by="time", ascending=False)
    st.dataframe(df_sorted, width="stretch")

# =========================
# 7. 통계
# =========================
st.subheader("통계 분석")
if not df.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df["event"].value_counts())
    with col2:
        st.bar_chart(df["camera"].value_counts())
else:
    st.warning("통계 데이터 없음")

# =========================
# 8. 모델 성능 분석
# =========================
st.subheader("모델 성능 분석")
if not df.empty:
    try:
        df_perf = df.copy()
        df_perf["time"] = pd.to_datetime(
            df_perf["time"], format="%Y%m%d_%H%M%S", errors="coerce"
        )
        df_perf = df_perf.dropna(subset=["time"]).sort_values(by="time")

        col1, col2 = st.columns(2)
        with col1:
            st.line_chart(df_perf.set_index("time")["persons"])
        with col2:
            event_count = df_perf.groupby("time").size()
            st.line_chart(event_count)
    except Exception as e:
        st.warning(f"성능 분석 오류: {e}")
else:
    st.warning("성능 데이터 없음")
