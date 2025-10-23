import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Kazakhstan Cars", page_icon="🚗", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 Kazakhstan Passenger Cars Dashboard")
st.markdown("### Analysis of Vehicle Fleet by Fuel Type (2011-2023)")

# Load data
@st.cache_data
def load_data():
    data = {
        'Year': [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
        'Total': [3553814, 3642826, 3678282, 4000109, 3856505, 3845301, 3851583, 3847981, 3776893, 3870318, 3798071, 3909559, 4690900],
        'Petrol': [3513098, 3580756, 3613651, 3846116, 3667017, 3603175, 3555485, 3455517, 3362957, 3426786, 3343736, 3451775, 4107974],
        'Diesel': [24559, 31277, 32245, 45945, 49257, 53148, 58273, 86840, 74226, 75758, 73867, 75982, 86772],
        'Gas': [2127, 2753, 2781, 2868, 3474, 3716, 3639, 3751, 3623, 3951, 3886, 4160, 6782],
        'Hybrid': [13876, 27908, 29473, 46429, 67761, 117298, 169221, 236101, 276273, 292437, 297120, 322350, 385847],
        'Electric': [154, 132, 132, 134, 785, 725, 723, 703, 613, 550, 491, 812, 7997],
    }
    return pd.DataFrame(data)

df = load_data()

# Sidebar with filters
with st.sidebar:
    st.header("🎛️ Filters")
    year_range = st.slider("Year Range", 2011, 2023, (2011, 2023))
    
    st.markdown("---")
    st.header("📊 View Options")
    chart_type = st.radio("Chart Type", ["Bar", "Line", "Area", "Both"])
    
    show_percentage = st.checkbox("Show Percentages", value=True)
    
    st.markdown("---")
    st.info("💡 Tip: Hover over charts for details!")

df_filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

# KPI Metrics with custom styling
st.markdown("## 📈 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Cars (2023)", f"{df['Total'].iloc[-1]:,.0f}", 
              delta=f"+{df['Total'].iloc[-1] - df['Total'].iloc[0]:,.0f}")

with col2:
    growth = ((df['Total'].iloc[-1] - df['Total'].iloc[0]) / df['Total'].iloc[0]) * 100
    st.metric("Growth Since 2011", f"{growth:.1f}%", delta="13 years")

with col3:
    st.metric("Hybrid Cars", f"{df['Hybrid'].iloc[-1]:,.0f}",
              delta=f"+{((df['Hybrid'].iloc[-1]/df['Hybrid'].iloc[0])-1)*100:.0f}%")

with col4:
    st.metric("Electric Cars", f"{df['Electric'].iloc[-1]:,.0f}",
              delta=f"+{df['Electric'].iloc[-1] - df['Electric'].iloc[0]:,.0f}")

with col5:
    st.metric("Petrol Market Share", f"87.6%", delta="-11.3%", delta_color="inverse")

st.markdown("---")

# Tab layout for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔥 Trends", "📉 Market Share", "📋 Data Table"])

with tab1:
    st.markdown("### Fleet Composition by Fuel Type")
    
    # Stacked area chart
    fig_area = go.Figure()
    
    categories = ['Petrol', 'Diesel', 'Gas', 'Hybrid', 'Electric']
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#FFA07A', '#98D8C8']
    
    for cat, color in zip(categories, colors):
        fig_area.add_trace(go.Scatter(
            x=df_filtered['Year'],
            y=df_filtered[cat],
            name=cat,
            mode='lines',
            stackgroup='one',
            fillcolor=color,
            line=dict(width=0.5, color=color),
            hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Cars: %{y:,.0f}<extra></extra>'
        ))
    
    fig_area.update_layout(
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12)
    )
    
    st.plotly_chart(fig_area, use_container_width=True)
    
    # Individual charts in columns
    st.markdown("### Individual Category Analysis")
    col1, col2, col3 = st.columns(3)
    
    categories_with_titles = [
        ('Petrol', '⛽ Petrol Cars', '#FF6B6B'),
        ('Diesel', '🛢️ Diesel Cars', '#4ECDC4'),
        ('Gas', '💨 Gas-Powered Cars', '#95E1D3'),
        ('Hybrid', '🔋 Hybrid Cars', '#FFA07A'),
        ('Electric', '⚡ Electric Cars', '#98D8C8')
    ]
    
    cols = [col1, col2, col3, col1, col2]
    
    for idx, (cat, title, color) in enumerate(categories_with_titles):
        with cols[idx]:
            st.markdown(f"**{title}**")
            
            fig = go.Figure()
            
            if chart_type in ["Bar", "Both"]:
                fig.add_trace(go.Bar(
                    x=df_filtered['Year'],
                    y=df_filtered[cat],
                    marker_color=color,
                    name='Units',
                    hovertemplate='<b>%{x}</b><br>Units: %{y:,.0f}<extra></extra>'
                ))
            
            if chart_type in ["Line", "Both"]:
                fig.add_trace(go.Scatter(
                    x=df_filtered['Year'],
                    y=df_filtered[cat],
                    mode='lines+markers',
                    line=dict(color=color if chart_type == "Line" else 'darkred', width=3),
                    marker=dict(size=8),
                    name='Trend',
                    hovertemplate='<b>%{x}</b><br>Units: %{y:,.0f}<extra></extra>'
                ))
            
            fig.update_layout(
                height=300,
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show growth stat
            if df[cat].iloc[0] > 0:
                growth = ((df[cat].iloc[-1] - df[cat].iloc[0]) / df[cat].iloc[0]) * 100
                st.caption(f"📈 Growth: **{growth:+.1f}%** since 2011")

with tab2:
    st.markdown("### 🔥 Growth Trends & Analysis")
    
    # Year-over-year growth
    df_growth = df.copy()
    for cat in ['Petrol', 'Diesel', 'Gas', 'Hybrid', 'Electric']:
        df_growth[f'{cat}_growth'] = df_growth[cat].pct_change() * 100
    
    fig_growth = go.Figure()
    
    for cat, color in zip(['Hybrid', 'Electric', 'Diesel'], ['#FFA07A', '#98D8C8', '#4ECDC4']):
        fig_growth.add_trace(go.Scatter(
            x=df_growth['Year'],
            y=df_growth[f'{cat}_growth'],
            mode='lines+markers',
            name=cat,
            line=dict(width=3),
            marker=dict(size=8)
        ))
    
    fig_growth.update_layout(
        title="Year-over-Year Growth Rate (%)",
        height=500,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis_title="Growth Rate (%)",
        xaxis_title="Year"
    )
    
    st.plotly_chart(fig_growth, use_container_width=True)
    
    # Correlation heatmap
    st.markdown("### 🎯 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📊 Market Dynamics:**
        - Petrol vehicles declining but still dominant (87.6%)
        - Hybrid adoption accelerating rapidly
        - Electric vehicles showing breakthrough in 2023
        """)
    
    with col2:
        st.success("""
        **💡 Future Outlook:**
        - Green vehicles (Hybrid + Electric) now >8% of fleet
        - Electric cars grew 885% in 2023 alone
        - Traditional fuels losing market share
        """)

with tab3:
    st.markdown("### 📉 Market Share Evolution")
    
    # Calculate percentages
    df_pct = df.copy()
    for cat in ['Petrol', 'Diesel', 'Gas', 'Hybrid', 'Electric']:
        df_pct[f'{cat}_pct'] = (df_pct[cat] / df_pct['Total']) * 100
    
    # Stacked bar chart
    fig_share = go.Figure()
    
    categories = ['Petrol', 'Diesel', 'Gas', 'Hybrid', 'Electric']
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#FFA07A', '#98D8C8']
    
    for cat, color in zip(categories, colors):
        fig_share.add_trace(go.Bar(
            x=df_pct['Year'],
            y=df_pct[f'{cat}_pct'],
            name=cat,
            marker_color=color,
            hovertemplate='<b>%{fullData.name}</b><br>%{y:.2f}%<extra></extra>'
        ))
    
    fig_share.update_layout(
        barmode='stack',
        height=500,
        yaxis_title="Market Share (%)",
        xaxis_title="Year",
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig_share, use_container_width=True)
    
    # Pie chart for current year
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 2011 Market Share")
        fig_pie1 = px.pie(
            values=[df['Petrol'].iloc[0], df['Diesel'].iloc[0], df['Gas'].iloc[0], 
                   df['Hybrid'].iloc[0], df['Electric'].iloc[0]],
            names=categories,
            color_discrete_sequence=colors,
            hole=0.4
        )
        fig_pie1.update_layout(height=400)
        st.plotly_chart(fig_pie1, use_container_width=True)
    
    with col2:
        st.markdown("#### 2023 Market Share")
        fig_pie2 = px.pie(
            values=[df['Petrol'].iloc[-1], df['Diesel'].iloc[-1], df['Gas'].iloc[-1], 
                   df['Hybrid'].iloc[-1], df['Electric'].iloc[-1]],
            names=categories,
            color_discrete_sequence=colors,
            hole=0.4
        )
        fig_pie2.update_layout(height=400)
        st.plotly_chart(fig_pie2, use_container_width=True)

with tab4:
    st.markdown("### 📋 Raw Data")
    
    # Style the dataframe
    st.dataframe(
        df_filtered.style.format({
            'Total': '{:,.0f}',
            'Petrol': '{:,.0f}',
            'Diesel': '{:,.0f}',
            'Gas': '{:,.0f}',
            'Hybrid': '{:,.0f}',
            'Electric': '{:,.0f}'
        }).background_gradient(subset=['Total'], cmap='Blues'),
        use_container_width=True
    )
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name="kazakhstan_cars_data.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.caption("📊 Data Source: Kazakhstan Automobile Statistics | 🔄 Last Updated: 2023")
