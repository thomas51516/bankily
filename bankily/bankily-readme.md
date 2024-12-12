Flask Application Deployment

Prérequis

Assurez-vous d'avoir les outils suivants installés sur votre système :

Python : Version 3.10 ou supérieure

Pip : Le gestionnaire de paquets Python

Installation

Clonez le dépôt :

git clone <URL_DU_DEPOT>
cd <NOM_DU_DEPOT>

Créez un environnement virtuel (recommandé) :

python3 -m venv env
source env/bin/activate  # Sous Windows : env\Scripts\activate

Installez les dépendances :

pip install -r requirements.txt

Base de données

Cette application utilise SQLite comme base de données. Le fichier de la base de données sera généré automatiquement au premier lancement de l'application.

Si vous avez besoin de préparer ou migrer la base de données, exécutez le script approprié (s'il existe) ou consultez la documentation de l'application.

Démarrage de l'application

Lancez l'application :

python app.py

Accédez à l'application :

Par défaut, l'application sera disponible à l'adresse suivante :

http://127.0.0.1:5000

Structure du projet

app.py : Point d'entrée principal de l'application.

templates/ : Contient les fichiers HTML.

static/ : Contient les ressources statiques comme CSS, JS, images, etc.

requirements.txt : Liste des dépendances Python.

instance/ : Contient la base de données SQLite et d'autres fichiers de configuration (généré automatiquement).

Environnement de production

Pour exécuter l'application Flask en mode production, utilisez un serveur WSGI comme Gunicorn ou uWSGI.

Installation de Gunicorn :

pip install gunicorn

Lancement de l'application :

gunicorn -w 4 -b 0.0.0.0:8000 app:app

Remplacez 4 par le nombre de workers souhaités.

Contribution

Forkez le dépôt

Créez une branche pour vos modifications :

git checkout -b feature/nom-de-la-feature

Soumettez une pull request

Support

Pour toute question ou assistance, veuillez contacter votre.email@example.com.

Licence

Ce projet est sous licence MIT.


