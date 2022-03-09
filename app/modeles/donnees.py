import datetime
from .. app import db

#On crée une classe Obelisque
class Obelisque(db.Model):
    obelisque_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    obelisque_nom = db.Column(db.Text)
    #Hauteur de l'obélisque
    obelisque_hauteur = db.Column(db.Float)
    #Hauteur totale
    obelisque_hauteur_avec_base = db.Column(db.Float)
    obelisque_materiau = db.Column(db.Text)
    #L'obélisque est-il une commande égyptienne ou romaine ?
    obelisque_type_commande = db.Column(db.Text)
    obelisque_notice = db.Column(db.Text)
    obelisque_inscription_latine = db.Column(db.Text)
    obelisque_inscription_latine_traduite = db.Column(db.Text)
    obelisque_bibliographie = db.Column(db.Text)
    #Nom du fichier image (utilisé pour intégrer l'image à la page)
    obelisque_image_nom = db.Column(db.Text)
    #URL de l'image
    obelisque_image_url = db.Column(db.Text)
    #Crédits pour l'image
    obelisque_image_auteur = db.Column(db.Text)
    #Licence de l'image
    obelisque_image_licence = db.Column(db.Text)
    #Lien vers la licence
    obelisque_image_licence_url = db.Column(db.Text)
    erige = db.relationship("Erige", back_populates="obelisque")
    authorships = db.relationship("Authorship", back_populates="obelisque")

#On crée une classe Personne pour recenser ceux ayant fait ériger un obélisque
class Personne(db.Model):
    personne_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    personne_nom = db.Column(db.Text)
    personne_fonction = db.Column(db.Text)
    personne_nationalite = db.Column(db.Text)
    erige = db.relationship("Erige", back_populates="personne")
    authorships = db.relationship("Authorship", back_populates="personne")

#On crée une classe Localisation pour recenser les lieux où les obélisques ont été érigés
class Localisation(db.Model):
    localisation_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    localisation_lieu = db.Column(db.Text)
    #Le terme de "ville" est à concevoir au sens large, il s'agit d'indiquer ici une référence plus précise que le pays, mais moins précise que le lieu exact.
    #On y renseigne la ville si le lieu d'évélation en possède une, mais on y retrouve également des termes tels que "Voie Appienne" (donc une route)
    #ou "Karnak" (un complexe)
    localisation_ville = db.Column(db.Text)
    localisation_pays = db.Column(db.Text)
    localisation_longitude = db.Column(db.Float)
    localisation_latitude = db.Column(db.Float)
    erige = db.relationship("Erige", back_populates="localisation")
    authorships = db.relationship("Authorship", back_populates="localisation")

#On crée une classe Erige servant de table de relation reliant les trois tables précédentes
class Erige(db.Model):
    __tablename__ = "erige"
    erige_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    erige_id_obelisque = db.Column(db.Integer, db.ForeignKey('obelisque.obelisque_id'))
    erige_id_personne = db.Column(db.Integer, db.ForeignKey('personne.personne_id'))
    erige_id_localisation = db.Column(db.Integer, db.ForeignKey('localisation.localisation_id'))
    erige_date = db.Column(db.Text)
    #On indique si l'enregistrement correspond à la localisation actuelle de l'obélisque (booléen, 0 = non, 1 = oui)
    erige_actuel = db.Column(db.Integer)
    obelisque = db.relationship("Obelisque", back_populates="erige")
    personne = db.relationship("Personne", back_populates="erige")
    localisation = db.relationship("Localisation", back_populates="erige")
    authorships = db.relationship("Authorship", back_populates="erige")

#On crée une classe Authorship pour recenser les modifications des utilisateurs
class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_obelisque_id = db.Column(db.Integer, db.ForeignKey('obelisque.obelisque_id'))
    authorship_personne_id = db.Column(db.Integer, db.ForeignKey('personne.personne_id'))
    authorship_localisation_id = db.Column(db.Integer, db.ForeignKey('localisation.localisation_id'))
    authorship_erige_id = db.Column(db.Integer, db.ForeignKey('erige.erige_id'))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    obelisque = db.relationship("Obelisque", back_populates="authorships")
    personne = db.relationship("Personne", back_populates="authorships")
    localisation = db.relationship("Localisation", back_populates="authorships")
    erige = db.relationship("Erige", back_populates="authorships")
    user = db.relationship("User", back_populates="authorships")