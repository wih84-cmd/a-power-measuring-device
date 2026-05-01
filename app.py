import streamlit as st
from abc import ABC, abstractmethod

# --- 1. 인터페이스 설계 (규칙 만들기) ---
class PowerConsumer(ABC):
    @abstractmethod
    def get_name(self) -> str:
        """부품의 이름을 반환해야 합니다."""
        pass

    @abstractmethod
    def get_current(self) -> float:
        """현재 소모하는 전류(A)를 계산해서 반환해야 합니다."""
        pass

# --- 2. 인터페이스를 구현한 클래스들 ---
class Motor120(PowerConsumer):
    def __init__(self, count: int):
        self.count = count

    def get_name(self) -> str:
        return "120 모터"

    def get_current(self) -> float:
        return self.count * 0.4  # 1개당 0.4A

class Motor300(PowerConsumer):
    def __init__(self, count: int):
        self.count = count

    def get_name(self) -> str:
        return "300 모터"

    def get_current(self) -> float:
        return self.count * 0.8  # 1개당 0.8A

class ServoMotor(PowerConsumer):
    def __init__(self, count: int):
        self.count = count

    def get_name(self) -> str:
        return "서보 모터"

    def get_current(self) -> float:
        return self.count * 0.2  # 1개당 0.2A

# --- 3. 화면 UI 및 메인 로직 ---
st.set_page_config(page_title="로봇 배터리 시뮬레이터", page_icon="🤖", layout="centered")
st.title("🤖 프로보 테크닉 배터리 시뮬레이터 (OOP 버전)")
st.markdown("객체지향 설계(인터페이스)를 적용하여 구조를 개선했습니다.")
st.divider()

st.subheader("⚙️ 로봇 설정")
b_type = st.radio("🔋 건전지 종류:", ['AA (오래감)', 'AAA (가벼움)'], horizontal=True)

col1, col2, col3 = st.columns(3)
with col1:
    count_120 = st.slider("🏎️ 120 모터:", min_value=0, max_value=5, value=0)
with col2:
    count_300 = st.slider("🚜 300 모터:", min_value=0, max_value=5, value=0)
with col3:
    count_servo = st.slider("🦾 서보 모터:", min_value=0, max_value=5, value=0)

st.divider()

# --- 4. 다형성(Polymorphism)을 활용한 계산 ---
parts = [
    Motor120(count_120),
    Motor300(count_300),
    ServoMotor(count_servo)
]

total_current = sum(part.get_current() for part in parts)
total_power = total_current * 6  # 6V 기준 전력

# --- 5. 결과 계산 및 애니메이션 출력 ---
capacity_base = 2500 if 'AA' in b_type else 1200
drain_per_minute = (total_current * 1000) / 60 if total_current > 0 else 0

if total_current > 0:
    mins = (capacity_base / 1000 / total_current) * 60
    anim_duration = 3.0 / total_current 
    animation_style = f"animation: drainAnim {anim_duration}s infinite linear;"
    status = f"배터리가 1분에 <b style='color:#e91e63;'>{drain_per_minute:.1f} mAh</b>씩 닳고 있어요!"
else:
    mins = 0
    animation_style = "width: 100%; background-color: #4CAF50;"
    status = "모터가 멈춰 있어서 배터리가 닳지 않습니다."

html_str = f"""
<style>
    @keyframes drainAnim {{
        0%   {{ width: 100%; background-color: #4CAF50; }}  
        50%  {{ background-color: #ffeb3b; }}             
        100% {{ width: 0%; background-color: #f44336; }}    
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
    <p style="font-size: 14px; color: #666;">- 현재 전력: <b>{total_power:.1f} W</b> / 전류: <b>{total_current:.2f} A</b></p>
    <h3 style="color: #e91e63;">⏳ 예상 수명: 약 {mins:.1f} 분</h3>
</div>
"""

st.markdown(html_str, unsafe_allow_html=True)
