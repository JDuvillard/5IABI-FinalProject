from Preprocess import split_stations
from Process import find_competitors, kpi, map_display, price_comparison, price_curves
import streamlit as st
import pandas as pd

# Placer st.set_page_config en premier
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.title('Analyse des Stations-Service')

    # Charger le CSS personnalisé
    load_css('styles/style.css')

    # Initialiser l'état de la barre latérale dans st.session_state
    if 'show_sidebar' not in st.session_state:
        st.session_state.show_sidebar = True

    # Bouton pour basculer l'affichage de la barre latérale
    if st.button('Afficher/Masquer la barre latérale'):
        st.session_state.show_sidebar = not st.session_state.show_sidebar

    if st.session_state.show_sidebar:
        # Barre latérale
        with st.sidebar:
            st.image('styles/EcoleHexagone.png', use_container_width=True)
            st.write('Jonah DUVILLARD')
            st.write('Master 2 : IA')

    # Exécution des scripts de préparation avec des spinners
    with st.spinner('Séparation des stations en cours...'):
        split_stations.split_stations()
    st.success('Séparation des stations terminée.')

    # Sélection de la date pour les KPI
    selected_date = st.date_input('Sélectionnez une date pour les KPI')

    # Affichage des KPI
    if selected_date:
        kpi.display_kpi(selected_date)

    # Sélection de la station Carrefour
    st.header('Sélection de la Station Carrefour')
    df_carrefour = pd.read_csv('./data/Carrefour.csv', sep=';')
    station_options = df_carrefour[['id', 'Enseignes', 'Ville']].copy()
    station_options['label'] = station_options['Enseignes'] + ' - ' + station_options['Ville'] + ' (ID: ' + station_options['id'].astype(str) + ')'
    station_choice = st.selectbox('Sélectionnez une station Carrefour', station_options['label'])
    selected_station_id = station_options[station_options['label'] == station_choice]['id'].values[0]

    if selected_station_id:
        # **Ajout du slider pour le rayon de recherche**
        st.header('Paramètres de Recherche des Concurrents')
        radius = st.slider('Sélectionnez le rayon de recherche en kilomètres', min_value=1, max_value=50, value=10)

        # Recherche des concurrents pour la station sélectionnée avec le rayon choisi
        with st.spinner('Recherche des concurrents en cours...'):
            find_competitors.find_competitors(selected_station_id, radius)
        st.success('Recherche des concurrents terminée.')

        # Affichage de la carte
        st.header('Carte des Stations')
        map_display.display_map(selected_station_id)

        # Affichage du tableau de comparaison des prix
        st.header('Tableau de Comparaison des Prix')
        price_comparison.display_price_comparison(selected_station_id)

        # Sélection de la plage de dates pour les courbes de prix
        st.header('Courbes d\'Évolution des Prix')
        start_date = st.date_input('Date de début', key='start_date')
        end_date = st.date_input('Date de fin', key='end_date')

        if start_date and end_date:
            price_curves.display_price_curves(selected_station_id, start_date, end_date)

if __name__ == '__main__':
    main()
