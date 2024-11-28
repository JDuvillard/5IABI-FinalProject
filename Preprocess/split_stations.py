import os
import pandas as pd
import streamlit as st


def split_stations():
    # Splitting Infos_Stations.csv into Carrefour and Concurrents
    df = pd.read_csv('./data/Infos_Stations.csv', sep=',')
    df_carrefour = df[df['Enseignes'].str.contains('Carrefour', na=False)]
    df_concurrents = df[~df['Enseignes'].str.contains('Carrefour', na=False)]
    df_carrefour.to_csv('./data/Carrefour.csv', index=False, sep=';')
    df_concurrents.to_csv('./data/Concurrents.csv', index=False, sep=';')

    # Vérifier si les fichiers splittés de prix existent déjà
    prix_part1_exists = os.path.exists('./data/Prix_Part1.csv')
    prix_part2_exists = os.path.exists('./data/Prix_Part2.csv')

    if prix_part1_exists and prix_part2_exists:
        st.success('Les fichiers Prix_Part1.csv et Prix_Part2.csv existent déjà.')
        # Pas besoin de Prix_2024.csv, on peut continuer
        return
    else:
        # Vérifier si Prix_2024.csv existe
        if os.path.exists('./data/Prix_2024.csv'):
            # Lecture du fichier Prix_2024.csv
            df = pd.read_csv('./data/Prix_2024.csv', sep=',')

            # Calcul du point de division
            split_index = len(df) // 2

            # Division du DataFrame en deux parties
            df_part1 = df.iloc[:split_index]
            df_part2 = df.iloc[split_index:]

            # Enregistrement des deux parties dans des fichiers CSV séparés
            df_part1.to_csv('./data/Prix_Part1.csv', index=False, sep=',')
            df_part2.to_csv('./data/Prix_Part2.csv', index=False, sep=',')

            st.success('Le fichier Prix_2024.csv a été divisé en deux fichiers : Prix_Part1.csv et Prix_Part2.csv')
        else:
            # Prix_2024.csv n'existe pas, afficher un message d'erreur
            st.error('Le fichier Prix_2024.csv est nécessaire pour poursuivre.')
            st.stop()  # Arrêter l'exécution du script
