import pandas as pd
import json
from geopy.distance import geodesic
import streamlit as st

def find_competitors(selected_station_id, radius):
    df_carrefour = pd.read_csv('./data/Carrefour.csv', sep=';')
    df_concurrents = pd.read_csv('./data/Concurrents.csv', sep=';')

    carrefour_row = df_carrefour[df_carrefour['id'] == selected_station_id].iloc[0]
    carrefour_station = (
        carrefour_row['Latitude'] / 100000,
        carrefour_row['Longitude'] / 100000
    )

    competitors = []

    total_concurrents = len(df_concurrents)
    progress_bar = st.progress(0)
    progress_text = st.empty()

    for idx, concurrent_row in df_concurrents.iterrows():
        concurrent_station = (
            concurrent_row['Latitude'] / 100000,  # Diviser si nécessaire
            concurrent_row['Longitude'] / 100000
        )
        distance = geodesic(carrefour_station, concurrent_station).km
        if distance <= radius:  # Utiliser le rayon sélectionné
            competitors.append({
                'id_station': concurrent_row['id'],
                'enseigne': concurrent_row['Enseignes'],
                'ville': concurrent_row['Ville'],
                'Latitude': concurrent_row['Latitude'] / 100000,
                'Longitude': concurrent_row['Longitude'] / 100000,
                'distance': distance
            })

        progress = (idx + 1) / total_concurrents
        progress_bar.progress(progress)
        progress_text.text(f'Analyse du concurrent {idx + 1}/{total_concurrents}')

    progress_bar.empty()
    progress_text.empty()

    competitors_info = {str(selected_station_id): competitors}
    with open('./output/competitors.json', 'w') as f:
        json.dump(competitors_info, f)
