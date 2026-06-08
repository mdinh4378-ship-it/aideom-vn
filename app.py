import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout=wide, page_title=AIDEOM-VN Dashboard)
st.sidebar.header(AIDEOM-VN Dashboard)

menu = st.sidebar.radio(Danh mục 12 Bài, [
    Bài 1: Macro, Bài 2: LP, Bài 3: MIP, Bài 4: MOO, 
    Bài 5: Stochastic 1, Bài 6: DP, Bài 7: RL, Bài 8: CGE, 
    Bài 9: Spatial, Bài 10: Stochastic 2, Bài 11: DQN, Bài 12: Tổng hợp
])

if menu == Bài 1: Macro:
    st.title(Bài 1: Hàm sản xuất Cobb-Douglas)
    col1, col2 = st.columns([1, 3])
    with col1:
        alpha = st.slider(Vốn, 0.0, 1.0, 0.33)
        beta = st.slider(Lao động, 0.0, 1.0, 0.42)
    with col2:
        years = [2020, 2021, 2022, 2023, 2024, 2025]
        y_real = [8044.4, 8487.5, 9513.3, 10221.8, 11511.9, 12847.6]
        fig = go.Figure(go.Scatter(x=years, y=y_real, mode=lines+markers, name=GDP))
        st.plotly_chart(fig, use_container_width=True)

elif menu == Bài 2: LP:
    st.title(Bài 2: Phân bổ Ngân sách Tuyến tính)
    budget = st.slider(Ngân sách, 50, 150, 100)
    data = pd.DataFrame({Hạng mục: [Hạ tầng, AI, Nhân lực, R&D], Phân bổ: [25, 15, 30, budget-70]})
    st.bar_chart(data.set_index(Hạng mục))

elif menu == Bài 3: MIP:
    st.title(Bài 3: Lựa chọn Dự án)
    budget = st.slider(Ngân sách MIP, 30, 150, 80)
    st.write(Các dự án được chọn dựa trên thuật toán Knapsack.)
    projects = {TT Dữ liệu: 30, Nền tảng AI: 20, Kỹ sư AI: 15, Y tế: 25}
    for k, v in projects.items():
        if budget >= v:
            st.success(f"Chọn: {k} (Phí: {v})")
            budget -= v

elif menu == Bài 4: MOO:
    st.title(Bài 4: Tối ưu Đa mục tiêu)
    max_co2 = st.slider(Hạn ngạch CO2, -20, 80, 30)
    co2 = np.arange(-20, 85, 5)
    gdp = 40 + np.sqrt(np.clip((co2 + 20), 0, None)) * 5
    fig = px.line(x=co2, y=gdp, labels={x: CO2, y: GDP})
    fig.add_vline(x=max_co2, line_dash=dash, line_color=red)
    st.plotly_chart(fig, use_container_width=True)

elif menu == Bài 5: Stochastic 1:
    st.title(Bài 5: Tối ưu Ngẫu nhiên Cơ bản)
    x = st.slider(Đầu tư máy chủ GĐ1, 0, 2500, 1000)
    st.metric(Chi phí dự kiến, f"{x*10 + max(0, 1000-x)*25} Tỷ")
    
elif menu == Bài 6: DP:
    st.title(Bài 6: Tối ưu Động)
    inv = st.slider(Đầu tư hàng năm, 10, 50, 20)
    k = 100
    k_vals = []
    for _ in range(5):
        k_vals.append(k)
        k = k*0.9 + inv
    st.bar_chart(pd.DataFrame({Năm: range(2026, 2031), Vốn: k_vals}).set_index(Năm))

elif menu == Bài 7: RL:
    st.title(Bài 7: Học tăng cường)
    st.write(Q-Values mô phỏng sau quá trình huấn luyện.)
    st.bar_chart(pd.DataFrame({Lớp: [Phổ thông, Bậc trung, Cao cấp], Q: [5.2, 1.1, -0.5]}).set_index(Lớp))

elif menu == Bài 8: CGE:
    st.title(Bài 8: Cân bằng Tổng quát)
    tax = st.slider(Thuế Carbon, 0, 60, 20)
    p = np.arange(10, 100, 10)
    d = 120 - p
    s = 20 + 1.5 * (p - tax)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=p, y=d, name=Cầu))
    fig.add_trace(go.Scatter(x=p, y=s, name=Cung))
    st.plotly_chart(fig, use_container_width=True)

elif menu == Bài 9: Spatial:
    st.title(Bài 9: Kinh tế Không gian)
    cost = st.slider(Phí vận chuyển, 0.01, 0.1, 0.05)
    d = np.arange(0, 350, 50)
    e = 1000 * 1.5 * np.exp(-cost * d)
    st.area_chart(pd.DataFrame({Khoảng cách: d, Mật độ: e}).set_index(Khoảng cách))

elif menu == Bài 10: Stochastic 2:
    st.title(Bài 10: Giá trị VSS)
    prob = st.slider(Xác suất Khủng hoảng, 0.0, 0.8, 0.2)
    ev = (80*1.5 + 20*0.8)*(1-prob) + (80*0.2 + 20*2.0)*prob
    sp = (40*1.5 + 60*0.8)*(1-prob) + (40*0.2 + 60*2.0)*prob
    st.metric(Chỉ số VSS, round(sp - ev, 2))
    st.bar_chart(pd.DataFrame({Mô hình: [EV, SP], Lợi nhuận: [ev, sp]}).set_index(Mô hình))

elif menu == Bài 11: DQN:
    st.title(Bài 11: Deep Q-Network)
    ep = np.arange(0, 1000, 50)
    reward = 100 - 80 * np.exp(-0.005 * ep)
    st.line_chart(pd.DataFrame({Epoch: ep, Reward: reward}).set_index(Epoch))

elif menu == Bài 12: Tổng hợp:
    st.title(Bài 12: Đồ án Tổng hợp)
    scen = st.selectbox(Kịch bản, [S1: Cơ sở, S4: Tối ưu])
    col1, col2, col3 = st.columns(3)
    if scen == S1: Cơ sở:
        col1.metric(GDP, 12.5)
        col2.metric(CO2, 80)
        col3.metric(Ngân sách, 100)
    else:
        col1.metric(GDP, 15.5, 3.0)
        col2.metric(CO2, 20, -60)
        col3.metric(Ngân sách, 110, 10)
    
    df = pd.DataFrame(dict(
        r=[85, 90, 85, 85, 95] if scen == S4: Tối ưu else [70, 60, 65, 50, 60],
        theta=[Kinh tế, Công nghệ, Vùng miền, Môi trường, Nhân lực]))
    fig = px.line_polar(df, r=r, theta=theta, line_close=True)
    fig.update_traces(fill=toself)
    st.plotly_chart(fig, use_container_width=True)
