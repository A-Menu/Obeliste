# L'Obéliste

Durant l'Antiquité, Rome compta au moins quinze obélisques en son sein ; ***l'Obéliste*** vous propose de
découvrir d'élévation en élévation les déplacements des treize obélisques antiques encore présents dans la ville.

<p align="center"><img width="923" alt="obeliste" src="https://user-images.githubusercontent.com/92547721/166152084-74720394-0caa-41ae-9d87-5be816ca05a2.png"></p>

## À propos

L'Obéliste est une application web réalisée sous Python à l'aide de Flask et SQLAlchemy.

Visant à gérer et visualiser une base de données relationnelle, elle a été créée dans le cadre
du [cours d'Introduction au développement applicatif](github.com/ponteineptique/cours-python) dispensé par M. Thibault
Clérice au Master
2 ["Technologies numériques appliquées à l'histoire"](https://www.chartes.psl.eu/fr/cursus/master-technologies-numeriques-appliquees-histoire)
de l'[École nationale des chartes](https://www.chartes.psl.eu/fr).

### Fonctionnalités

- Une page descriptive par obélisque, commanditaire et lieu recensé dans la base
- Cinq index : intégralité des obélisques, obélisques égyptiens, obélisques romains, commanditaires, lieux
- Plusieurs types de cartes permettant de visualiser les divers lieux où les obélisques ont été élevés
- De la recherche plein texte sur les pages des obélisques

- Une fois inscrit et connecté, possibilité d'ajouter, modifier ou supprimer de la base de données les obélisques, commanditaires, lieux et élévations


## Installation Linux

- Cloner ou enregistrer le dépôt GitHub à l'emplacement voulu
- Se déplacer dans le dossier
- Si besoin, installer les prérequis Python : `sudo apt-get install python3 libfreetype6-dev python3-pip python3-virtualenv`
- Créer un environnement virtuel : `virtualenv ~/.obeliste -p python3`
- Activer l'environnement virtuel : `source ~/.obeliste/bin/activate` (à activer à chaque fois que vous désirez ouvrir
  l'application)
- Installer les dépendances requises : `pip install -r requirements.txt`
- Lancer l'application : `python3 run.py`
- Pour visualiser l'application, se rendre à l'adresse suivante : [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
