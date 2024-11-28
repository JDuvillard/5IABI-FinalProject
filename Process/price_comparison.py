import pandas as pd
import streamlit as st
import json


def display_price_comparison(selected_station_id):
    df_prix = pd.read_csv('./data/Prix_2024.csv', sep=',')
    df_infos = pd.read_csv('./data/Infos_Stations.csv', sep=',')

    df = pd.merge(df_prix, df_infos, on='id')

    with open('./output/competitors.json', 'r') as f:
        competitors_info = json.load(f)
    competitor_ids = [comp['id_station'] for comp in competitors_info[str(selected_station_id)]]
    competitor_ids.append(selected_station_id)

    df = df[df['id'].isin(competitor_ids)]

    carburant_cols = ['Gazole', 'SP95', 'SP98', 'E10', 'E85', 'GPLc']
    df_long = df.melt(
        id_vars=['Date', 'id', 'Enseignes', 'Ville'],
        value_vars=carburant_cols,
        var_name='type_carburant',
        value_name='prix'
    )

    df_long = df_long.dropna(subset=['prix'])

    df_long = df_long[df_long['prix'] > 0]

    carburants = df_long['type_carburant'].unique()

    rows = [carburants[:3], carburants[3:]]

    for row_carburants in rows:
        cols = st.columns(3)
        for col, carburant in zip(cols, row_carburants):
            with col:
                st.subheader(f'Comparaison des prix pour {carburant}')
                df_carburant = df_long[df_long['type_carburant'] == carburant]
                latest_date = df_carburant['Date'].max()
                df_latest = df_carburant[df_carburant['Date'] == latest_date]

                df_latest = df_latest[df_latest['prix'] > 0]

                df_latest = df_latest.sort_values('prix', ascending=True)
                df_latest.reset_index(drop=True, inplace=True)

                if df_latest.empty:
                    st.write('Aucun prix disponible pour ce carburant.')
                else:
                    def highlight_row(row):
                        color = 'background-color: lightgreen' if row['id'] == selected_station_id else ''
                        return [color] * len(row)

                    st.dataframe(df_latest.style.apply(highlight_row, axis=1))
