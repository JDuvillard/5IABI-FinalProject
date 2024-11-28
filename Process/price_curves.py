import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import json

def display_price_curves(selected_station_id, start_date, end_date):
    df_prix = pd.read_csv('./data/Prix_2024.csv', sep=',')
    df_infos = pd.read_csv('./data/Infos_Stations.csv', sep=',')

    df = pd.merge(df_prix, df_infos, on='id')
    df['Date'] = pd.to_datetime(df['Date'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    with open('./output/competitors.json', 'r') as f:
        competitors_info = json.load(f)
    competitor_ids = [comp['id_station'] for comp in competitors_info[str(selected_station_id)]]
    competitor_ids.append(selected_station_id)

    df = df[df['id'].isin(competitor_ids)]
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    carburant_cols = ['Gazole', 'SP95', 'SP98', 'E10', 'E85', 'GPLc']
    df_long = df.melt(
        id_vars=['Date', 'id', 'Enseignes', 'Ville'],
        value_vars=carburant_cols,
        var_name='type_carburant',
        value_name='prix'
    )

    df_long = df_long.dropna(subset=['prix'])

    carburants = df_long['type_carburant'].unique()

    for carburant in carburants:
        st.subheader(f'Évolution des prix pour {carburant}')
        df_carburant = df_long[df_long['type_carburant'] == carburant]

        plt.figure(figsize=(10, 5))
        for station_id in df_carburant['id'].unique():
            station_data = df_carburant[df_carburant['id'] == station_id]
            station_name = df_infos[df_infos['id'] == station_id]['Enseignes'].values[0]
            plt.plot(station_data['Date'], station_data['prix'], label=station_name)
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Prix')
        plt.xticks(rotation=45)
        st.pyplot(plt)
        plt.close()
