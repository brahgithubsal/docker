# Dockerfile — Recette de construction de l'image de production
FROM python:3.12-slim

# 1. Définir le répertoire de travail dans le conteneur
WORKDIR /app

# 2. Copier D'ABORD les dépendances seules pour exploiter le cache Docker
COPY requirements.txt .

# 3. Installer les packages sans stocker le cache pip (réduction de taille)
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copier ensuite le code source applicatif
COPY src/ ./src/

# 5. Documenter le port sur lequel l'application écoute
EXPOSE 5000

# 6. Sécurité non-root : utiliser un utilisateur système non privilégié
USER nobody

# 7. Commande d'exécution au démarrage (format JSON exec obligatoire)
CMD ["python", "src/app.py"]
