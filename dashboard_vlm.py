import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit_autorefresh import st_autorefresh
from PIL import Image

EVENTS_CSV = Path("./events_vlm.csv")
CAMERA_IMAGES = Path("./events/")  # 최신 CCTV 이미지

st_autorefresh(interval=5000, key="refresh")  # 5초 갱신

st.title("VLM 기반 AI CCTV 관제")

# 이벤트 로그
df = pd.read_csv(EVENTS_CSV)
st.subheader("이벤트 리스트")
selected = st.selectbox("선택 이벤트", df.index, format_func=lambda x: f"{df.loc[x,'timestamp']} | {df.loc[x,'camera_id']} | {df.loc[x,'event_type']}")

if selected is not None:
    event = df.loc[selected]
    st.write("설명:", event['description'])
    st.image(Image.open(event['image_path']), caption=f"{event['camera_id']} 이벤트 이미지")

# 통계
st.subheader("통계")
st.bar_chart(df['event_type'].value_counts())