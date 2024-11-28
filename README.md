# Projet d'Analyse des Stations-Service
## Introduction
Ce projet est une application Streamlit permettant d'analyser les stations-service, en particulier les stations Carrefour et leurs concurrents. L'application offre des fonctionnalités telles que :

- Affichage des KPI (indicateurs clés de performance) pour une date sélectionnée.
- Carte interactive montrant une station Carrefour sélectionnée et ses concurrents à proximité.
- Comparaison des prix des carburants entre la station Carrefour sélectionnée et ses concurrents.
- Courbes d'évolution des prix des carburants sur une période sélectionnée.

## Installation et Exécution du Projet avec Docker
### Prérequis
- Docker doit être installé sur votre machine.
- Git (facultatif) si vous souhaitez cloner le projet depuis un dépôt distant.

### Étapes à Suivre
1. Cloner le Dépôt du Projet
```bash
git clone https://github.com/JDuvillard/5IABI-FinalProject.git
```
2. Se Placer dans le Répertoire du Projet
```bash
cd 5IABI-FinalProject
```
3. Mettez les fichiers `Infos_Stations.csv` et `Prix_2024.csv` dans le dossier `data`

4. Construire l'Image Docker
```bash
docker build -t 5IABI-FinalProject .
```
- Remplacez `nom-de-votre-image` par le nom que vous souhaitez donner à votre image Docker.
- Le `.` indique que le `Dockerfile` se trouve dans le répertoire courant.
5. Exécuter le Conteneur Docker
```bash
docker run -p 8501:8501 5IABI-FinalProject
```
- L'option `-p 8501:8501` mappe le port 8501 du conteneur au port 8501 de votre machine hôte, permettant d'accéder à l'application depuis votre navigateur.
6. Accéder à l'Application
Ouvrez votre navigateur web et accédez à l'adresse suivante :

```arduino
http://localhost:8501
```
Votre application Streamlit devrait maintenant être accessible.

### Contenu du Dockerfile
Voici le contenu du Dockerfile que vous devez placer à la racine de votre projet :

```dockerfile
# Utiliser l'image de base officielle de Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code du projet dans le conteneur
COPY . .

# Exposer le port par défaut de Streamlit
EXPOSE 8501

# Lancer l'application Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
### Fichier requirements.txt
Assurez-vous d'avoir un fichier requirements.txt contenant toutes les dépendances nécessaires :

```
pandas
geopy
folium
streamlit
matplotlib
```
Vous pouvez spécifier les versions spécifiques si nécessaire :
```makefile
pandas==1.5.0
geopy==2.3.0
folium==0.12.1
streamlit==1.13.0
matplotlib==3.6.0
```
## Notes Supplémentaires
- Mise à Jour du Projet : Si vous apportez des modifications au code, vous devrez reconstruire l'image Docker :
```bash
docker build -t 5IABI-FinalProject .
```
- Arrêter le Conteneur : Pour arrêter le conteneur en cours d'exécution, utilisez CTRL + C dans le terminal ou :
```bash
docker ps
docker stop CONTAINER_ID
```
- Gestion des Données : Si votre application utilise des fichiers de données externes, assurez-vous qu'ils sont inclus dans le conteneur ou accessibles par celui-ci.
-  de Volumes (Optionnel) : Pour refléter les modifications sans reconstruire l'image :
```bash
docker run -p 8501:8501 -v $(pwd):/app 5IABI-FinalProject
```
- L'option `-v $(pwd):/app` monte le répertoire courant dans le conteneur, remplaçant le répertoire `/app` du conteneur par le vôtre.

Attention : L'utilisation de volumes peut avoir des implications sur les performances et la sécurité.

## Conclusion
Vous avez maintenant toutes les instructions nécessaires pour exécuter votre projet d'analyse des stations-service à l'aide de Docker. Si vous avez des questions ou si vous rencontrez des problèmes lors de l'installation ou de l'exécution, n'hésitez pas à me le faire savoir !