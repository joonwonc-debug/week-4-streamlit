import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# 1. 페이지 설정
st.set_page_config(page_title="NoiseTouch Poster", layout="centered")

# 2. 헬퍼 함수들 (기존 로직 유지)
def random_palette(k=7):
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

def blob(center=(0.5, 0.5), r=0.3, points=180, wobble=0.08):
    angles = np.linspace(0, 2*math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# 3. 세션 상태 관리 (팔레트 유지용)
if 'palette' not in st.session_state:
    st.session_state.palette = random_palette()

# "새로운 팔레트/리셋" 버튼 기능
def reset_palette():
    st.session_state.palette = random_palette()

# 4. 사이드바 UI 구성 (Matplotlib Slider 대체)
st.sidebar.header("Controls")
n_layers = st.sidebar.slider("Layers", min_value=1, max_value=30, value=12, step=1)
wobble_val = st.sidebar.slider("Wobble Intensity", min_value=0.05, max_value=0.5, value=0.25)

if st.sidebar.button("Regenerate Art"):
    reset_palette()

# 5. 메인 그리기 함수
def draw_poster_streamlit(n_layers, wobble_val, palette):
    # Streamlit에서는 매번 새로운 Figure를 생성해야 합니다.
    fig, ax = plt.subplots(figsize=(7, 10))
    fig.patch.set_facecolor((0.98, 0.98, 0.97))
    ax.set_facecolor((0.98, 0.98, 0.97))
    ax.axis('off')

    # 레이어 그리기
    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        # Wobble range를 슬라이더 값 기준으로 설정
        wobble = random.uniform(wobble_val - 0.05, wobble_val + 0.05)
        
        x, y = blob(center=(cx, cy), r=rr, wobble=wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.3, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    # 텍스트 추가
    ax.text(0.05, 0.95, "NoiseTouch Generative Poster", fontsize=16, weight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.91, "Week 4 • Arts & Advanced Big Data", fontsize=10, transform=ax.transAxes)
    
    return fig

# 6. 화면 출력
st.title("NoiseTouch Generative Poster")
st.markdown("슬라이더를 조절하거나 버튼을 눌러 새로운 아트를 생성해보세요.")

# 그림 생성 및 출력
fig = draw_poster_streamlit(n_layers, wobble_val, st.session_state.palette)
st.pyplot(fig)
