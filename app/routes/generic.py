from flask import render_template, request, flash, redirect


from ..app import app, login, db
from ..modeles.donnees import Obelisque, Personne, Erige, Localisation, Authorship
from ..modeles.utilisateurs import User
from ..constantes import RESULTATS_PAR_PAGE
from flask_login import login_user, current_user, logout_user, login_required
# On importe or_ pour pouvoir filtrer des résultats sur de multiples éléments
from sqlalchemy import or_

#Page d'accueil
@app.route("/")
def accueil():
    erige = Erige.query.all()
    return render_template("pages/accueil.html", erige=erige)


#Routes vers les trois éléments principaux de la base

#Les obélisques
@app.route("/obelisque/<int:obelisque_id>")
def obelisque(obelisque_id):
    obelisque = Obelisque.query.filter(Obelisque.obelisque_id == obelisque_id).first_or_404()
    erige = Erige.query.filter(Erige.erige_id_obelisque == obelisque_id)
    return render_template("pages/obelisque.html", obelisque=obelisque, erige=erige)

#Les personnes (commanditaires)
@app.route("/personne/<int:personne_id>")
def personne(personne_id):
    personne = Personne.query.filter(Personne.personne_id == personne_id).first_or_404()
    erige = Erige.query.filter(Erige.erige_id_personne == personne_id).order_by(Erige.erige_date)
    return render_template("pages/personne.html", personne=personne, erige=erige)

#Les localisations
@app.route("/lieu/<int:localisation_id>")
def localisation(localisation_id):
    localisation = Localisation.query.filter(Localisation.localisation_id == localisation_id).first_or_404()
    erige = Erige.query.filter(Erige.erige_id_localisation == localisation_id).order_by(Erige.erige_date)
    return render_template("pages/lieu.html", localisation=localisation, erige=erige)


#Les pages d'index

#L'index recençant l'intégralité des obélisques
@app.route("/index_obelisques")
def index_obelisques():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Obelisque.query.order_by(Obelisque.obelisque_nom).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_obelisques.html", resultats=resultats)

#L'index des obélisques égyptiens
@app.route("/index_obelisques_egyptiens")
def index_obelisques_egyptiens():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Obelisque.query.filter(Obelisque.obelisque_type_commande =="Égyptienne").paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_obelisques_egyptiens.html", resultats=resultats)

#L'index des obélisques romains
@app.route("/index_obelisques_romains")
def index_obelisques_romains():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Obelisque.query.filter(Obelisque.obelisque_type_commande =="Romaine").paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_obelisques_romains.html", resultats=resultats)

#L'index des personnes (commanditaires)
@app.route("/index_personnes")
def index_personnes():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Personne.query.order_by(Personne.personne_nom).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_personnes.html", resultats=resultats)

#L'index des lieux (localisations)
@app.route("/index_lieux")
def index_lieux():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Localisation.query.order_by(Localisation.localisation_lieu).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_lieux.html", resultats=resultats)


#Faire une recherche plein texte sur la table Obelisque
@app.route("/recherche")
def recherche():
    """ Route permettant la recherche plein-texte
    """
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats =  []

    # On fait de même pour le titre de la page
    titre = "Recherche"
    if motclef:
        resultats = Obelisque.query.filter(or_(
                Obelisque.obelisque_nom.like("%{}%".format(motclef)),
                Obelisque.obelisque_materiau.like("%{}%".format(motclef)),
                Obelisque.obelisque_type_commande.like("%{}%".format(motclef)),
                Obelisque.obelisque_notice.like("%{}%".format(motclef)),
                Obelisque.obelisque_inscription_latine.like("%{}%".format(motclef)),
                Obelisque.obelisque_inscription_latine_traduite.like("%{}%".format(motclef)))).paginate(page=page, per_page=RESULTATS_PAR_PAGE)

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef
    )


# Gestion des comptes utilisateurs

#Création d'un compte : l'inscription
@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")

#Connexion à un compte existant
@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'

#Déconnexion
@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")


# Gérer les pages d'erreurs

#Erreur 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('erreurs/erreur_404.html'), 404

#Erreur 500
@app.errorhandler(500)
def internal_error(error):
    return render_template('error/erreur_500.html'), 500


#Modifier, ajouter ou supprimer une page


#Modifier une page

#Modifier une page obélisque
@app.route("/obelisque/<int:obelisque_id>/update", methods=["GET", "POST"])
@login_required
def obelisque_update(obelisque_id):
    mon_obelisque = Obelisque.query.get_or_404(obelisque_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        if not request.form.get("obelisque_nom", "").strip():
            erreurs.append("Insérez un nom d'obélisque")
        if not request.form.get("obelisque_hauteur", "").strip():
            erreurs.append("Insérez une hauteur d'obélisque")
        if not request.form.get("obelisque_hauteur_avec_base", "").strip():
            erreurs.append("Insérez une hauteur avec base d'obélisque")
        if not request.form.get("obelisque_materiau", "").strip():
            erreurs.append("Insérez le matériau de l'obélisque")
        if not request.form.get("obelisque_type_commande", "").strip():
            erreurs.append("Insérez le type de commande de l'obélisque")
        if not request.form.get("obelisque_notice", "").strip():
            erreurs.append("Insérez une notice d'obélisque")
        if not request.form.get("obelisque_bibliographie", "").strip():
            erreurs.append("Insérez une bibliographie")
        if not request.form.get("obelisque_image_nom", "").strip():
            erreurs.append("Insérez le nom du fichier image")
        if not request.form.get("obelisque_image_url", "").strip():
            erreurs.append("Insérez l'URL de l'image'")
        if not request.form.get("obelisque_image_auteur", "").strip():
            erreurs.append("Insérez le nom de l'auteur de l'image")
        if not request.form.get("obelisque_image_licence", "").strip():
            erreurs.append("Insérez les droits de réutilisation de l'image")
        if not request.form.get("obelisque_image_licence_url", "").strip():
            erreurs.append("Insérez l'URL de la licence de l'image")

        if not erreurs:
            print("Faire ma modification")
            mon_obelisque.obelisque_nom = request.form["obelisque_nom"]
            mon_obelisque.obelisque_hauteur = request.form["obelisque_hauteur"]
            mon_obelisque.obelisque_hauteur_avec_base = request.form["obelisque_hauteur_avec_base"]
            mon_obelisque.obelisque_materiau = request.form["obelisque_materiau"]
            mon_obelisque.obelisque_type_commande = request.form["obelisque_type_commande"]
            mon_obelisque.obelisque_notice = request.form["obelisque_notice"]
            mon_obelisque.obelisque_bibliographie = request.form["obelisque_bibliographie"]
            mon_obelisque.obelisque_image_nom = request.form["obelisque_image_nom"]
            mon_obelisque.obelisque_image_url = request.form["obelisque_image_url"]
            mon_obelisque.obelisque_image_auteur = request.form["obelisque_image_auteur"]
            mon_obelisque.obelisque_image_licence = request.form["obelisque_image_licence"]
            mon_obelisque.obelisque_image_licence_url = request.form["obelisque_image_licence_url"]

            db.session.add(mon_obelisque)
            db.session.add(Authorship(obelisque=mon_obelisque, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/obelisque_form_update.html",
        obelisque=mon_obelisque,
        erreurs=erreurs,
        updated=updated
    )