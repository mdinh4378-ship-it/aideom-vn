import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout='wide', page_title='AIDEOM-VN Dashboard')
st.sidebar.header('AIDEOM-VN Dashboard')

menu = st.sidebar.radio('Danh mục 12 Bài', [
    'Bài 1: Macro', 'Bài 2: LP', 'Bài 3: MIP', 'Bài 4: MOO', 
    'Bài 5: Stochastic 1', 'Bài 6: DP', 'Bài 7: RL', 'Bài 8: CGE', 
    'Bài 9: Spatial', 'Bài 10: Stochastic 2', 'Bài 11: DQN', 'Bài 12: Tổng hợp'
])

if menu == 'Bài 1: Macro':
    st.title('Bài 1: Hàm sản xuất Cobb-Douglas mở rộng')
    st.markdown('Phân tích tác động của AI và Số hóa đến tăng trưởng kinh tế vĩ mô.')
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader('Hệ số co giãn')
        alpha = st.slider('Vốn (α)', 0.0, 1.0, 0.33)
        beta = st.slider('Lao động (β)', 0.0, 1.0, 0.42)
        gamma = st.slider('Số hóa (γ)', 0.0, 1.0, 0.10)
        delta = st.slider('Năng lực AI (δ)', 0.0, 1.0, 0.08)
        theta = st.slider('Nhân lực số (θ)', 0.0, 1.0, 0.07)
        
        sum_params = alpha + beta + gamma + delta + theta
        if round(sum_params, 2) == 1.00:
            st.success(f'Tổng hệ số: {sum_params:.2f} (Chuẩn CRS)')
        else:
            st.warning(f'Tổng hệ số: {sum_params:.2f} (Cảnh báo: Nên = 1.0)')

    with col2:
        tab1, tab2, tab3 = st.tabs(['Khớp mô hình', 'Hạch toán Tăng trưởng', 'Dự báo 2030'])
        
        # Dữ liệu gốc
        years = np.array([2020, 2021, 2022, 2023, 2024, 2025])
        Y = np.array([8044.4, 8487.5, 9513.3, 10221.8, 11511.9, 12847.6])
        K = np.array([16500, 17800, 19600, 21300, 23500, 25900])
        L = np.array([53.6, 50.5, 51.7, 52.4, 52.9, 53.4])
        D = np.array([12.0, 12.7, 14.3, 16.5, 18.3, 19.5])
        AI = np.array([55.6, 60.2, 65.4, 67.0, 73.8, 80.1])
        H = np.array([24.1, 26.1, 26.2, 27.0, 28.4, 29.2])

        # Tính toán TFP và Y Dự báo
        denom = (K**alpha) * (L**beta) * (D**gamma) * (AI**delta) * (H**theta)
        At = Y / denom
        A_mean = np.mean(At)
        Y_pred = A_mean * denom
        mape = np.mean(np.abs((Y - Y_pred) / Y)) * 100

        with tab1:
            col_m1, col_m2 = st.columns(2)
            col_m1.metric('MAPE (Độ lệch chuẩn)', f'{mape:.2f}%')
            col_m2.metric('TFP Trung bình', f'{A_mean:.4f}')

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=years, y=Y, mode='lines+markers', name='GDP Thực tế', line=dict(color='#3b82f6', width=3)))
            fig.add_trace(go.Scatter(x=years, y=Y_pred, mode='lines+markers', name='GDP Dự báo', line=dict(color='#f59e0b', width=3, dash='dash')))
            fig.update_layout(title='GDP Thực tế vs Dự báo (Nghìn tỷ VND)', margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            # Hạch toán tăng trưởng (CAGR)
            g_Y = (np.power(Y[-1]/Y[0], 1/5) - 1) * 100
            g_K = (np.power(K[-1]/K[0], 1/5) - 1) * 100
            g_L = (np.power(L[-1]/L[0], 1/5) - 1) * 100
            g_D = (np.power(D[-1]/D[0], 1/5) - 1) * 100
            g_AI = (np.power(AI[-1]/AI[0], 1/5) - 1) * 100
            g_H = (np.power(H[-1]/H[0], 1/5) - 1) * 100
            g_A = (np.power(At[-1]/At[0], 1/5) - 1) * 100

            labels = ['Vốn (K)', 'Lao động (L)', 'Số hóa (D)', 'AI', 'Nhân lực số (H)', 'TFP']
            values = [alpha*g_K, beta*g_L, gamma*g_D, delta*g_AI, theta*g_H, g_A]

            fig2 = px.pie(values=values, names=labels, hole=0.5)
            fig2.update_layout(title=f'Đóng góp vào Tăng trưởng GDP (Tổng: {g_Y:.2f}%/năm)')
            st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            st.markdown('**Dự báo Vĩ mô năm 2030**')
            A_2030 = At[-1] * (1.012**5)
            K_2030 = K[-1] * (1.06**5)
            L_2030 = L[-1] * (1.06**5)
            Y_2030 = A_2030 * (K_2030**alpha) * (L_2030**beta) * (30.0**gamma) * (100.0**delta) * (35.0**theta)

            st.metric('Kết quả GDP Dự báo (2030)', f'{(Y_2030/1000):.2f} triệu tỷ VNĐ')
            st.info('Giả định đầu vào 2030: Vốn và Lao động tăng 6%/năm. TFP tăng 1.2%/năm. Số hóa đạt 30%, AI đạt 100k doanh nghiệp, Nhân lực số đạt 35%.')
elif menu == 'Bài 2: LP':
    st.title('Bài 2: Phân bổ Ngân sách (Quy hoạch Tuyến tính)')
    st.markdown('Tối ưu hóa 4 hạng mục đầu tư bằng mô hình Linear Programming (LP).')

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader('Thông số đầu vào')
        budget = st.slider('Ngân sách (B)', 70, 150, 100)
        min_x3 = st.slider('Min Nhân lực (x3)', 10, 50, 20)
        tech_pct = st.slider('Tỷ trọng Công nghệ (%)', 10, 50, 35)
        tech_ratio = tech_pct / 100.0

    with col2:
        tab1, tab2 = st.tabs(['Dashboard Tương tác', 'Mô hình Toán & Code'])

        with tab1:
            from scipy.optimize import linprog

            # Hàm mục tiêu: Maximize Z
            c = [-0.85, -1.20, -0.95, -1.35]

            # Ràng buộc bất phương trình
            A_ub = [
                [1, 1, 1, 1],
                [0, -1, 0, -1]
            ]
            b_ub = [budget, -tech_ratio * budget]

            # Giới hạn cho từng biến
            bounds = [
                (25, None),      
                (15, None),      
                (min_x3, None),  
                (10, None)       
            ]

            res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

            if res.success:
                Z = -res.fun
                x1, x2, x3, x4 = res.x

                col_z, col_shadow = st.columns(2)
                col_z.metric('Mục tiêu GDP (Z*)', f'{Z:.2f} nghìn tỷ')
                col_shadow.success('Bài toán có nghiệm tối ưu.')

                alloc_data = pd.DataFrame({
                    'Hạng mục': ['Hạ tầng số', 'AI & Dữ liệu', 'Nhân lực số', 'R&D Công nghệ'],
                    'Phân bổ': [x1, x2, x3, x4]
                })
                
                fig = px.bar(alloc_data, x='Phân bổ', y='Hạng mục', orientation='h', color='Hạng mục')
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f'Bài toán VÔ NGHIỆM: Ngân sách {budget}k tỷ không đủ để đáp ứng các mức đầu tư tối thiểu và {tech_pct}% tỷ trọng công nghệ.')

        with tab2:
            st.markdown('**1. Triển khai code Python (Scipy):**')
            st.code('''
from scipy.optimize import linprog

c = [-0.85, -1.20, -0.95, -1.35]
A_ub = [[1, 1, 1, 1], [0, -1, 0, -1]]
b_ub = [budget, -tech_ratio * budget]
bounds = [(25, None), (15, None), (min_x3, None), (10, None)]

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
            ''', language='python')

elif menu == 'Bài 3: MIP':
    st.title('Bài 3: Lựa chọn Dự án Đầu tư (MIP)')
    st.markdown('Giải bài toán cái túi (Knapsack) với ràng buộc logic bằng thuật toán Quy hoạch nguyên.')

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader('Thông số')
        budget_mip = st.slider('Ngân sách (B)', 30, 150, 80, key='b3')
        use_prereq = st.checkbox('Bật Ràng buộc Tiền quyết (Nền tảng AI cần TT Dữ liệu)', value=True)
        use_exclusive = st.checkbox('Bật Ràng buộc Loại trừ (Chỉ chọn 1: Y tế hoặc NN)', value=False)

    with col2:
        tab1, tab2 = st.tabs(['Kết quả Phân bổ', 'Mô hình Toán học'])

        with tab1:
            projects = [
                {'id': 0, 'name': 'TT Dữ liệu Quốc gia', 'cost': 30, 'return': 50},
                {'id': 1, 'name': 'Nền tảng AI Tiếng Việt', 'cost': 20, 'return': 35},
                {'id': 2, 'name': 'Đào tạo 50k Kỹ sư', 'cost': 15, 'return': 25},
                {'id': 3, 'name': 'Y tế Thông minh', 'cost': 25, 'return': 40},
                {'id': 4, 'name': 'Nông nghiệp AI', 'cost': 10, 'return': 18}
            ]

            max_z = 0
            best_x = [0, 0, 0, 0, 0]
            used_b = 0

            # Thuật toán Brute-force vét cạn 2^5 = 32 trường hợp
            for i in range(32):
                x = [(i >> j) & 1 for j in range(5)]
                cost = sum(x[j] * projects[j]['cost'] for j in range(5))
                
                if cost > budget_mip: 
                    continue
                if use_prereq and x[1] > x[0]: 
                    continue
                if use_exclusive and (x[3] + x[4] > 1): 
                    continue
                
                ret = sum(x[j] * projects[j]['return'] for j in range(5))
                if ret > max_z:
                    max_z = ret
                    best_x = x
                    used_b = cost

            col_res1, col_res2 = st.columns(2)
            col_res1.metric('Tổng Lợi ích (Z*)', f'{max_z} nghìn tỷ')
            col_res2.metric('Ngân sách đã dùng', f'{used_b} / {budget_mip}')

            st.markdown('**Danh sách dự án:**')
            for j, p in enumerate(projects):
                status = '✅ CHỌN' if best_x[j] else '❌ Bỏ qua'
                color = 'green' if best_x[j] else 'gray'
                st.markdown(f"- :{color}[**{status}**] - {p['name']} (Chi phí: {p['cost']}, Hoàn vốn: {p['return']})")

        with tab2:
            st.markdown('**Mô hình Quy hoạch Nguyên (MIP):**')
            st.markdown(r'''
            * **Biến quyết định:** $x_i \in \{0, 1\}$
            * **Hàm mục tiêu:** Maximize $Z = 50x_0 + 35x_1 + 25x_2 + 40x_3 + 18x_4$
            * **Ràng buộc Ngân sách:** $30x_0 + 20x_1 + 15x_2 + 25x_3 + 10x_4 \le B$
            * **Ràng buộc Tiền quyết:** $x_1 \le x_0$
            * **Ràng buộc Loại trừ:** $x_3 + x_4 \le 1$
            ''')
elif menu == 'Bài 4: MOO':
    st.title('Bài 4: Tối ưu hóa Đa mục tiêu (MOO)')
    st.markdown('Tìm tập hợp các phương án Pareto-Optimal giữa Tăng trưởng và Phát thải.')

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader('Tham số ràng buộc')
        epsilon = st.slider('Ràng buộc phát thải (ε-CO2)', -20, 80, 30)
        st.info(f'Giới hạn phát thải tối đa là {epsilon} đơn vị.')

    with col2:
        tab1, tab2 = st.tabs(['Đường biên Pareto', 'Phương pháp giải'])

        with tab1:
            # Tạo đường cong mô phỏng Pareto
            co2_vals = np.arange(-20, 85, 5)
            gdp_vals = 40 + np.sqrt(np.clip((co2_vals + 20), 0, None)) * 5
            
            df_pareto = pd.DataFrame({'CO2': co2_vals, 'GDP': gdp_vals})
            
            fig = px.line(df_pareto, x='CO2', y='GDP', title='Đường biên Pareto (Trade-off)')
            # Điểm giải pháp tối ưu theo epsilon
            optimal_gdp = 40 + np.sqrt(np.clip((epsilon + 20), 0, None)) * 5
            fig.add_scatter(x=[epsilon], y=[optimal_gdp], mode='markers+text', 
                            name='Giải pháp chọn', text=['Tối ưu'], textposition='top center',
                            marker=dict(size=12, color='red'))
            
            st.plotly_chart(fig, use_container_width=True)
            st.success(f'Tại mức phát thải {epsilon}, GDP tối đa đạt được là {optimal_gdp:.2f} nghìn tỷ.')

        with tab2:
            st.markdown('**1. Mô hình Epsilon-Constraint:**')
            st.latex(r'''
            \text{Maximize } f_1(x) = \text{GDP}(x) \\
            \text{Subject to: } f_2(x) = \text{CO2}(x) \le \epsilon
            ''')
            st.markdown('**2. Ý nghĩa:**')
            st.write('Bằng cách thay đổi giá trị $\epsilon$ (ngân sách phát thải), ta vẽ ra được toàn bộ đường biên Pareto, giúp nhà hoạch định thấy được cái giá phải trả (trade-off) nếu muốn giảm phát thải thêm một đơn vị.')

elif menu == 'Bài 5: Stochastic 1':
    st.title('Bài 5: Tối ưu Ngẫu nhiên Cơ bản')
    st.markdown('Bài toán "Người bán báo" (News-vendor Problem): Tối ưu số lượng đầu tư trong điều kiện nhu cầu không chắc chắn.')

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader('Biến quyết định (GĐ 1)')
        investX = st.slider('Số lượng máy chủ (X)', 0, 2500, 1000, step=100)
        
        st.info('Giả định nhu cầu (Xác suất):')
        st.write('- 30% Thấp (500)')
        st.write('- 50% Bình thường (1000)')
        st.write('- 20% Cao (2000)')

    with col2:
        tab1, tab2 = st.tabs(['Đường cong Chi phí Kỳ vọng', 'Giải thích thuật toán'])

        with tab1:
            # Thuật toán tính hàm kỳ vọng E[C(X)]
            # Chi phí: Mua 10/cụm, Thuê bù 25/cụm
            curve = []
            min_cost = float('inf')
            best_x = 0
            
            for x in range(0, 2600, 50):
                # E[C(X)] = Sum(P_i * (x*10 + max(0, D_i - x)*25))
                ec = 0.3*(x*10 + max(0, 500-x)*25) + 0.5*(x*10 + max(0, 1000-x)*25) + 0.2*(x*10 + max(0, 2000-x)*25)
                curve.append({'x': x, 'cost': ec})
                if ec < min_cost:
                    min_cost = ec
                    best_x = x
            
            df_curve = pd.DataFrame(curve)
            current_cost = df_curve.loc[df_curve['x'] == investX, 'cost'].values[0]
            
            fig = px.line(df_curve, x='x', y='cost', title='Chi phí Kỳ vọng E[C(X)]')
            fig.add_scatter(x=[investX], y=[current_cost], mode='markers', name='Điểm chọn', marker=dict(size=12, color='red'))
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric('Chi phí kỳ vọng tại X hiện tại', f'{current_cost:.0f} tỷ VND')
            st.warning(f'Chi phí tối ưu đạt được tại X = {best_x} đơn vị.')

        with tab2:
            st.markdown('**1. Cấu trúc mô hình:**')
            st.latex(r'''
            \text{Minimize } E[C(X)] = C_m \cdot X + E[C_s \cdot \max(0, D - X)]
            ''')
            st.write('Trong đó:')
            st.write('- $C_m$: Chi phí mua (10)')
            st.write('- $C_s$: Chi phí thuê bù (25)')
            st.write('- $D$: Nhu cầu ngẫu nhiên')
            st.markdown('**2. Bản chất:** Đây là mô hình 2 giai đoạn: Giai đoạn 1 (Here-and-Now) quyết định $X$, Giai đoạn 2 (Recourse) xử lý phần thiếu hụt $D-X$ khi nhu cầu đã hiện thực hóa.')
    
elif menu == 'Bài 6: DP':
    st.title('Bài 6: Tối ưu hóa Động (Dynamic Programming)')
    st.markdown('Mô phỏng tích lũy Vốn ($K_t$) và Năng lực số qua 5 năm bằng phương trình Bellman.')

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader('Tham số trạng thái')
        inv = st.slider('Đầu tư hàng năm ($I_t$)', 10, 50, 20)
        depreciation = st.slider('Tỷ lệ khấu hao ($\delta$)', 0.05, 0.25, 0.10)
        
        st.info('Phương trình trạng thái:')
        st.latex(r'K_{t+1} = (1 - \delta)K_t + I_t')

    with col2:
        tab1, tab2 = st.tabs(['Lộ trình Tích lũy Vốn', 'Giải thích Thuật toán'])
        
        with tab1:
            # Giải phương trình trạng thái
            K = 100 # Vốn ban đầu
            k_vals = []
            y_vals = []
            for t in range(5):
                Y = 10 * np.sqrt(K) # Hàm sản xuất: Y = A*K^0.5
                k_vals.append(K)
                y_vals.append(Y)
                K = (1 - depreciation) * K + inv
            
            df_dp = pd.DataFrame({'Năm': range(2026, 2031), 'Vốn (K)': k_vals, 'GDP (Y)': y_vals})
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df_dp['Năm'], y=df_dp['Vốn (K)'], name='Vốn (K)'))
            fig.add_trace(go.Scatter(x=df_dp['Năm'], y=df_dp['GDP (Y)'], name='GDP (Y)', mode='lines+markers', line=dict(width=3)))
            fig.update_layout(title='Kết quả mô phỏng tích lũy vốn 2026-2030')
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.markdown('**1. Nguyên lý tối ưu Bellman:**')
            st.write('Giá trị của hiện tại phụ thuộc vào giá trị của tương lai.')
            st.latex(r'''
            V_t(K_t) = \max_{I_t} \{ Y_t + \beta V_{t+1}(K_{t+1}) \}
            ''')
            st.markdown('**2. Quy trình:**')
            st.write('- **Trạng thái (State):** Vốn tích lũy $K_t$')
            st.write('- **Quyết định (Action):** Mức đầu tư $I_t$')
            st.write('- **Chuyển trạng thái:** Phương trình khấu hao và tái đầu tư.')
            st.write('Đây là mô hình quy hoạch động xác định (Deterministic DP). Ở các bài sau, chúng ta sẽ mở rộng sang stochastic.')

elif menu == 'Bài 7: RL':
    st.title('Bài 7: Học tăng cường (Reinforcement Learning)')
    st.markdown('Agent AI tự học chính sách đào tạo lao động bằng thuật toán Q-Learning.')

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader('Tham số huấn luyện')
        lr = st.slider('Tốc độ học (Alpha)', 0.01, 0.5, 0.1)
        gamma = st.slider('Tỷ lệ chiết khấu (Gamma)', 0.5, 0.99, 0.9)
        if st.button('Bắt đầu huấn luyện'):
            st.session_state.rl_running = True

    with col2:
        tab1, tab2 = st.tabs(['Dashboard Huấn luyện', 'Cấu trúc Q-Learning'])
        
        with tab1:
            if 'q_table' not in st.session_state:
                st.session_state.q_table = np.zeros((3, 2)) # 3 Trạng thái, 2 Hành động
            
            # Mô phỏng quá trình hội tụ
            if st.session_state.get('rl_running'):
                # Cập nhật Q-table đơn giản
                for s in range(3):
                    action = np.random.randint(2)
                    reward = 5 if s == 0 and action == 1 else -1
                    st.session_state.q_table[s, action] += lr * (reward + gamma * 0 - st.session_state.q_table[s, action])
                st.success('Đang huấn luyện Agent...')
            
            df_q = pd.DataFrame(st.session_state.q_table, 
                                columns=['Bỏ mặc', 'Đào tạo'], 
                                index=['LĐ Phổ thông', 'Kỹ năng Vừa', 'Kỹ năng Cao'])
            
            fig = px.imshow(df_q, text_auto=True, title='Q-Table (Giá trị Hành động tại mỗi Trạng thái)', color_continuous_scale='RdBu')
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.markdown('**1. Hàm cập nhật Q-Value (Bellman Equation):**')
            st.latex(r'''
            Q(s, a) \leftarrow Q(s, a) + \alpha [R + \gamma \max_{a'} Q(s', a') - Q(s, a)]
            ''')
            st.markdown('**2. Các thành phần:**')
            st.write('- **Trạng thái (s):** Trình độ lao động hiện tại.')
            st.write('- **Hành động (a):** Đào tạo hoặc Bỏ mặc.')
            st.write('- **Phần thưởng (R):** Tăng trưởng năng suất sau đào tạo.')
            st.write('Agent sẽ dần ưu tiên các hành động có giá trị Q cao nhất (ô màu xanh đậm trên Q-Table).')

elif menu == 'Bài 8: CGE':
    st.title('Bài 8: Cân bằng Tổng quát (CGE)')
    st.markdown('Mô phỏng sự dịch chuyển của Giá và Sản lượng thị trường khi áp Thuế Carbon.')

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader('Thông số chính sách')
        carbon_tax = st.slider('Mức Thuế Carbon ($/tấn)', 0, 60, 20)
        st.info('Thuế Carbon làm tăng chi phí biên của doanh nghiệp, đẩy đường Cung sang trái.')

    with col2:
        tab1, tab2 = st.tabs(['Đồ thị Cân bằng', 'Mô hình Toán học'])
        
        with tab1:
            # Đường cầu: Qd = 120 - P
            # Đường cung bị ảnh hưởng bởi Thuế: Qs = 20 + 1.5 * (P - Tax)
            prices = np.linspace(20, 100, 50)
            demand = 120 - prices
            supply = 20 + 1.5 * (prices - carbon_tax)
            
            # Tính điểm cân bằng: 120 - P = 20 + 1.5P - 1.5*Tax => 2.5P = 100 + 1.5*Tax
            p_eq = (100 + 1.5 * carbon_tax) / 2.5
            q_eq = 120 - p_eq
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=demand, y=prices, name='Đường Cầu (Qd)', line=dict(color='blue', width=3)))
            fig.add_trace(go.Scatter(x=supply, y=prices, name='Đường Cung (Qs)', line=dict(color='red', width=3)))
            fig.add_trace(go.Scatter(x=[q_eq], y=[p_eq], mode='markers', name='Điểm cân bằng', marker=dict(size=12, color='black')))
            
            fig.update_layout(title='Cân bằng Thị trường (P*, Q*)', xaxis_title='Sản lượng (Q)', yaxis_title='Giá (P)')
            st.plotly_chart(fig, use_container_width=True)
            st.metric('Giá cân bằng thị trường (P*)', f'${p_eq:.2f}')
            st.metric('Sản lượng cân bằng (Q*)', f'{q_eq:.2f}')

        with tab2:
            st.markdown('**1. Hệ phương trình Cân bằng:**')
            st.latex(r'''
            \begin{cases} 
            Q_d = 120 - P \\
            Q_s = 20 + 1.5(P - T) 
            \end{cases}
            ''')
            st.write('Tại điểm cân bằng, $Q_d = Q_s$. Khi Thuế Carbon ($T$) tăng, đường Cung dịch chuyển sang trái, làm giá tăng và sản lượng giảm.')

elif menu == 'Bài 9: Spatial':
    st.title('Bài 9: Kinh tế học Không gian')
    st.markdown('Mô hình Trọng lực: Sức hút của các Siêu đô thị và sự phân rã theo khoảng cách.')

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader('Tham số không gian')
        friction = st.slider('Hệ số ma sát (Phí VC)', 0.01, 0.2, 0.05)
        hub_power = st.slider('Sức hút Trung tâm (Hub)', 500, 2000, 1000)
        st.write('Hệ số ma sát cao khiến mật độ kinh tế giảm cực nhanh khi đi xa khỏi trung tâm.')

    with col2:
        tab1, tab2 = st.tabs(['Đường cong Mật độ', 'Mô hình Toán học'])
        
        with tab1:
            # Khoảng cách từ Hub ra ngoại vi (km)
            distances = np.arange(0, 500, 10)
            # Mật độ E(d) = Power * exp(-friction * d)
            density = hub_power * np.exp(-friction * distances)
            
            df_spatial = pd.DataFrame({'Khoảng cách (km)': distances, 'Mật độ kinh tế': density})
            
            fig = px.area(df_spatial, x='Khoảng cách (km)', y='Mật độ kinh tế', 
                          title='Sự suy giảm Mật độ Kinh tế theo khoảng cách')
            st.plotly_chart(fig, use_container_width=True)
            
            st.info('Đồ thị cho thấy vùng "hinterland" (ngoại vi) cần hạ tầng kết nối tốt (giảm ma sát) để thu hẹp khoảng cách phát triển.')

        with tab2:
            st.markdown('**1. Hàm trọng lực không gian:**')
            st.latex(r'''
            E(d) = A \cdot e^{-\phi \cdot d}
            ''')
            st.write('Trong đó:')
            st.write('- $E(d)$: Mật độ kinh tế tại khoảng cách $d$')
            st.write('- $A$: Sức hút của Hub trung tâm')
            st.write('- $\phi$: Hệ số ma sát vận chuyển/giao dịch')
            st.write('- $d$: Khoảng cách địa lý')
            
            st.markdown('**2. Ứng dụng:**')
            st.write('Mô hình này giúp quy hoạch đường cao tốc hoặc các cụm công nghiệp vệ tinh để điều phối dòng vốn đầu tư tối ưu.')

elif menu == 'Bài 10: Stochastic 2':
    st.title('Bài 10: Quy hoạch ngẫu nhiên 2 giai đoạn')
    st.markdown('Đánh giá Giá trị của Giải pháp Ngẫu nhiên (VSS) dưới rủi ro Khủng hoảng.')

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader('Thông số kịch bản')
        prob_crisis = st.slider('Xác suất Khủng hoảng (p)', 0.0, 0.8, 0.2)
        st.info('Kịch bản: AI sinh lời cao lúc bình thường, nhưng Nhân lực là khoản đầu tư phòng thủ an toàn lúc khủng hoảng.')

    with col2:
        tab1, tab2 = st.tabs(['Phân tích VSS', 'Mô hình Toán học'])
        
        with tab1:
            # EV (Expected Value) Strategy: Đầu tư mù quáng vào AI (LN lúc nào cũng cao)
            # SP (Stochastic Program) Strategy: Đầu tư phòng thủ, dồn vốn vào Nhân lực (H)
            
            # Tỷ suất sinh lời: Bình thường (AI=1.5, H=0.8) | Khủng hoảng (AI=0.2, H=2.0)
            evProfit = (80*1.5 + 20*0.8) * (1 - prob_crisis) + (80*0.2 + 20*2.0) * prob_crisis
            spProfit = (40*1.5 + 60*0.8) * (1 - prob_crisis) + (40*0.2 + 60*2.0) * prob_crisis
            vss = spProfit - evProfit
            
            df_vss = pd.DataFrame({
                'Kế hoạch': ['Ngây thơ (EV)', 'Ngẫu nhiên (SP)'],
                'Kỳ vọng': [evProfit, spProfit]
            })
            
            fig = px.bar(df_vss, x='Kế hoạch', y='Kỳ vọng', color='Kế hoạch', 
                         title='So sánh Lợi nhuận Kỳ vọng giữa EV và SP')
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric('Giá trị VSS (Lợi ích vượt trội)', f'+{max(0, vss):.2f}')
            st.write('VSS > 0 chứng minh việc lập kế hoạch dựa trên kịch bản ngẫu nhiên luôn mang lại lợi ích kinh tế cao hơn.')

        with tab2:
            st.markdown('**1. Cấu trúc mô hình 2 giai đoạn:**')
            st.latex(r'''
            \text{Min } c^T x + E_{\omega} [Q(x, \omega)]
            ''')
            st.write('- **GĐ1 (x):** Quyết định đầu tư trước khi biết kịch bản.')
            st.write('- **GĐ2 (Q):** Quyết định điều chỉnh (Recourse) tùy thuộc vào kịch bản $\omega$.')
            st.write('- **VSS:** Đo lường chi phí cơ hội nếu chúng ta dự báo sai rủi ro ngay từ đầu.')

elif menu == 'Bài 11: DQN':
    st.title('Bài 11: Deep Q-Network (DQN)')
    st.markdown('Sử dụng Mạng nơ-ron sâu để ước lượng hàm Q(s, a) trong môi trường phức tạp.')

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader('Tham số huấn luyện')
        lr = st.slider('Learning Rate', 0.0001, 0.01, 0.001, format="%.4f")
        if st.button('Khởi động mô phỏng'):
            st.session_state.dqn_running = True

    with col2:
        tab1, tab2 = st.tabs(['Hội tụ (Loss & Reward)', 'Kiến trúc mạng (DQN)'])
        
        with tab1:
            # Mô phỏng quá trình training của mạng nơ-ron
            episodes = np.arange(0, 1000, 50)
            reward = 100 - 80 * np.exp(-0.005 * episodes) + np.random.normal(0, 2, len(episodes))
            loss = 50 * np.exp(-0.01 * episodes) + np.random.normal(0, 1, len(episodes))
            
            df_dqn = pd.DataFrame({'Epoch': episodes, 'Reward': reward, 'Loss': loss})
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_dqn['Epoch'], y=df_dqn['Reward'], name='Reward (Phần thưởng)', line=dict(color='#10b981')))
            fig.add_trace(go.Scatter(x=df_dqn['Epoch'], y=df_dqn['Loss'], name='Loss (Mất mát)', line=dict(color='#ef4444')))
            fig.update_layout(title='Quá trình học của DQN Agent', xaxis_title='Epoch', yaxis_title='Giá trị')
            st.plotly_chart(fig, use_container_width=True)
            
            st.write('Đường Reward đi lên và Loss đi xuống cho thấy mạng nơ-ron đang hội tụ về chính sách tối ưu.')

        with tab2:
            st.markdown('**Cấu trúc Mạng nơ-ron DQN:**')
            st.code('''
import torch.nn as nn
class DQN(nn.Module):
    def __init__(self, n_obs, n_act):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_obs, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, n_act)
        )
    def forward(self, x):
        return self.net(x)
            ''', language='python')
            st.write('Mạng này nhận "trạng thái" làm đầu vào và xuất ra "Giá trị Q" cho tất cả các hành động có thể thực hiện.')

elif menu == 'Bài 12: Tổng hợp':
    st.title('Bài 12: Đồ án Tổng hợp')
    scen = st.selectbox('Kịch bản', ['S1: Cơ sở', 'S4: Tối ưu'])
    col1, col2, col3 = st.columns(3)
    if scen == 'S1: Cơ sở':
        col1.metric('GDP', 12.5)
        col2.metric('CO2', 80)
        col3.metric('Ngân sách', 100)
    else:
        col1.metric('GDP', 15.5, 3.0)
        col2.metric('CO2', 20, -60)
        col3.metric('Ngân sách', 110, 10)
    
    df = pd.DataFrame(dict(
        r=[85, 90, 85, 85, 95] if scen == 'S4: Tối ưu' else [70, 60, 65, 50, 60],
        theta=['Kinh tế', 'Công nghệ', 'Vùng miền', 'Môi trường', 'Nhân lực']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)
