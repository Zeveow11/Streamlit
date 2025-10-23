import streamlit as st
import plotly.express as px
import pandas as pd
import json
import requests

st.set_page_config(page_title="Kazakhstan Regions Map", page_icon="🗺️", layout="wide")

st.title("🗺️ Kazakhstan Regional Map")
st.markdown("### Interactive map showing all regions (oblasts) of Kazakhstan")

# Load Kazakhstan GeoJSON
@st.cache_data
def load_geojson():
    # Alternative working URL
    url = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/kazakhstan/kazakhstan-regions.json"
    response = requests.get(url)
    return response.json()

# Sample data for regions
@st.cache_data
def load_region_data():
    regions = {
        'id': ['KZ-10', 'KZ-75', 'KZ-19', 'KZ-11', 'KZ-15', 'KZ-23', 'KZ-27', 
               'KZ-31', 'KZ-33', 'KZ-35', 'KZ-39', 'KZ-43', 'KZ-47', 'KZ-55', 
               'KZ-59', 'KZ-61', 'KZ-62', 'KZ-63', 'KZ-71', 'KZ-79'],
        'name': ['Abai', 'Astana', 'Akmola', 'Aktobe', 'Almaty', 'Almaty Region',
                 'Atyrau', 'East Kazakhstan', 'Jetisu', 'West Kazakhstan', 'Karaganda',
                 'Kostanay', 'Kyzylorda', 'Mangystau', 'Pavlodar', 'North Kazakhstan',
                 'Ulytau', 'Turkestan', 'Shymkent', 'Zhambyl'],
        'cars': [120000, 280000, 180000, 210000, 450000, 480000,
                 150000, 320000, 160000, 160000, 310000,
                 200000, 190000, 170000, 180000, 130000, 
                 90000, 450000, 240000, 260000],
        'population': [450000, 1200000, 750000, 900000, 2000000, 2100000,
                       650000, 1400000, 620000, 680000, 1380000,
                       880000, 820000, 720000, 750000, 550000,
                       280000, 2000000, 1100000, 1150000]
    }
    return pd.DataFrame(regions)

try:
    geojson = load_geojson()
    df = load_region_data()
    
    # Sidebar
    st.sidebar.header("🎛️ Map Settings")
    
    metric_choice = st.sidebar.selectbox(
        "Choose metric to display",
        ["Number of Cars", "Population", "Cars per 1000 people"]
    )
    
    color_scheme = st.sidebar.selectbox(
        "Color Scheme",
        ["Viridis", "Blues", "Reds", "Greens", "Plasma", "Turbo", "YlOrRd"]
    )
    
    # Calculate metric
    if metric_choice == "Cars per 1000 people":
        df['metric'] = (df['cars'] / df['population'] * 1000).round(1)
        metric_label = 'Cars per 1000 people'
    elif metric_choice == "Population":
        df['metric'] = df['population']
        metric_label = 'Population'
    else:
        df['metric'] = df['cars']
        metric_label = 'Number of Cars'
    
    # Create map
    fig = px.choropleth(
        df,
        geojson=geojson,
        locations='id',
        featureidkey="properties.code",
        color='metric',
        color_continuous_scale=color_scheme,
        hover_name='name',
        hover_data={
            'id': False,
            'name': True,
            'population': ':,',
            'cars': ':,',
            'metric': ':,.1f'
        },
        labels={'metric': metric_label},
        title=f"Kazakhstan Regions - {metric_choice}"
    )
    
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        center={"lat": 48, "lon": 68}
    )
    
    fig.update_layout(
        height=700,
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
except Exception as e:
    st.error(f"Choropleth map failed: {str(e)}")
    st.info("Showing alternative scatter map visualization...")
    
    # Fallback to scatter geo map
    df = load_region_data()
    
    # Approximate coordinates for regions
    coords = {
        'Astana': (51.1694, 71.4491),
        'Almaty': (43.2220, 76.8512),
        'Shymkent': (42.3000, 69.6000),
        'Akmola': (51.1801, 71.4460),
        'Aktobe': (50.2839, 57.1670),
        'Almaty Region': (43.2567, 76.9286),
        'Atyrau': (47.1164, 51.8830),
        'East Kazakhstan': (49.9481, 82.6278),
        'West Kazakhstan': (51.2145, 51.3572),
        'Karaganda': (49.8047, 73.1094),
        'Kostanay': (53.2144, 63.6246),
        'Kyzylorda': (44.8528, 65.5089),
        'Mangystau': (44.5167, 54.0167),
        'Pavlodar': (52.2873, 76.9674),
        'North Kazakhstan': (54.8667, 69.1667),
        'Turkestan': (43.3000, 68.2500),
        'Zhambyl': (42.9000, 71.3667),
        'Jetisu': (45.0167, 78.3667),
        'Abai': (49.6500, 77.8667),
        'Ulytau': (48.5667, 66.5667)
    }
    
    df['lat'] = df['name'].map(lambda x: coords.get(x, (48, 68))[0])
    df['lon'] = df['name'].map(lambda x: coords.get(x, (48, 68))[1])
    
    fig = px.scatter_geo(
        df,
        lat='lat',
        lon='lon',
        size='cars',
        color='cars',
        hover_name='name',
        hover_data={
            'cars': ':,',
            'population': ':,',
            'lat': False,
            'lon': False
        },
        size_max=40,
        color_continuous_scale='Viridis',
        title='Kazakhstan Car Distribution by Region (Bubble Map)'
    )
    
    fig.update_geos(
        center=dict(lat=48, lon=68),
        projection_scale=3.5,
        visible=True,
        resolution=50,
        showcountries=True,
        countrycolor="lightgray",
        showland=True,
        landcolor="lightgray"
    )
    
    fig.update_layout(height=700)
    
    st.plotly_chart(fig, use_container_width=True)

# Statistics
st.markdown("---")
st.markdown("### 📊 Regional Statistics")

df = load_region_data()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Population", f"{df['population'].sum():,}")

with col2:
    st.metric("Total Cars", f"{df['cars'].sum():,}")

with col3:
    st.metric("Average Cars/1000", f"{(df['cars'].sum() / df['population'].sum() * 1000):.1f}")

with col4:
    st.metric("Number of Regions", len(df))

# Top regions
st.markdown("---")
st.markdown("### 🏆 Top Regions by Number of Cars")

col1, col2 = st.columns(2)

with col1:
    top_regions = df.nlargest(10, 'cars')[['name', 'cars', 'population']]
    st.dataframe(
        top_regions,
        use_container_width=True,
        column_config={
            "name": "Region",
            "cars": st.column_config.NumberColumn("Cars", format="%d"),
            "population": st.column_config.NumberColumn("Population", format="%d"),
        },
        hide_index=True
    )

with col2:
    fig_bar = px.bar(
        df.nlargest(10, 'cars'),
        x='cars',
        y='name',
        orientation='h',
        color='cars',
        color_continuous_scale='Viridis',
        labels={'cars': 'Number of Cars', 'name': 'Region'}
    )
    fig_bar.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

# Data table
st.markdown("---")
st.markdown("### 📋 Complete Regional Data")

st.dataframe(
    df.sort_values('cars', ascending=False)[['name', 'cars', 'population']],
    use_container_width=True,
    column_config={
        "name": "Region Name",
        "population": st.column_config.NumberColumn("Population", format="%d"),
        "cars": st.column_config.NumberColumn("Number of Cars", format="%d"),
    },
    hide_index=True
)

# Download
csv = df.to_csv(index=False)
st.download_button(
    label="📥 Download Regional Data",
    data=csv,
    file_name="kazakhstan_regional_cars.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("🗺️ Sample Data for Demonstration | 📊 2023 Estimates")
