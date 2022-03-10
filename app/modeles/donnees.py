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

    @staticmethod
    def obelisque_add(obelisque_add_nom, obelisque_add_hauteur, obelisque_add_hauteur_avec_base, obelisque_add_materiau, obelisque_add_type_commande, obelisque_add_notice, obelisque_add_inscription_latine, obelisque_add_inscription_latine_traduite, obelisque_add_bibliographie, obelisque_add_image_nom, obelisque_add_image_url, obelisque_add_image_auteur, obelisque_add_image_licence, obelisque_add_image_licence_url):
        erreurs = []
        if not obelisque_add_nom:
            erreurs.append("veuillez renseigner le nom de l'obélisque")
        if not obelisque_add_hauteur:
            erreurs.append( "veuillez renseigner la hauteur de l'obélisque")
        if not obelisque_add_hauteur_avec_base:
            erreurs.append("veuillez renseigner la hauteur totale du monument")
        if not obelisque_add_materiau:
           erreurs.append("veuillez renseigner le matériau composant l'obélisque")
        if not obelisque_add_type_commande:
            erreurs.append("veuillez renseigner le type de commande")
        if not obelisque_add_notice:
            erreurs.append("veuillez renseigner une brève notice sur l'obélisque")
        if not obelisque_add_bibliographie:
            erreurs.append("veuillez renseigner vos sources")
        if not obelisque_add_image_nom:
            erreurs.append("veuillez renseigner une image de l'obélisque")
        if not obelisque_add_image_url:
            erreurs.append("veuillez renseigner l'URL de l'image")
        if not obelisque_add_image_auteur:
            erreurs.append("veuillez renseigner l'ayant-droit de l'image")
        if not obelisque_add_image_licence:
            erreurs.append("veuillez renseigner la licence permettant la réutilisation de l'image")
        if not obelisque_add_image_licence_url:
            erreurs.append("veuillez renseigner l'URL de la licence")

            # S'il y a au moins une erreur, afficher un message d'erreur.
        if len(erreurs) > 0:
            return False, erreurs

            # Si aucune erreur n'a été détectée, ajout d'une nouvelle entrée dans la table Obelisque
        ajoutable = Obelisque(obelisque_nom=obelisque_add_nom,
                              obelisque_hauteur=obelisque_add_hauteur,
                              obelisque_hauteur_avec_base=obelisque_add_hauteur_avec_base,
                              obelisque_materiau=obelisque_add_materiau,
                              obelisque_type_commande=obelisque_add_type_commande,
                              obelisque_notice=obelisque_add_notice,
                              obelisque_inscription_latine=obelisque_add_inscription_latine,
                              obelisque_inscription_latine_traduite=obelisque_add_inscription_latine_traduite,
                              obelisque_bibliographie=obelisque_add_bibliographie,
                              obelisque_image_nom=obelisque_add_image_nom,
                              obelisque_image_url=obelisque_add_image_url,
                              obelisque_image_auteur=obelisque_add_image_auteur,
                              obelisque_image_licence=obelisque_add_image_licence,
                              obelisque_image_licence_url=obelisque_add_image_licence_url,
                              )

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(ajoutable)
            db.session.commit()
            return True, ajoutable

        except Exception as erreur:
            return False, [str(erreur)]

#On crée une classe Personne pour recenser ceux ayant fait ériger un obélisque
class Personne(db.Model):
    personne_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    personne_nom = db.Column(db.Text)
    personne_fonction = db.Column(db.Text)
    personne_nationalite = db.Column(db.Text)
    erige = db.relationship("Erige", back_populates="personne")
    authorships = db.relationship("Authorship", back_populates="personne")

    @staticmethod
    def personne_add(personne_add_nom, personne_add_fonction, personne_add_nationalite):
        erreurs = []
        if not personne_add_nom:
            erreurs.append("veuillez renseigner le nom du commanditaire")
        if not personne_add_fonction:
            erreurs.append(
                "veuillez renseigner les fonctions du commanditaire")
        if not personne_add_nationalite:
            erreurs.append(
                "veuillez renseigner la nationalité du commanditaire")

            # S'il y a au moins une erreur, afficher un message d'erreur.
        if len(erreurs) > 0:
            return False, erreurs

            # Si aucune erreur n'a été détectée, ajout d'une nouvelle entrée dans la table Personne
        ajoutable = Personne(personne_nom=personne_add_nom,
                             personne_fonction=personne_add_fonction,
                             personne_nationalite=personne_add_nationalite)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(ajoutable)
            db.session.commit()
            return True, ajoutable

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def personne_update(personne_nom, personne_fonction, personne_nationalite):
        erreurs = []
        if not personne_nom:
            erreurs.append("veuillez renseigner le nom du commanditaire")
        if not personne_nationalite:
            erreurs.append("veuillez renseigner la nationalité du commanditaire")

        # S'il y a au moins une erreur.
        if len(erreurs) > 0:
            return False, erreurs

        # On récupère une personne dans la base.
        editable = Personne.query.get(personne_id)

        # On vérifie que l'utilisateur-ice modifie au moins un champ.
        if editable.personne_nom == personne_nom \
                and editable.personne_fonction == personne_fonction \
                and editable.personne_nationalite == personne_nationalite :
            erreurs.append("No edit was submitted")

        if len(erreurs) > 0:
            return False, erreurs

        else:
            # Mise à jour du site
            editable.personne_nom = personne_nom
            editable.personne_fonction = personne_fonction
            editable.personne_nationalite = personne_nationalite

        try:
            # On l'ajoute au transport vers la base de données.
            db.session.add(editable)
            # On envoie le paquet.
            db.session.commit()

            # On renvoie les informations du site.
            return True, editable
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def personne_delete(personne_id):
        """
        Fonction qui permet de supprimer une personne de la base.
        :param personne_id: id de la personne (int)
        :return:
        """
        supprimable = Personne.query.get(personne_id)

        try:
            db.session.delete(supprimable)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


#On crée une classe Localisation pour recenser les lieux où les obélisques ont été érigés
class Localisation(db.Model):
    localisation_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    localisation_lieu = db.Column(db.Text)
    #Le terme de "ville" est à concevoir au sens large, il s'agit d'indiquer ici une référence plus précise que le pays, mais moins précise que le lieu exact.
    #On y renseigne la ville si le lieu d'évélation en possède une, mais on y retrouve également des termes tels que "Voie Appienne" (donc une route)
    #ou "Karnak" (un complexe)
    localisation_ville = db.Column(db.Text)
    localisation_pays = db.Column(db.Text)
    localisation_longitude = db.Column(db.Text)
    localisation_latitude = db.Column(db.Text)
    erige = db.relationship("Erige", back_populates="localisation")
    authorships = db.relationship("Authorship", back_populates="localisation")

    @staticmethod
    def localisation_add(localisation_add_lieu, localisation_add_ville, localisation_add_pays, localisation_add_latitude, localisation_add_longitude):
        erreurs = []
        if not localisation_add_lieu:
            erreurs.append("Veuillez renseigner le nom du lieu")
        if not localisation_add_ville:
            erreurs.append(
                "Veuillez renseigner le nom de la ville")
        if not localisation_add_pays:
            erreurs.append(
                "Veuillez renseigner le nom du pays")

            # S'il y a au moins une erreur, afficher un message d'erreur.
        if len(erreurs) > 0:
            return False, erreurs

            # Si aucune erreur n'a été détectée, ajout d'une nouvelle entrée dans la table Localisation
        ajoutable = Localisation(localisation_lieu=localisation_add_lieu,
                             localisation_ville=localisation_add_ville,
                             localisation_pays=localisation_add_pays,
                                 localisation_latitude=localisation_add_latitude,
                                 localisation_longitude=localisation_add_longitude)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(ajoutable)
            db.session.commit()
            return True, ajoutable

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def localisation_update(localisation_lieu, localisation_ville, localisation_pays, localisation_latitude, localisation_longitude):
        erreurs = []
        if not localisation_lieu:
            erreurs.append("veuillez renseigner le nom du lieu")
        if not localisation_ville:
            erreurs.append("veuillez renseigner le nom de la ville où se trouve le lieu")
        if not localisation_pays:
            erreurs.append("veuillez renseigner le pays où se trouve le lieu")

        # S'il y a au moins une erreur.
        if len(erreurs) > 0:
            return False, erreurs

        # On récupère une personne dans la base.
        editable = Localisation.query.get(localisation_id)

        # On vérifie que l'utilisateur-ice modifie au moins un champ.
        if editable.localisation_lieu == localisation_lieu \
                and editable.localisation_ville == localisation_ville \
                and editable.localisation_pays == localisation_pays\
                and editable.localisation_latitude == localisation_latitude\
                and editable.localisation_longitude == localisation_longitude :
            erreurs.append("No edit was submitted")

        if len(erreurs) > 0:
            return False, erreurs

        else:
            # Mise à jour du lieu
            editable.localisation_lieu = localisation_lieu
            editable.localisation_ville = localisation_ville
            editable.localisation_pays = localisation_pays
            editable.localisation_latitude = localisation_latitude
            editable.localisation_longitude = localisation_longitude

        try:
            # On l'ajoute au transport vers la base de données.
            db.session.add(editable)
            # On envoie le paquet.
            db.session.commit()

            # On renvoie les informations du site.
            return True, editable
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def localisation_delete(localisation_id):
        """
        Fonction qui permet de supprimer une personne de la base.
        :param personne_id: id de la personne (int)
        :return:
        """
        supprimable = Localisation.query.get(localisation_id)

        try:
            db.session.delete(supprimable)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


#On crée une classe Erige servant de table de relation reliant les trois tables précédentes
class Erige(db.Model):
    __tablename__ = "erige"
    erige_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    erige_id_obelisque = db.Column(db.Integer, db.ForeignKey('obelisque.obelisque_id'))
    erige_id_personne = db.Column(db.Integer, db.ForeignKey('personne.personne_id'))
    erige_id_localisation = db.Column(db.Integer, db.ForeignKey('localisation.localisation_id'))
    erige_date = db.Column(db.Text)
    #On indique si l'enregistrement correspond à la localisation actuelle de l'obélisque (booléen, 0 = non, 1 = oui)
    erige_actuel = db.Column(db.Boolean, default=0)
    obelisque = db.relationship("Obelisque", back_populates="erige")
    personne = db.relationship("Personne", back_populates="erige")
    localisation = db.relationship("Localisation", back_populates="erige")
    authorships = db.relationship("Authorship", back_populates="erige")

#On crée une classe Authorship pour recenser les modifications des utilisateurs
class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    authorship_obelisque_id = db.Column(db.Integer, db.ForeignKey('obelisque.obelisque_id'), nullable=True)
    authorship_personne_id = db.Column(db.Integer, db.ForeignKey('personne.personne_id'), nullable=True)
    authorship_localisation_id = db.Column(db.Integer, db.ForeignKey('localisation.localisation_id'), nullable=True)
    authorship_erige_id = db.Column(db.Integer, db.ForeignKey('erige.erige_id'), nullable=True)
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    obelisque = db.relationship("Obelisque", back_populates="authorships")
    personne = db.relationship("Personne", back_populates="authorships")
    localisation = db.relationship("Localisation", back_populates="authorships")
    erige = db.relationship("Erige", back_populates="authorships")
    user = db.relationship("User", back_populates="authorships")