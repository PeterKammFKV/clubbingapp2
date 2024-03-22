#!/usr/bin/env python
# coding: utf-8

# In[19]:


import streamlit as st
import osmnx as ox
import folium
from streamlit_folium import folium_static
from shapely.geometry import Point

def plot_night_clubs(city):
    # Retrieve night clubs using Overpass API
    night_clubs = ox.geometries_from_place(city, tags={'amenity': 'nightclub'})

    # Filter out non-Point geometries
    night_clubs = night_clubs[night_clubs['geometry'].apply(lambda x: isinstance(x, Point))]

    # Retrieve city boundary
    city_boundary = ox.geocode_to_gdf(city)

    # Plot the city and night clubs on an interactive map
    m = folium.Map(location=[night_clubs['geometry'].apply(lambda p: p.y).mean(), night_clubs['geometry'].apply(lambda p: p.x).mean()], zoom_start=12, tiles='cartodbpositron')

    # Add city boundary to the map
    folium.GeoJson(city_boundary.to_json(), style_function=lambda feature: {
                   'fillColor': '#FAFAFA',  # Fill color of the boundary
                   'color': 'black',      # Border color of the boundary
                   'weight': 2,           # Border width of the boundary
                   'fillOpacity': 0.2     # Opacity of the filled area
               }) .add_to(m)

    # Add night clubs as dots on the map
    for idx, row in night_clubs.iterrows():
        folium.CircleMarker(location=[row['geometry'].y, row['geometry'].x], radius=3, color='red', fill=True, fill_color='black', fill_opacity=0.7, popup=row['name']).add_to(m)

    # Add night clubs as dots on the map
    for idx, row in night_clubs.iterrows():
        popup_text = f"{row['name']}"
        folium.CircleMarker(location=[row['geometry'].y, row['geometry'].x], 
                            radius=3, 
                            color='red', 
                            fill=True, 
                            fill_color='black', 
                            fill_opacity=0.7, 
                            popup=folium.Popup(popup_text)).add_to(m)
    # Display the map
    folium_static(m)

    # Print the map file path with a customized background color
    st.markdown(f'<p style="background-color:#ECECEC">Night clubs in {city}, enjoy.</p>', unsafe_allow_html=True)

# Streamlit app title
st.title("Let's go clubbing!")

# Get user input for city name
city = st.text_input("Enter the city name:")

# Check if city name is provided
if city:
    plot_night_clubs(city)
    
    
# Add GIF at the bottom of the page
st.image("ClubingDance.gif", use_column_width='auto', caption="ronimo ronimo")


# In[ ]:




