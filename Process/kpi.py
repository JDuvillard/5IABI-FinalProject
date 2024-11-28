import pandas as pd
import streamlit as st

def display_kpi(selected_date):
    with st.spinner('Calcul des KPI en cours...'):
        df_prix = pd.read_csv('./data/Prix_2024.csv', sep=',')
        df_infos = pd.read_csv('./data/Infos_Stations.csv', sep=',')

        df_prix['Date'] = pd.to_datetime(df_prix['Date'])
        selected_date = pd.to_datetime(selected_date)

        df = pd.merge(df_prix, df_infos, on='id')

        df = df[df['Date'] == selected_date]

        carburant_cols = ['Gazole', 'SP95', 'SP98', 'E10', 'E85', 'GPLc']
        df_long = df.melt(
            id_vars=['Date', 'id', 'Enseignes', 'Ville'],
            value_vars=carburant_cols,
            var_name='type_carburant',
            value_name='prix'
        )

        df_long = df_long.dropna(subset=['prix'])

        enseignes = ['Carrefour', 'Auchan', 'E.Leclerc', 'Total Access', 'Intermarché', 'Système U']
        carburants = df_long['type_carburant'].unique()

        for carburant in carburants:
            st.subheader(f'Prix moyen pour {carburant}')
            df_carburant = df_long[df_long['type_carburant'] == carburant]
            prix_moyen = df_carburant.groupby('Enseignes')['prix'].mean().reindex(enseignes)
            st.bar_chart(prix_moyen.dropna())
    st.success('Calcul des KPI terminé.')
