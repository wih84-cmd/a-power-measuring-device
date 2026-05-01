import streamlit as st

# --- 1. 페이지 기본 설정 ---
st.set_page_config(page_title="로봇 배터리 시뮬레이터", page_icon="🤖", layout="centered")

st.title("🤖 프로보 테크닉 배터리 시뮬레이터")
st.markdown("모터 개수를 조절해서 배터리가 얼마나 빨리 닳는지 확인해 보세요!")
st.divider() # 가로줄 긋기

# --- 2. 사용자 입력 (위젯) ---
st.subheader("⚙️ 로봇 설정")
b_type = st.radio("🔋 건전지 종류:", ['AA (오래감)', 'AAA (가벼움)'], horizontal=True)

# 3개의 모터 슬라이더를 3칸으로 나누어 깔끔하게 배치
col1, col2, col3 = st.columns(3)
with col1:
    m120 = st.slider("🏎️ 120 모터 (0.4A):", min_value=0, max_value=5, value=0)
with col2:
    m300 = st.slider("🚜 300 모터 (0.8A):", min_value=0, max_value=5, value=0)
with col3:
    servo = st.slider("🦾 서보 모터 (0.2A):", min_value=0, max_value=5, value=0)

st.divider()

# --- 3. 계산하기 ---
# 건전지 용량 설정
capacity_base = 2500 if 'AA' in b_type else 1200

# 소모 전류 및 전력 계산
current = (m120 * 0.4) + (m300 * 0.8) + (servo * 0.2)
power = current * 6 # 6V 기준 전력

# 1분당 소모되는 배터리 양
drain_per_minute = (current * 1000) / 60 if current > 0 else 0

# 상태 및 애니메이션 설정
if current > 0:
    mins = (capacity_base / 1000 / current) * 60
    
    # 전류가 높을수록 애니메이션이 짧아짐(빨라짐)
    anim_duration = 3.0 / current 
    animation_style = f"animation: drainAnim {anim_duration}s infinite linear;"
    status = f"배터리가 1분에 <b style='color:#e91e63;'>{drain_per_minute:.1f} mAh</b>씩 닳고 있어요!"
else:
    mins = 0
    animation_style = "width: 100%; background-color: #4CAF50;"
    status = "모터가 멈춰 있어서 배터리가 닳지 않습니다."

# --- 4. 시각적 HTML 및 CSS 애니메이션 화면에 그리기 ---
html_str = f"""
<style>
    @keyframes drainAnim {{
        0%   {{ width: 100%; background-color: #4CAF50; }}  /* 초록색 */
        50%  {{ background-color: #ffeb3b; }}             /* 노란색 */
        100% {{ width: 0%; background-color: #f44336; }}    /* 빨간색 */
    }}
</style>

<div style="border: 3px solid #555; padding: 20px; border-radius: 15px; background-color: #f9f9f9; font-family: sans-serif; max-width: 500px; margin: auto;">
    <h3 style="margin-top: 0;">⚡ 실시간 배터리 소모 속도</h3>
    
    <div style="display: flex; align-items: center; margin-bottom: 15px;">
        <div style="flex-grow: 1; height: 40px; border: 4px solid #333; border-radius: 8px; padding: 2px; background-color: #ddd;">
            <div style="height: 100%; border-radius: 4px; {animation_style}"></div>
        </div>
        <div style="width: 10px; height: 20px; background-color: #333; border-radius: 0 4px 4px 0;"></div>
    </div>
    
    <p style="font-size: 16px;">{status}</p>
    <p style="font-size: 14px; color: #666;">- 현재 전력: <b>{power:.1f} W</b> / 전류: <b>{current:.2f} A</b></p>
    <h3 style="color: #e91e63;">⏳ 예상 수명: 약 {mins:.1f} 분</h3>
</div>
"""

# HTML을 Streamlit 화면에 렌더링 (unsafe_allow_html=True 필수)
st.markdown(html_str, unsafe_allow_html=True)
