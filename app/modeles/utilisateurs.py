from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .. app import db, login

#On crée une classe Utilisateur
class Utilisateur(UserMixin, db.Model):
    utilisateur_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    utilisateur_login = db.Column(db.String(45), nullable=False, unique=True)
    utilisateur_mail = db.Column(db.Text, nullable=False)
    utilisateur_password = db.Column(db.String(100), nullable=False)


    @staticmethod
    def identification(login, motdepasse):
        """ Identifie un utilisateur. Si cela fonctionne, renvoie les données de l'utilisateurs.

        :param login: Login de l'utilisateur
        :param motdepasse: Mot de passe envoyé par l'utilisateur
        :returns: Si réussite, données de l'utilisateur. Sinon None
        :rtype: User or None
        """
        utilisateur = Utilisateur.query.filter(Utilisateur.utilisateur_login == login).first()
        if utilisateur and check_password_hash(Utilisateur.utilisateur_password, motdepasse):
            return utilisateur
        return None

    @staticmethod
    def creer(login, email, nom, motdepasse):
        """ Crée un compte utilisateur-rice. Retourne un tuple (booléen, User ou liste).
        Si il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur
        Sinon, elle renvoie True suivi de la donnée enregistrée

        :param login: Login de l'utilisateur-rice
        :param email: Email de l'utilisateur-rice
        :param nom: Nom de l'utilisateur-rice
        :param motdepasse: Mot de passe de l'utilisateur-rice (Minimum 6 caractères)

        """
        erreurs = []
        if not login:
            erreurs.append("Le login fourni est vide")
        if not email:
            erreurs.append("L'email fourni est vide")
        if not motdepasse or len(motdepasse) < 6:
            erreurs.append("Le mot de passe fourni est vide ou trop court")

        # On vérifie que personne n'a utilisé cet email ou ce login
        uniques = Utilisateur.query.filter(
            db.or_(Utilisateur.utilisateur_mail == email, Utilisateur.utilisateur_login == login)
        ).count()
        if uniques > 0:
            erreurs.append("L'email ou le login sont déjà inscrits dans notre base de données")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs

        # On crée un utilisateur
        utilisateur = Utilisateur(
            utilisateur_login=login,
            utilisateur_mail=email,
            utilisateur_password=generate_password_hash(motdepasse)
        )

        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(utilisateur)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        """ Retourne l'id de l'objet actuellement utilisé

        :returns: ID de l'utilisateur
        :rtype: int
        """
        return self.utilisateur_id

    def to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "people",
            "attributes": {
                "name": self.utilisateur_login
            }
        }

@login.user_loader
def trouver_utilisateur_via_id(identifiant):
    return Utilisateur.query.get(int(identifiant))
