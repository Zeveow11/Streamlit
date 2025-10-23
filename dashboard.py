import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Kazakhstan Cars Dashboard", page_icon="🚗", layout="wide")

st.title("🚗 Kazakhstan Passenger Cars Statistics (2011-2023)")
st.markdown("---")

@st.cache_data
def load_data():
    data = {
        'Year': [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
        'Total': [3553814, 3642826, 3678282, 4000109, 3856505, 3845301, 3851583, 3847981, 3776893, 3870318, 3798071, 3909559, 4690900],
        'Petrol': [3513098, 3580756, 3613651, 3846116, 3667017, 3603175, 3555485, 3455517, 3362957, 3426786, 3343736, 3451775, 4107974],
        'Petrol_%': [98.85, 98.30, 98.24, 96.15, 95.09, 93.70, 92.31, 89.80, 89.04, 88.54, 88.04, 88.29, 87.60],
        'Diesel': [24559, 31277, 32245, 45945, 49257, 53148, 58273, 86840, 74226, 75758, 73867, 75982, 86772],
        'Diesel_%': [0.69, 0.86, 0.88, 1.15, 1.28, 1.38, 1.51, 2.26, 1.97, 1.96, 1.94, 1.94, 1.80],
        'Gas': [2127, 2753, 2781, 2868, 3474, 3716, 3639, 3751, 3623, 3951, 3886, 4160, 6782],
        'Gas_%': [0.06, 0.08, 0.08, 0.07, 0.09, 0.10, 0.09, 0.10, 0.10, 0.10, 0.10, 0.11, 0.10],
        'Hybrid': [13876, 27908, 29473, 46429, 67761, 117298, 169221, 236101, 276273, 292437, 297120, 322350, 385847],
        'Hybrid_%': [0.39, 0.77, 0.80, 1.16, 1.76, 3.05, 4.39, 6.14, 7.31, 7.56, 7.82, 8.25, 8.20],
        'Electric': [154, 132, 132, 134, 785, 725, 723, 703, 613, 550, 491, 812, 7997],
        'Electric_%': [0.00, 0.00, 0.00, 0.00, 0.02, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01, 0.02, 0.17],
        'Not_Specified': [0, 0, 0, 58617, 68211, 67239, 64242, 65069, 59201, 70836, 78971, 54480, 95526],
        'Not_Specified_%': [0, 0, 0, 1.52, 1.86, 1.87, 1.81, 1.88, 1.76, 2.07, 2.36, 1.58, 2.33]
    }
    return pd.DataFrame(data)

df = load_data()

# Sidebar
st.sidebar.header("Filters")
year_range = st.sidebar.slider("Select Year Range", 2011, 2023, (2011, 2023))
df_filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Cars (2023)", f"{df['Total'].iloc[-1]:,.0f}")
with col2:
    growth = ((df['Total'].iloc[-1] - df['Total'].iloc[0]) / df['Total'].iloc[0]) * 100
    st.metric("Growth (2011-2023)", f"{growth:.1f}%")
with col3:
    st.metric("Hybrid Cars (2023)", f"{df['Hybrid'].iloc[-1]:,.0f}")
with col4:
    st.metric("Electric Cars (2023)", f"{df['Electric'].iloc[-1]:,.0f}")

st.markdown("---")

colors = {
    'Petrol': '#FF6B6B', 'Diesel': '#4ECDC4', 'Gas': '#95E1D3',
    'Hybrid': '#FFA07A', 'Electric': '#98D8C8', 'Not_Specified': '#B19CD9'
}

categories = [
    ('Petrol', 'Petrol Cars'), ('Diesel', 'Diesel Cars'), ('Gas', 'Gas-Powered Cars'),
    ('Hybrid', 'Hybrid Cars'), ('Electric', 'Electric Cars'), ('Not_Specified', 'Not Specified')
]

for i in range(0, 6, 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(categories):
            category, title = categories[i + j]
            with cols[j]:
                st.subheader(title)
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(go.Bar(
                    x=df_filtered['Year'], y=df_filtered[category],
                    name='Units', marker_color=colors[category],
                    hovertemplate='<b>%{x}</b><br>Units: %{y:,.0f}<extra></extra>'
                ), secondary_y=False)
                
                fig.add_trace(go.Scatter(
                    x=df_filtered['Year'], y=df_filtered[f'{category}_%'],
                    name='%', mode='lines+markers',
                    line=dict(color='darkred', width=2), marker=dict(size=6),
                    hovertemplate='<b>%{x}</b><br>%: %{y:.2f}%<extra></extra>'
                ), secondary_y=True)
                
                fig.update_xaxes(title_text="Year")
                fig.update_yaxes(title_text="Units", secondary_y=False)
                fig.update_yaxes(title_text="%", secondary_y=True)
                fig.update_layout(height=350, showlegend=True, hovermode='x unified')
                
                st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📊 Summary Statistics")
st.dataframe(df_filtered, use_container_width=True)