import pandas as pd

def split_stations():
    df = pd.read_csv('./data/Infos_Stations.csv', sep=',')
    df_carrefour = df[df['Enseignes'].str.contains('Carrefour', na=False)]
    df_concurrents = df[~df['Enseignes'].str.contains('Carrefour', na=False)]
    df_carrefour.to_csv('./data/Carrefour.csv', index=False, sep=';')
    df_concurrents.to_csv('./data/Concurrents.csv', index=False, sep=';')
