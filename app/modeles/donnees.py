import datetime
from ..app import db


# On crée une classe Obelisque
class Obelisque(db.Model):
    obelisque_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # Le nom de l'obélisque
    obelisque_nom = db.Column(db.Text)
    # Hauteur de l'obélisque à proprement parler
    obelisque_hauteur = db.Column(db.Float)
    # Hauteur totale du monument
    obelisque_hauteur_avec_base = db.Column(db.Float)
    # Matériau composant l'obélisque
    obelisque_materiau = db.Column(db.Text)
    # L'obélisque est-il une commande égyptienne ou romaine ?
    obelisque_type_commande = db.Column(db.Text)
    # Une brève description
    obelisque_notice = db.Column(db.Text)
    # On transcrit les inscriptions latines présentes sur l'obélisque si elles existent
    obelisque_inscription_latine = db.Column(db.Text)
    # On traduit les inscriptions latines présentes sur l'obélisque si elles existent
    obelisque_inscription_latine_traduite = db.Column(db.Text)
    # Les sources utilisées pour rédiger la fiche
    obelisque_bibliographie = db.Column(db.Text)
    # URL de l'image
    obelisque_image_url = db.Column(db.Text)
    # Crédits pour l'image
    obelisque_image_auteur = db.Column(db.Text)
    # Licence de l'image
    obelisque_image_licence = db.Column(db.Text)
    # Lien vers la licence
    obelisque_image_licence_url = db.Column(db.Text)
    erige = db.relationship("Erige", back_populates="obelisque")
    authorships = db.relationship("Authorship", back_populates="obelisque")

    # Pour ajouter un obélisque :
    @staticmethod
    def obelisque_add(obelisque_add_nom, obelisque_add_hauteur, obelisque_add_hauteur_avec_base, obelisque_add_materiau,
                      obelisque_add_type_commande, obelisque_add_notice, obelisque_add_inscription_latine,
                      obelisque_add_inscription_latine_traduite, obelisque_add_bibliographie, obelisque_add_image_url,
                      obelisque_add_image_auteur, obelisque_add_image_licence, obelisque_add_image_licence_url):

        """ Fonction permettant d'ajouter un obélisque à la base de données.
            :param obelisque_add_*: données recueillies depuis le formulaire
            :type obelisque_add_*: Text ou Float (obelisque_add_hauteur, obelisque_add_hauteur_avec_base)
            :returns: ajout de l'entrée dans la table obelisque de la base de données """

        erreurs = []
        # On définit des attributs obligatoires et les erreurs affichées si ceux-ci sont laissés vides
        if not obelisque_add_nom:
            erreurs.append("veuillez renseigner le nom de l'obélisque")
        if not obelisque_add_hauteur:
            erreurs.append("veuillez renseigner la hauteur de l'obélisque")
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
        if not obelisque_add_image_url:
            erreurs.append("veuillez renseigner l'URL de l'image")
        if not obelisque_add_image_auteur:
            erreurs.append("veuillez renseigner l'ayant-droit de l'image")
        if not obelisque_add_image_licence:
            erreurs.append("veuillez renseigner la licence permettant la réutilisation de l'image")
        if not obelisque_add_image_licence_url:
            erreurs.append("veuillez renseigner l'URL de la licence")

        # En cas d'erreur on affiche le message d'erreur associé
        if len(erreurs) > 0:
            return False, erreurs

        # En l'absence d'erreurs, on récupère les données du futur nouvel enregistrement à partir du formulaire
        ajoutable = Obelisque(obelisque_nom=obelisque_add_nom,
                              obelisque_hauteur=obelisque_add_hauteur,
                              obelisque_hauteur_avec_base=obelisque_add_hauteur_avec_base,
                              obelisque_materiau=obelisque_add_materiau,
                              obelisque_type_commande=obelisque_add_type_commande,
                              obelisque_notice=obelisque_add_notice,
                              obelisque_inscription_latine=obelisque_add_inscription_latine,
                              obelisque_inscription_latine_traduite=obelisque_add_inscription_latine_traduite,
                              obelisque_bibliographie=obelisque_add_bibliographie,
                              obelisque_image_url=obelisque_add_image_url,
                              obelisque_image_auteur=obelisque_add_image_auteur,
                              obelisque_image_licence=obelisque_add_image_licence,
                              obelisque_image_licence_url=obelisque_add_image_licence_url,
                              )

        # Si l'ajout fonctionne, on l'intègre à la base de données
        try:
            db.session.add(ajoutable)
            db.session.commit()
            return True, ajoutable

        # Sinon, on retourne une erreur
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def obelisque_delete(obelisque_id):

        """ Fonction permettant de supprimer un obélisque de la base de données.
            :param obelisque_id: id de l'obélisque à supprimer
            :type obelisque_id: integer
            :returns: suppression de l'obélisque sélectionné de la table obelisque de la base de données """

        supprimable = Obelisque.query.get(obelisque_id)

        # Si l'opération fonctionne, on supprime l'enregistrement de la base de données
        try:
            db.session.delete(supprimable)
            db.session.commit()
            return True

        # Sinon, on retourne une erreur
        except Exception as erreur:
            return False, [str(erreur)]


# On crée une classe Personne pour recenser ceux ayant fait ériger un obélisque
class Personne(db.Model):
    personne_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # Le nom du commanditaire
    personne_nom = db.Column(db.Text)
    # Ses fonctions
    personne_fonction = db.Column(db.Text)
    # Sa nationalité
    personne_nationalite = db.Column(db.Text)
    erige = db.relationship("Erige", back_populates="personne")
    authorships = db.relationship("Authorship", back_populates="personne")

    @staticmethod
    def personne_add(personne_add_nom, personne_add_fonction, personne_add_nationalite):

        """ Fonction permettant d'ajouter un commanditaire à la base de données.
            :param personne_add_*: données recueillies depuis le formulaire
            :type personne_add_*: Text
            :returns: ajout de l'entrée dans la table personne de la base de données """

        erreurs = []
        # On définit des attributs obligatoires et les erreurs affichées si ceux-ci sont laissés vides
        if not personne_add_nom:
            erreurs.append("veuillez renseigner le nom du commanditaire")
        if not personne_add_fonction:
            erreurs.append(
                "veuillez renseigner les fonctions du commanditaire")
        if not personne_add_nationalite:
            erreurs.append(
                "veuillez renseigner la nationalité du commanditaire")

        # En cas d'erreur on affiche le message d'erreur associé
        if len(erreurs) > 0:
            return False, erreurs

        # En l'absence d'erreurs, on récupère les données du futur nouvel enregistrement à partir du formulaire
        ajoutable = Personne(personne_nom=personne_add_nom,
                             personne_fonction=personne_add_fonction,
                             personne_nationalite=personne_add_nationalite)

        # Si l'ajout fonctionne, on l'intègre à la base de données
        try:
            db.session.add(ajoutable)
            db.session.commit()
            return True, ajoutable

        # Sinon, on retourne une erreur
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def personne_delete(personne_id):

        """ Fonction permettant de supprimer un commanditaire de la base de données.
            :param personne_id: id du commanditaire à supprimer
            :type personne_id: integer
            :returns: suppression du commanditaire sélectionné de la table personne de la base de données """

        supprimable = Personne.query.get(personne_id)

        # Si l'opération fonctionne, on supprime l'enregistrement de la base de données
        try:
            db.session.delete(supprimable)
            db.session.commit()
            return True

        # Sinon, on retourne une erreur
        except Exception as erreur:
            return False, [str(erreur)]


# On crée une classe Localisation pour recenser les lieux où les obélisques ont été érigés
class Localisation(db.Model):
    localisation_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # Le lieu exact de l'élévation
    localisation_lieu = db.Column(db.Text)
    # Le terme de "ville" est à concevoir au sens large, il s'agit d'indiquer ici une référence plus précise que le pays, mais moins précise que le lieu exact.
    # On y renseigne la ville si le lieu d'évélation en possède une, mais on y retrouve également des termes tels que "Voie Appienne" (donc une route)
    # ou "Karnak" (un complexe)
    localisation_ville = db.Column(db.Text)
    # Le pays du lieu de l'élévation
    localisation_pays = db.Column(db.Text)
    # La longitude
    localisation_longitude = db.Column(db.Float)
    # La latitude
    localisation_latitude = db.Column(db.Float)
    erige = db.relationship("Erige", back_populates="localisation")
    authorships = db.relationship("Authorship", back_populates="localisation")

    @staticmethod
    def localisation_add(localisation_add_lieu, localisation_add_ville, localisation_add_pays,
                         localisation_add_latitude, localisation_add_longitude):

        """ Fonction permettant d'ajouter un lieu à la base de données.
            :param localisation_add_*: données recueillies depuis le formulaire
            :type localisation_add_*: Text ou Float (localisation_add_latitude et localisation_add_longitude)
            :returns: ajout de l'entrée dans la table localisation de la base de données """

        erreurs = []
        # On définit des attributs obligatoires et les erreurs affichées si ceux-ci sont laissés vides
        if not localisation_add_lieu:
            erreurs.append("veuillez renseigner le nom du lieu")
        if not localisation_add_ville:
            erreurs.append(
                "veuillez renseigner le nom de la ville")
        if not localisation_add_pays:
            erreurs.append(
                "veuillez renseigner le nom du pays")
        if not localisation_add_latitude:
            erreurs.append(
                "veuillez renseigner une latitude")
        if not localisation_add_longitude:
            erreurs.append(
                "veuillez renseigner une longitude")

        # En cas d'erreur on affiche le message d'erreur associé
        if len(erreurs) > 0:
            return False, erreurs

        # En l'absence d'erreurs, on récupère les données du futur nouvel enregistrement à partir du formulaire
        ajoutable = Localisation(localisation_lieu=localisation_add_lieu,
                                 localisation_ville=localisation_add_ville,
                                 localisation_pays=localisation_add_pays,
                                 localisation_latitude=localisation_add_latitude,
                                 localisation_longitude=localisation_add_longitude)

        # Si l'ajout fonctionne, on l'intègre à la base de données
        try:
            db.session.add(ajoutable)
            db.session.commit()
            return True, ajoutable

        # Sinon, on retourne une erreur
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def localisation_delete(localisation_id):

        """ Fonction permettant de supprimer un lieu de la base de données.
            :param localisation_id: id du lieu à supprimer
            :type localisation_id: integer
            :returns: suppression du lieu sélectionné de la table localisation de la base de données """

        supprimable = Localisation.query.get(localisation_id)

        # Si l'opération fonctionne, on supprime l'enregistrement de la base de données
        try:
            db.session.delete(supprimable)
            db.session.commit()
            return True

        # Sinon, on retourne une erreur
        except Exception as erreur:
            return False, [str(erreur)]


# On crée une classe Erige servant de table de relation reliant les trois tables précédentes
# Cette table recense les élévations d'obélisques
class Erige(db.Model):
    __tablename__ = "erige"
    erige_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # On récupère l'id de l'obélisque élevé
    erige_id_obelisque = db.Column(db.Integer, db.ForeignKey('obelisque.obelisque_id'))
    # On récupère l'id du commanditaire ayant ordonné l'élévation
    erige_id_personne = db.Column(db.Integer, db.ForeignKey('personne.personne_id'))
    # On récupère l'id du lieu où a été élevé l'obélisque
    erige_id_localisation = db.Column(db.Integer, db.ForeignKey('localisation.localisation_id'))
    # On renseigne la date de l'élévation (au format Text, permettant aisément l'emploi de valeurs telles que "1279-1213 av. J.-C.")
    erige_date = db.Column(db.Text)
    # On indique si l'enregistrement correspond à la localisation actuelle de l'obélisque (0 = non, 1 = oui)
    erige_actuel = db.Column(db.Integer)
    obelisque = db.relationship("Obelisque", back_populates="erige")
    personne = db.relationship("Personne", back_populates="erige")
    localisation = db.relationship("Localisation", back_populates="erige")
    authorships = db.relationship("Authorship", back_populates="erige")

    @staticmethod
    def erige_add(erige_add_id_obelisque, erige_add_id_personne, erige_add_id_localisation, erige_add_date,
                  erige_add_actuel):

        """ Fonction permettant d'ajouter une élévation à la base de données.
            :param erige_add_*: données recueillies depuis le formulaire
            :type erige_add_*: Text (erige_add_date) ou Integer
            :returns: ajout de l'entrée dans la table erige de la base de données """

        erreurs = []
        # On définit des attributs obligatoires et les erreurs affichées si ceux-ci sont laissés vides
        if not erige_add_id_obelisque:
            erreurs.append("veuillez renseigner l'identifiant de l'obélisque'")
        if not erige_add_id_personne:
            erreurs.append(
                "veuillez renseigner l'identifiant du commanditaire'")
        if not erige_add_id_localisation:
            erreurs.append(
                "veuillez renseigner l'identifiant du lieu'")
        if not erige_add_date:
            erreurs.append(
                "veuillez renseigner la date d'élévation")

        # En cas d'erreur on affiche le message d'erreur associé
        if len(erreurs) > 0:
            return False, erreurs

        # En l'absence d'erreurs, on récupère les données du futur nouvel enregistrement à partir du formulaire
        ajoutable = Erige(erige_id_obelisque=erige_add_id_obelisque,
                          erige_id_personne=erige_add_id_personne,
                          erige_id_localisation=erige_add_id_localisation,
                          erige_date=erige_add_date,
                          erige_actuel=erige_add_actuel)

        # Si l'ajout fonctionne, on l'intègre à la base de données
        try:
            db.session.add(ajoutable)
            db.session.commit()
            return True, ajoutable

        # Sinon, on retourne une erreur
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def erige_delete(erige_id):

        """ Fonction permettant de supprimer une élévation de la base de données.
            :param erige_id: id de l'élévation à supprimer
            :type erige_id: integer
            :returns: suppression de l'élévation sélectionnée de la table erige de la base de données """

        supprimable = Erige.query.get(erige_id)

        # Si l'opération fonctionne, on supprime l'enregistrement de la base de données
        try:
            db.session.delete(supprimable)
            db.session.commit()
            return True

        # Sinon, on retourne une erreur
        except Exception as erreur:
            return False, [str(erreur)]


# On crée une classe Authorship pour recenser les modifications des utilisateurs
class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    authorship_obelisque_id = db.Column(db.Integer, db.ForeignKey('obelisque.obelisque_id'), nullable=True)
    authorship_personne_id = db.Column(db.Integer, db.ForeignKey('personne.personne_id'), nullable=True)
    authorship_localisation_id = db.Column(db.Integer, db.ForeignKey('localisation.localisation_id'), nullable=True)
    authorship_erige_id = db.Column(db.Integer, db.ForeignKey('erige.erige_id'), nullable=True)
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # Pour renseigner l'heure, on utilise les paramètres locaux
    # Source : https://www.codegrepper.com/code-examples/python/python+datetime+local+timezone
    now = datetime.datetime.now()
    local_now = now.astimezone()
    authorship_date = db.Column(db.DateTime, default=local_now, nullable=False)
    obelisque = db.relationship("Obelisque", back_populates="authorships")
    personne = db.relationship("Personne", back_populates="authorships")
    localisation = db.relationship("Localisation", back_populates="authorships")
    erige = db.relationship("Erige", back_populates="authorships")
    user = db.relationship("User", back_populates="authorships")
