from flask import render_template, request, flash, redirect, url_for

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

#Page redirigeant vers les ajouts de pages
@app.route("/add")
def add():
    return render_template("pages/add.html")


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

#L'index recensant l'intégralité des obélisques
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


#Ajouter, modifier ou supprimer une page

#Ajouter une page

#Ajouter une page obélisque

@app.route("/obelisque/add", methods=["GET", "POST"])
@login_required
def obelisque_add():

    if request.method == "POST":
        statut, informations = Obelisque.obelisque_add(
            obelisque_add_nom = request.form.get("obelisque_add_nom", None),
            obelisque_add_hauteur = request.form.get("obelisque_add_hauteur", None),
            obelisque_add_hauteur_avec_base = request.form.get("obelisque_add_hauteur_avec_base", None),
            obelisque_add_materiau=request.form.get("obelisque_add_materiau", None),
            obelisque_add_type_commande=request.form.get("obelisque_add_type_commande", None),
            obelisque_add_notice=request.form.get("obelisque_add_notice", None),
            obelisque_add_inscription_latine=request.form.get("obelisque_add_inscription_latine", None),
            obelisque_add_inscription_latine_traduite=request.form.get("obelisque_add_inscription_latine_traduite", None),
            obelisque_add_bibliographie=request.form.get("obelisque_add_bibliographie", None),
            obelisque_add_image_url=request.form.get("obelisque_add_image_url", None),
            obelisque_add_image_auteur=request.form.get("obelisque_add_image_auteur", None),
            obelisque_add_image_licence=request.form.get("obelisque_add_image_licence", None),
            obelisque_add_image_licence_url=request.form.get("obelisque_add_image_licence_url", None)
        )

        if statut is True:
            flash("Nouvel obélisque ajouté à la base", "success")
            return redirect("/")
        else:
            flash("Echec : " + ", ".join(informations), "danger")
            return render_template("pages/obelisque_form_add.html")
    else:
        return render_template("pages/obelisque_form_add.html")


#Ajouter une page personne

@app.route("/personne/add", methods=["GET", "POST"])
@login_required
def personne_add():

    if request.method == "POST":
        statut, informations = Personne.personne_add(
        personne_add_nom = request.form.get("personne_add_nom", None),
        personne_add_fonction = request.form.get("personne_add_fonction", None),
        personne_add_nationalite = request.form.get("personne_add_nationalite", None)
        )

        if statut is True:
            flash("Nouveau commanditaire ajouté à la base", "success")
            return redirect("/")
        else:
            flash("Echec : " + ", ".join(informations), "danger")
            return render_template("pages/personne_form_add.html")
    else:
        return render_template("pages/personne_form_add.html")

#Ajouter une page lieu

@app.route("/lieu/add", methods=["GET", "POST"])
@login_required
def localisation_add():

    if request.method == "POST":
        statut, informations = Localisation.localisation_add(
        localisation_add_lieu = request.form.get("localisation_add_lieu", None),
        localisation_add_ville = request.form.get("localisation_add_ville", None),
        localisation_add_pays = request.form.get("localisation_add_pays", None),
        localisation_add_latitude=request.form.get("localisation_add_latitude", None),
        localisation_add_longitude=request.form.get("localisation_add_longitude", None)
        )

        if statut is True:
            flash("Nouveau lieu ajouté à la base", "success")
            return redirect("/")
        else:
            flash("Echec : " + ", ".join(informations), "danger")
            return render_template("pages/lieu_form_add.html")
    else:
        return render_template("pages/lieu_form_add.html")


#Modifier une page

#Modifier une page obélisque

@app.route("/obelisque/<int:obelisque_id>/update", methods=["GET", "POST"])
@login_required
def obelisque_update(obelisque_id):
    editable = Obelisque.query.get_or_404(obelisque_id)
    '''erige_editable = Erige.query.filter(Erige.erige_id_obelisque == obelisque_id)'''

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
            editable.obelisque_nom = request.form["obelisque_nom"]
            editable.obelisque_hauteur = request.form["obelisque_hauteur"]
            editable.obelisque_hauteur_avec_base = request.form["obelisque_hauteur_avec_base"]
            editable.obelisque_materiau = request.form["obelisque_materiau"]
            editable.obelisque_type_commande = request.form["obelisque_type_commande"]
            editable.obelisque_notice = request.form["obelisque_notice"]
            editable.obelisque_bibliographie = request.form["obelisque_bibliographie"]
            editable.obelisque_inscription_latine = request.form["obelisque_inscription_latine"]
            editable.obelisque_inscription_latine_traduite = request.form["obelisque_inscription_latine_traduite"]
            editable.obelisque_image_url = request.form["obelisque_image_url"]
            editable.obelisque_image_auteur = request.form["obelisque_image_auteur"]
            editable.obelisque_image_licence = request.form["obelisque_image_licence"]
            editable.obelisque_image_licence_url = request.form["obelisque_image_licence_url"]

            '''erige_editable.erige_id_obelisque = request.form["erige_id_obelisque"]
            erige_editable.erige_id_personne = request.form["erige_id_personne"]
            erige_editable.erige_id_localisation = request.form["erige_id_localisation"]
            erige_editable.erige_date = request.form["erige_date"]
            erige_editable.erige_actuel = request.form["erige_actuel"]'''

            db.session.add(editable)
            db.session.add(Authorship(obelisque=editable, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/obelisque_form_update.html",
        obelisque=editable,
        erreurs=erreurs,
        updated=updated
    )

#Modifier une page personne

@app.route("/personne/<int:personne_id>/update", methods=["GET", "POST"])
@login_required
def personne_update(personne_id):
    editable = Personne.query.get_or_404(personne_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        if not request.form.get("personne_nom", "").strip():
            erreurs.append("Insérez un nom")
        if not request.form.get("personne_nationalite", "").strip():
            erreurs.append("Insérez la nationalité de la personne")

        if not erreurs:
            print("Faire ma modification")
            editable.personne_nom = request.form["personne_nom"]
            editable.personne_nationalite = request.form["personne_nationalite"]
            editable.personne_fonction = request.form["personne_fonction"]

            db.session.add(editable)
            db.session.add(Authorship(personne=editable, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/personne_form_update.html",
        personne=editable,
        erreurs=erreurs,
        updated=updated
    )


#Modifier une page lieu

@app.route("/lieu/<int:localisation_id>/update", methods=["GET", "POST"])
@login_required
def localisation_update(localisation_id):
    editable = Localisation.query.get_or_404(localisation_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        if not request.form.get("localisation_lieu", "").strip():
            erreurs.append("Insérez un nom de lieu")
        if not request.form.get("localisation_ville", "").strip():
            erreurs.append("Insérez la ville du lieu")
        if not request.form.get("localisation_pays", "").strip():
            erreurs.append("Insérez le pays du lieu")

        if not erreurs:
            print("Faire ma modification")
            editable.localisation_lieu = request.form["localisation_lieu"]
            editable.localisation_ville = request.form["localisation_ville"]
            editable.localisation_pays = request.form["localisation_pays"]
            editable.localisation_latitude = request.form["localisation_latitude"]
            editable.localisation_longitude = request.form["localisation_longitude"]

            db.session.add(editable)
            db.session.add(Authorship(localisation=editable, user=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/lieu_form_update.html",
        localisation=editable,
        erreurs=erreurs,
        updated=updated
    )


#Supprimer une page

#Supprimer une page obélisque

@app.route("/obelisque/<int:obelisque_id>/delete", methods=["POST", "GET"])
@login_required
def obelisque_delete(obelisque_id):

    supprimable = Obelisque.query.get(obelisque_id)

    if request.method == "POST":
        statut = Obelisque.obelisque_delete(
            obelisque_id=obelisque_id
        )

        if statut is True:
            flash("L'obélisque a été supprimé de la base", "success")
            return redirect("/")
        else:
            flash("Echec", "error")
            return redirect("/")
    else:
        return render_template("pages/obelisque_form_delete.html", supprimable=supprimable)


#Supprimer une page personne

@app.route("/personne/<int:personne_id>/delete", methods=["POST", "GET"])
@login_required
def personne_delete(personne_id):

    supprimable = Personne.query.get(personne_id)

    if request.method == "POST":
        statut = Personne.personne_delete(
            personne_id=personne_id
        )

        if statut is True:
            flash("Le commanditaire a été supprimé de la base", "success")
            return redirect("/")
        else:
            flash("Echec", "error")
            return redirect("/")
    else:
        return render_template("pages/personne_form_delete.html", supprimable=supprimable)


#Supprimer une page lieu

@app.route("/lieu/<int:localisation_id>/delete", methods=["POST", "GET"])
@login_required
def localisation_delete(localisation_id):

    supprimable = Localisation.query.get(localisation_id)

    if request.method == "POST":
        statut = Localisation.localisation_delete(
            localisation_id=localisation_id
        )

        if statut is True:
            flash("Le lieu a été supprimé de la base", "success")
            return redirect("/")
        else:
            flash("Echec", "error")
            return redirect("/")
    else:
        return render_template("pages/lieu_form_delete.html", supprimable=supprimable)


#La page pour la gestion des élévations
#Source : https://www.youtube.com/watch?v=XTpLbBJTOM4
@app.route('/elevations')
@login_required
def elevations():
    erige = Erige.query.all()

    return render_template("pages/elevations.html", erige=erige)


#Ajouter une page Erige

@app.route("/erige/add", methods=["GET", "POST"])
@login_required
def erige_add():

    if request.method == "POST":
        statut, informations = Erige.erige_add(
        erige_add_id_obelisque = request.form.get("erige_add_id_obelisque", None),
        erige_add_id_personne = request.form.get("erige_add_id_personne", None),
        erige_add_id_localisation = request.form.get("erige_add_id_localisation", None),
        erige_add_date=request.form.get("erige_add_date", None),
        erige_add_actuel = request.form.get("erige_add_actuel", None)
        )

        if statut is True:
            flash("Nouvelle élévation ajoutée à la base", "success")
            return redirect(url_for('elevations'))
        else:
            flash("Echec : " + ", ".join(informations), "danger")
            return redirect(url_for('elevations'))
    else:
        return redirect(url_for('elevations'))

#Modifier une élévation

@app.route("/erige/<int:erige_id>/update", methods=["GET", "POST"])
@login_required
def erige_update(erige_id):
    editable = Erige.query.get_or_404(erige_id)

    erreurs = []

    if request.method == "POST":
        if not request.form.get("erige_id_obelisque", "").strip():
            erreurs.append("Insérez un id d'obélisque")
        if not request.form.get("erige_id_personne", "").strip():
            erreurs.append("Insérez un id de personne")
        if not request.form.get("erige_id_localisation", "").strip():
            erreurs.append("Insérez un id de lieu")
        if not request.form.get("erige_date", "").strip():
            erreurs.append("Insérez une date d'élévation")

        if not erreurs:
            print("Faire ma modification")
            editable.erige_id_obelisque = request.form["erige_id_obelisque"]
            editable.erige_id_personne = request.form["erige_id_personne"]
            editable.erige_id_localisation = request.form["erige_id_localisation"]
            editable.erige_date = request.form["erige_date"]
            editable.erige_actuel = request.form["erige_actuel"]

            db.session.add(editable)
            db.session.add(Authorship(erige=editable, user=current_user))
            db.session.commit()
            flash("Elévation mise à jour avec succès", "success")
        else :
            flash("Echec", "danger")

    return redirect(url_for('elevations'))


#Supprimer une élévation

@app.route("/erige/<int:erige_id>/delete", methods=["POST", "GET"])
@login_required
def erige_delete(erige_id):

    supprimable = Erige.query.get(erige_id)
    db.session.delete(supprimable)
    db.session.commit()
    flash("Elévation supprimée avec succès", "success")

    return redirect(url_for('elevations'))