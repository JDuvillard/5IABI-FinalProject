# price_comparison.py

import pandas as pd
import streamlit as st
import json


def display_price_comparison(selected_station_id):
    # Lire les deux parties du fichier de prix
    df_prix_part1 = pd.read_csv('./data/Prix_Part1.csv', sep=',')
    df_prix_part2 = pd.read_csv('./data/Prix_Part2.csv', sep=',')
    # Combiner les deux parties
    df_prix = pd.concat([df_prix_part1, df_prix_part2], ignore_index=True)

    # Lire les informations des stations
    df_infos = pd.read_csv('./data/Infos_Stations.csv', sep=',')

    # Fusionner les données de prix avec les informations des stations
    df = pd.merge(df_prix, df_infos, on='id')

    # Charger les informations des concurrents
    with open('./output/competitors.json', 'r') as f:
        competitors_info = json.load(f)
    competitor_ids = [comp['id_station'] for comp in competitors_info[str(selected_station_id)]]
    competitor_ids.append(selected_station_id)

    # Filtrer les données pour les stations sélectionnées
    df = df[df['id'].isin(competitor_ids)]

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

    # Organisation des carburants en lignes de 3 colonnes
    rows = [carburants[:3], carburants[3:]]

    for row_carburants in rows:
        cols = st.columns(3)
        for col, carburant in zip(cols, row_carburants):
            with col:
                st.subheader(f'Comparaison des prix pour {carburant}')
                df_carburant = df_long[df_long['type_carburant'] == carburant]
                latest_date = df_carburant['Date'].max()
                df_latest = df_carburant[df_carburant['Date'] == latest_date]

                df_latest = df_latest.sort_values('prix', ascending=True)
                df_latest.reset_index(drop=True, inplace=True)

                if df_latest.empty:
                    st.write('Aucun prix disponible pour ce carburant.')
                else:
                    def highlight_row(row):
                        color = 'background-color: lightgreen' if row['id'] == selected_station_id else ''
                        return [color] * len(row)

                    st.dataframe(df_latest.style.apply(highlight_row, axis=1), use_container_width=True)
