import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="Kazakhstan Map", page_icon="🗺️", layout="wide")

st.title("🗺️ Kazakhstan Regional Map")
st.markdown("### Interactive OpenStreetMap with regional data")

# Regional data
@st.cache_data
def load_data():
    data = {
        'Region': ['Almaty City', 'Astana', 'Shymkent', 'Almaty Region', 'Akmola', 
                   'Aktobe', 'Atyrau', 'East Kazakhstan', 'West Kazakhstan', 
                   'Karaganda', 'Kostanay', 'Kyzylorda', 'Mangystau', 
                   'Pavlodar', 'North Kazakhstan', 'Turkestan', 'Zhambyl'],
        'Total Cars': [450000, 280000, 240000, 480000, 180000, 210000, 150000,
                       320000, 160000, 310000, 200000, 190000, 170000,
                       180000, 130000, 450000, 260000],
        'Electric': [5000, 3500, 2000, 4000, 1500, 1800, 1200,
                     2800, 1400, 2600, 1700, 1600, 1500,
                     1550, 1100, 3800, 2200],
        'Hybrid': [12000, 8000, 5000, 10000, 3000, 4000, 2500,
                   7000, 3200, 6500, 4200, 3800, 3500,
                   3700, 2600, 9500, 5500],
        'Population': [2000000, 1200000, 1100000, 2100000, 750000, 900000, 650000,
                       1400000, 680000, 1380000, 880000, 820000, 720000,
                       750000, 550000, 2000000, 1150000],
        'Latitude': [43.2220, 51.1694, 42.3000, 43.2567, 51.1801, 50.2839, 47.1164,
                     49.9481, 51.2145, 49.8047, 53.2144, 44.8528, 44.5167,
                     52.2873, 54.8667, 43.3000, 42.9000],
        'Longitude': [76.8512, 71.4491, 69.6000, 76.9286, 71.4460, 57.1670, 51.8830,
                      82.6278, 51.3572, 73.1094, 63.6246, 65.5089, 54.0167,
                      76.9674, 69.1667, 68.2500, 71.3667]
    }
    df = pd.DataFrame(data)
    df['Cars per 1000'] = (df['Total Cars'] / df['Population'] * 1000).round(1)
    return df

df = load_data()

# Sidebar
st.sidebar.header("🎛️ Map Controls")

map_style = st.sidebar.selectbox(
    "Map Style",
    ["OpenStreetMap", "CartoDB Positron", "CartoDB Dark Matter", "Stamen Terrain", "Stamen Toner"]
)

metric = st.sidebar.selectbox(
    "Bubble Size Based On",
    ["Total Cars", "Electric", "Hybrid", "Population", "Cars per 1000"]
)

show_heatmap = st.sidebar.checkbox("Show Heatmap Layer", value=False)

# Map style mapping
tile_mapping = {
    "OpenStreetMap": "OpenStreetMap",
    "CartoDB Positron": "CartoDB positron",
    "CartoDB Dark Matter": "CartoDB dark_matter",
    "Stamen Terrain": "Stamen Terrain",
    "Stamen Toner": "Stamen Toner"
}

# Create base map
m = folium.Map(
    location=[48.0196, 66.9237],  # Center of Kazakhstan
    zoom_start=5,
    tiles=tile_mapping[map_style],
    attr='Map data'
)

# Add markers with circles
for idx, row in df.iterrows():
    # Calculate bubble size based on metric
    size_value = row[metric]
    radius = (size_value / df[metric].max()) * 50000  # Scale radius
    
    # Color based on Cars per 1000
    cars_per_capita = row['Cars per 1000']
    if cars_per_capita > 250:
        color = '#d73027'  # Red
    elif cars_per_capita > 200:
        color = '#fc8d59'  # Orange
    elif cars_per_capita > 150:
        color = '#fee08b'  # Yellow
    else:
        color = '#91bfdb'  # Blue
    
    # Create popup content
    popup_html = f"""
    <div style="font-family: Arial; width: 250px;">
        <h4 style="margin-bottom: 10px; color: #2c3e50;">{row['Region']}</h4>
        <hr style="margin: 5px 0;">
        <p style="margin: 5px 0;"><b>🚗 Total Cars:</b> {row['Total Cars']:,}</p>
        <p style="margin: 5px 0;"><b>⚡ Electric:</b> {row['Electric']:,}</p>
        <p style="margin: 5px 0;"><b>🔋 Hybrid:</b> {row['Hybrid']:,}</p>
        <p style="margin: 5px 0;"><b>👥 Population:</b> {row['Population']:,}</p>
        <p style="margin: 5px 0;"><b>📊 Cars/1000:</b> {row['Cars per 1000']:.1f}</p>
    </div>
    """
    
    # Add circle marker
    folium.Circle(
        location=[row['Latitude'], row['Longitude']],
        radius=radius,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"<b>{row['Region']}</b><br>Cars: {row['Total Cars']:,}",
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.6,
        weight=2
    ).add_to(m)
    
    # Add marker with icon
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row['Region'],
        icon=folium.Icon(color='blue' if row['Total Cars'] < 300000 else 'red', icon='car', prefix='fa')
    ).add_to(m)

# Add heatmap if selected
if show_heatmap:
    from folium.plugins import HeatMap
    heat_data = [[row['Latitude'], row['Longitude'], row['Total Cars']/10000] 
                 for idx, row in df.iterrows()]
    HeatMap(heat_data, radius=50, blur=40, max_zoom=13).add_to(m)

# Add legend
legend_html = """
<div style="position: fixed; 
     bottom: 50px; right: 50px; width: 200px; height: auto; 
     background-color: white; z-index:9999; font-size:14px;
     border:2px solid grey; border-radius: 5px; padding: 10px">
     <p style="margin: 0; font-weight: bold;">Cars per 1000 people</p>
     <p style="margin: 5px 0;"><span style="color: #d73027;">●</span> > 250</p>
     <p style="margin: 5px 0;"><span style="color: #fc8d59;">●</span> 200-250</p>
     <p style="margin: 5px 0;"><span style="color: #fee08b;">●</span> 150-200</p>
     <p style="margin: 5px 0;"><span style="color: #91bfdb;">●</span> < 150</p>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Display map
st_folium(m, width=1400, height=700)

# Statistics
st.markdown("---")
st.markdown("### 📊 Key Statistics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Population", f"{df['Population'].sum():,}")

with col2:
    st.metric("Total Cars", f"{df['Total Cars'].sum():,}")

with col3:
    st.metric("Electric Cars", f"{df['Electric'].sum():,}")

with col4:
    st.metric("Hybrid Cars", f"{df['Hybrid'].sum():,}")

with col5:
    avg_cars = (df['Total Cars'].sum() / df['Population'].sum() * 1000)
    st.metric("Avg Cars/1000", f"{avg_cars:.1f}")

# Charts
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🏆 Top 10 Regions by Total Cars")
    top_10 = df.nlargest(10, 'Total Cars')[['Region', 'Total Cars']]
    st.bar_chart(top_10.set_index('Region'))

with col2:
    st.markdown("#### ⚡ Green Vehicles Distribution")
    green_df = df[['Region', 'Electric', 'Hybrid']].set_index('Region')
    st.bar_chart(green_df)

# Data table
st.markdown("---")
st.markdown("### 📋 Regional Data")

st.dataframe(
    df[['Region', 'Total Cars', 'Electric', 'Hybrid', 'Population', 'Cars per 1000']].sort_values('Total Cars', ascending=False),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.caption("🗺️ Powered by OpenStreetMap | 📊 Sample Data 2023")
