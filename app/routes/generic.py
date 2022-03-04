from flask import render_template, request, flash, redirect


from ..app import app, login, db
from ..modeles.donnees import Obelisque, Personne, Erige, Image
from ..modeles.utilisateurs import User
from ..constantes import RESULTATS_PAR_PAGE
from flask_login import login_user, current_user, logout_user
# On importe or_ pour pouvoir filtrer des résultats sur de multiples éléments
from sqlalchemy import or_


@app.route("/")
def accueil():
    erige = Erige.query.all()
    obelisque = Obelisque.query.all()
    return render_template("pages/accueil.html", erige=erige, obelisque=obelisque)


@app.route("/obelisque/<int:obelisque_id>")
def obelisque(obelisque_id):
    obelisque_unique = Obelisque.query.filter(Obelisque.obelisque_id == obelisque_id).first_or_404()
    image_unique = Image.query.filter(Image.image_obelisque_id == obelisque_id).first()
    erige_multiple = Erige.query.filter(Erige.erige_id_obelisque == obelisque_id)
    personne_multiple = Personne.query.filter(Erige.erige_id_personne == Personne.personne_id)
    return render_template("pages/obelisque.html", obelisque=obelisque_unique, image=image_unique, erige=erige_multiple, personne=personne_multiple)

@app.route("/personne/<int:personne_id>")
def personne(personne_id):
    personne_unique = Personne.query.filter(Personne.personne_id == personne_id).first_or_404()
    erige_multiple = Erige.query.filter(Erige.erige_id_personne == personne_id)
    obelisque = Erige.query.filter(Erige.erige_id_obelisque == Obelisque.obelisque_id)

    return render_template("pages/personne.html", personne=personne_unique, erige=erige_multiple, obelisque=obelisque)

@app.route("/lieu/<int:erige_id>")
def erige(erige_id):
    erige = Erige.query.filter(Erige.erige_id == erige_id).first_or_404()
    return render_template("pages/lieu.html", erige=erige)


@app.route("/index_obelisques")
def index_obelisques():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Image.query.order_by(Image.image_titre_obelisque).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_obelisques.html", resultats=resultats)

@app.route("/index_personnes")
def index_personnes():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Personne.query.order_by(Personne.personne_nom).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_personnes.html", resultats=resultats)


@app.route("/index_lieux")
def index_lieux():
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = Erige.query.group_by(Erige.erige_lieu).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_lieux.html", resultats=resultats)


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
                Obelisque.obelisque_inscription_latine_traduite.like("%{}%".format(motclef))


            )).paginate(page=page, per_page=RESULTATS_PAR_PAGE)

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef
    )


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


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")



# Erreurs.
@app.errorhandler(404)
def not_found_error(error):
    return render_template('erreurs/erreur_404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error/erreur_500.html'), 500