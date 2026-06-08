import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout='wide')
st.sidebar.header('AIDEOM-VN Dashboard')
menu = st.sidebar.radio('Danh mục', ['Bài 1: Macro', 'Bài 2: LP', 'Bài 12: Đồ án Tổng hợp'])

if menu == 'Bài 1: Macro':
    st.title('Bài 1: Hàm sản xuất Cobb-Douglas')
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader('Hệ số co giãn')
        alpha = st.slider('Vốn', 0.0, 1.0, 0.33)
        beta = st.slider('Lao động', 0.0, 1.0, 0.42)
        
    with col2:
        st.subheader('Biểu đồ Tăng trưởng')
        years = [2020, 2021, 2022, 2023, 2024, 2025]
        y_real = [8044.4, 8487.5, 9513.3, 10221.8, 11511.9, 12847.6]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=y_real, mode='lines+markers', name='GDP Thực tế'))
        st.plotly_chart(fig, use_container_width=True)

elif menu == 'Bài 2: LP':
    st.title('Bài 2: Phân bổ Ngân sách')
    budget = st.slider('Tổng ngân sách', 50, 150, 100)
    
    alloc_data = pd.DataFrame({
        'Hạng mục': ['Hạ tầng', 'AI', 'Nhân lực', 'R&D'],
        'Phân bổ': [25, 15, 30, budget - 70]
    }).set_index('Hạng mục')
    
    st.bar_chart(alloc_data)

elif menu == 'Bài 12: Đồ án Tổng hợp':
    st.title('Đồ án Tổng hợp Chính sách')
    scenario = st.selectbox('Kịch bản', ['Cơ sở', 'Tối ưu Toàn diện'])
    
    col1, col2, col3 = st.columns(3)
    if scenario == 'Cơ sở':
        col1.metric('GDP 2030', '12.5 Tr.Tỷ')
        col2.metric('Phát thải CO2', '80 MT')
        col3.metric('Khoảng cách vùng', 'Trung bình')
    else:
        col1.metric('GDP 2030', '15.5 Tr.Tỷ', 'Tăng')
        col2.metric('Phát thải CO2', '20 MT', '-60 MT')
        col3.metric('Khoảng cách vùng', 'Tốt', 'Cải thiện')
