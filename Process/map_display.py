import folium
import json
import pandas as pd
import streamlit as st

def display_map(selected_station_id):
    df_carrefour = pd.read_csv('./data/Carrefour.csv', sep=';')
    with open('./output/competitors.json', 'r') as f:
        competitors_info = json.load(f)

    selected_station = df_carrefour[df_carrefour['id'] == selected_station_id].iloc[0]

    selected_latitude = selected_station['Latitude'] / 100000
    selected_longitude = selected_station['Longitude'] / 100000

    st.write(f"Coordonnées de la station sélectionnée : Latitude = {selected_latitude}, Longitude = {selected_longitude}")

    m = folium.Map(location=[selected_latitude, selected_longitude], zoom_start=12)

    folium.Marker(
        location=[selected_latitude, selected_longitude],
        popup=f"Carrefour - {selected_station['Ville']}",
        icon=folium.Icon(color='green')
    ).add_to(m)

    competitors = competitors_info[str(selected_station_id)]
    for competitor in competitors:
        folium.Marker(
            location=[competitor['Latitude'], competitor['Longitude']],
            popup=f"{competitor['enseigne']} - {competitor['ville']}",
            icon=folium.Icon(color='red')
        ).add_to(m)

    st.components.v1.html(m._repr_html_(), height=500)
