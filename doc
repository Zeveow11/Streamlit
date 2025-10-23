import streamlit as st
import plotly.express as px
import pandas as pd
import json
import requests

st.set_page_config(page_title="Kazakhstan Regions Map", page_icon="🗺️", layout="wide")

st.title("🗺️ Kazakhstan Regional Map")
st.markdown("### Interactive map showing all regions (oblasts) of Kazakhstan")

# Load Kazakhstan GeoJSON from online source
@st.cache_data
def load_geojson():
    # This URL has Kazakhstan regions data
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/kazakhstan.geojson"
    response = requests.get(url)
    return response.json()

# Sample data for regions (you can customize this)
@st.cache_data
def load_region_data():
    regions = {
        'name': [
            'Almaty', 'Nur-Sultan', 'Shymkent', 'Akmola', 'Aktobe', 'Almaty Region',
            'Atyrau', 'East Kazakhstan', 'Zhambyl', 'West Kazakhstan', 'Karaganda',
            'Kostanay', 'Kyzylorda', 'Mangystau', 'Pavlodar', 'North Kazakhstan', 'Turkestan'
        ],
        'population': [
            2000000, 1200000, 1100000, 750000, 900000, 2100000,
            650000, 1400000, 1150000, 680000, 1380000,
            880000, 820000, 720000, 750000, 550000, 2000000
        ],
        'cars': [
            450000, 280000, 240000, 180000, 210000, 480000,
            150000, 320000, 260000, 160000, 310000,
            200000, 190000, 170000, 180000, 130000, 450000
        ]
    }
    return pd.DataFrame(regions)

# Load data
try:
    geojson = load_geojson()
    df = load_region_data()
    
    # Sidebar options
    st.sidebar.header("🎛️ Map Settings")
    
    metric_choice = st.sidebar.selectbox(
        "Choose metric to display",
        ["Population", "Number of Cars", "Cars per Capita"]
    )
    
    color_scheme = st.sidebar.selectbox(
        "Color Scheme",
        ["Viridis", "Blues", "Reds", "Greens", "Plasma", "Turbo"]
    )
    
    # Calculate cars per capita if needed
    if metric_choice == "Cars per Capita":
        df['cars_per_capita'] = (df['cars'] / df['population'] * 1000).round(1)
        metric_column = 'cars_per_capita'
        metric_label = 'Cars per 1000 people'
    elif metric_choice == "Population":
        metric_column = 'population'
        metric_label = 'Population'
    else:
        metric_column = 'cars'
        metric_label = 'Number of Cars'
    
    # Create choropleth map
    fig = px.choropleth(
        df,
        geojson=geojson,
        locations='name',
        featureidkey="properties.name",
        color=metric_column,
        color_continuous_scale=color_scheme,
        hover_name='name',
        hover_data={
            'name': False,
            'population': ':,',
            'cars': ':,',
            metric_column: ':,.1f' if metric_choice == "Cars per Capita" else ':,'
        },
        labels={metric_column: metric_label},
        title=f"Kazakhstan Regions by {metric_choice}"
    )
    
    fig.update_geos(
        fitbounds="locations",
        visible=False
    )
    
    fig.update_layout(
        height=700,
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    st.markdown("---")
    st.markdown("### 📊 Regional Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Population", f"{df['population'].sum():,}")
    
    with col2:
        st.metric("Total Cars", f"{df['cars'].sum():,}")
    
    with col3:
        st.metric("Average Cars/1000", f"{(df['cars'].sum() / df['population'].sum() * 1000):.1f}")
    
    with col4:
        st.metric("Number of Regions", len(df))
    
    # Data table
    st.markdown("---")
    st.markdown("### 📋 Regional Data")
    
    st.dataframe(
        df.sort_values(metric_column, ascending=False),
        use_container_width=True,
        column_config={
            "name": "Region Name",
            "population": st.column_config.NumberColumn("Population", format="%d"),
            "cars": st.column_config.NumberColumn("Cars", format="%d"),
        },
        hide_index=True
    )

except Exception as e:
    st.error(f"Error loading map data: {str(e)}")
    st.info("💡 Using alternative visualization...")
    
    # Fallback: Simple bar chart if map fails
    df = load_region_data()
    
    st.bar_chart(df.set_index('name')['cars'])

# Footer
st.markdown("---")
st.caption("🗺️ Map Data: Open Source GeoJSON | 📊 Sample Data for Demonstration")
