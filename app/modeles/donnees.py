from flask import url_for
import datetime

from .. app import db


#On crée une classe Obelisque
class Obelisque(db.Model):
    obelisque_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    obelisque_nom = db.Column(db.Text)
    obelisque_hauteur = db.Column(db.Float)
    obelisque_hauteur_avec_base = db.Column(db.Float)
    obelisque_materiau = db.Column(db.Text)
    obelisque_type_commande = db.Column(db.Text)
    obelisque_notice = db.Column(db.Text)
    obelisque_inscription_latine = db.Column(db.Text)
    obelisque_inscription_latine_traduite = db.Column(db.Text)
    obelisque_bibliographie = db.Column(db.Text)
    obelisque_image_nom = db.Column(db.Text)
    obelisque_image_url = db.Column(db.Text)
    obelisque_image_auteur = db.Column(db.Text)
    obelisque_image_licence = db.Column(db.Text)
    obelisque_image_licence_url = db.Column(db.Text)
    erige = db.relationship("Erige", back_populates="obelisque")

#On crée une classe Personne
class Personne(db.Model):
    personne_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    personne_nom = db.Column(db.Text)
    personne_fonction = db.Column(db.Text)
    personne_nationalite = db.Column(db.Text)
    erige = db.relationship("Erige", back_populates="personne")

#On crée une classe Localisation
class Localisation(db.Model):
    localisation_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    localisation_lieu = db.Column(db.Text)
    localisation_ville = db.Column(db.Text)
    localisation_pays = db.Column(db.Text)
    localisation_longitude = db.Column(db.Float)
    localisation_latitude = db.Column(db.Float)
    erige = db.relationship("Erige", back_populates="localisation")

#On crée une classe Erige
class Erige(db.Model):
    __tablename__ = "erige"
    erige_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    erige_id_obelisque = db.Column(db.Integer, db.ForeignKey('obelisque.obelisque_id'))
    erige_id_personne = db.Column(db.Integer, db.ForeignKey('personne.personne_id'))
    erige_id_localisation = db.Column(db.Integer, db.ForeignKey('localisation.localisation_id'))
    erige_date = db.Column(db.Text)
    erige_actuel = db.Column(db.Integer)
    obelisque = db.relationship("Obelisque", back_populates="erige")
    personne = db.relationship("Personne", back_populates="erige")
    localisation = db.relationship("Localisation", back_populates="erige")