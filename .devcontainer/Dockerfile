# Utiliser une image de base Python officielle
FROM mcr.microsoft.com/vscode/devcontainers/python:3.9

# Mettre à jour apt et installer les dépendances système en une seule commande ROBUSTE
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    google-chrome-stable \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Installer ChromeDriver de manière propre
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    chmod +x chromedriver && \
    mv -f chromedriver /usr/local/bin/chromedriver

# Définir la variable d'environnement pour l'écran virtuel
ENV DISPLAY=:99

# Installer les dépendances Python DIRECTEMENT avec pip
# Plus besoin du fichier requirements.txt
RUN pip install --no-cache-dir selenium requests
