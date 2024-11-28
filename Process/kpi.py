# kpi.py

import pandas as pd
import streamlit as st


def display_kpi(selected_date):
    with st.spinner('Calcul des KPI en cours...'):
        # Lire les deux parties du fichier de prix
        df_prix_part1 = pd.read_csv('./data/Prix_Part1.csv', sep=',')
        df_prix_part2 = pd.read_csv('./data/Prix_Part2.csv', sep=',')
        # Combiner les deux parties
        df_prix = pd.concat([df_prix_part1, df_prix_part2], ignore_index=True)

        # Lire les informations des stations
        df_infos = pd.read_csv('./data/Infos_Stations.csv', sep=',')

        # Conversion des dates
        df_prix['Date'] = pd.to_datetime(df_prix['Date'])
        selected_date = pd.to_datetime(selected_date)

        # Fusionner les données de prix avec les informations des stations
        df = pd.merge(df_prix, df_infos, on='id')

        # Filtrer les données pour la date sélectionnée
        df = df[df['Date'] == selected_date]

        # Vérifier si des données sont disponibles pour la date sélectionnée
        if df.empty:
            st.warning(f"Aucune donnée disponible pour la date sélectionnée : {selected_date.strftime('%Y-%m-%d')}")
            return

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

        # Liste des enseignes à considérer
        enseignes = df_long['Enseignes'].unique()

        # Liste des carburants disponibles
        carburants = df_long['type_carburant'].unique()

        for carburant in carburants:
            st.subheader(f'Prix moyen pour {carburant}')
            df_carburant = df_long[df_long['type_carburant'] == carburant]
            prix_moyen = df_carburant.groupby('Enseignes')['prix'].mean()
            prix_moyen = prix_moyen.dropna()
            if prix_moyen.empty:
                st.write(f"Aucune donnée disponible pour le carburant {carburant} à la date sélectionnée.")
            else:
                st.bar_chart(prix_moyen, use_container_width=True)
        st.success('Calcul des KPI terminé.')
