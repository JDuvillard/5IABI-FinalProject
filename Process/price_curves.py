# price_curves.py

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import json


def display_price_curves(selected_station_id, start_date, end_date):
    # Lire les deux parties du fichier de prix
    df_prix_part1 = pd.read_csv('./data/Prix_Part1.csv', sep=',')
    df_prix_part2 = pd.read_csv('./data/Prix_Part2.csv', sep=',')
    # Combiner les deux parties
    df_prix = pd.concat([df_prix_part1, df_prix_part2], ignore_index=True)

    # Lire les informations des stations
    df_infos = pd.read_csv('./data/Infos_Stations.csv', sep=',')

    # Fusionner les données de prix avec les informations des stations
    df = pd.merge(df_prix, df_infos, on='id')

    # Convertir les dates en format datetime
    df['Date'] = pd.to_datetime(df['Date'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Charger les informations des concurrents
    with open('./output/competitors.json', 'r') as f:
        competitors_info = json.load(f)
    competitor_ids = [comp['id_station'] for comp in competitors_info[str(selected_station_id)]]
    competitor_ids.append(selected_station_id)

    # Filtrer les données pour les stations sélectionnées
    df = df[df['id'].isin(competitor_ids)]
    # Filtrer les données pour la plage de dates sélectionnée
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Colonnes des carburants
    carburant_cols = ['Gazole', 'SP95', 'SP98', 'E10', 'E85', 'GPLc']

    # Transformation en format long
    df_long = df.melt(
        id_vars=['Date', 'id', 'Enseignes', 'Ville'],
        value_vars=carburant_cols,
        var_name='type_carburant',
        value_name='prix'
    )

    # Suppression des valeurs manquantes et des prix égaux à zéro
    df_long = df_long.dropna(subset=['prix'])
    df_long = df_long[df_long['prix'] > 0]

    # Liste des carburants disponibles
    carburants = df_long['type_carburant'].unique()

    for carburant in carburants:
        st.subheader(f'Évolution des prix pour {carburant}')
        df_carburant = df_long[df_long['type_carburant'] == carburant]

        if df_carburant.empty:
            st.write(f"Aucune donnée disponible pour le carburant {carburant} dans la période sélectionnée.")
            continue

        plt.figure(figsize=(10, 5))

        for station_id in df_carburant['id'].unique():
            station_data = df_carburant[df_carburant['id'] == station_id]
            station_name = df_infos[df_infos['id'] == station_id]['Enseignes'].values[0]
            plt.plot(station_data['Date'], station_data['prix'], label=f"{station_name} (ID: {station_id})")

        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Prix (€)')
        plt.title(f'Évolution des prix pour {carburant}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)
        plt.close()
