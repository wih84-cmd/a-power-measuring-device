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

# 💡 여기서부터 수정됨! HTML 태그들을 들여쓰기 없이 왼쪽으로 쫙 붙였습니다.
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
