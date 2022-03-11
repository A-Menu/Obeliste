from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from .constantes import SECRET_KEY


chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics
    )
# On configure le secret
app.config['SECRET_KEY'] = SECRET_KEY
# On configure la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./obeliste.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


#On définit le lieu où sont stockées les images
UPLOAD_FOLDER = 'app/static/images/img_obelisques/'
#On définit les extensions acceptées pour télécharger des images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

#On configure le fichier pour recevoir les images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# On initie l'extension
db = SQLAlchemy(app)

# On met en place la gestion d'utilisateur-rice-s
login = LoginManager(app)


from .routes import generic
from .routes import api