from flask import render_template, request, flash, redirect


from ..app import app, login, db
from ..modeles.donnees import Obelisque, Personne, Erige, Image
from ..modeles.utilisateurs import Utilisateur
from ..constantes import LIEUX_PAR_PAGE
from flask_login import login_user, current_user, logout_user


@app.route("/")
def accueil():
    return render_template("pages/accueil.html")


@app.route("/obelisque/<int:obelisque_id>")
def obelisque(obelisque_id):
    obelisque_unique = Obelisque.query.filter(Obelisque.obelisque_id == obelisque_id).first()
    image_unique = Image.query.filter(Image.image_obelisque_id == obelisque_id).first()
    erige_multiple = Erige.query.filter(Erige.erige_id_obelisque == obelisque_id)
    personne_multiple = Personne.query.filter(Erige.erige_id_personne == Personne.personne_id)
    return render_template("pages/obelisque.html", obelisque=obelisque_unique, image=image_unique, erige=erige_multiple, personne=personne_multiple)


@app.route("/personne/<int:personne_id>")
def personne(personne_id):
    personne_unique = Personne.query.filter(Personne.personne_id == personne_id).first()
    erige_multiple = Erige.query.filter(Erige.erige_id_obelisque == personne_id)
    return render_template("pages/personne.html", personne=personne_unique, erige=erige_multiple)


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
    resultats = []

    # On fait de même pour le titre de la page
    titre = "Recherche"
    if motclef:
        resultats = Obelisque.query.filter(
            Obelisque.obelisque_nom.like("%{}%".format(motclef))
        ).paginate(page=page, per_page=LIEUX_PAR_PAGE)
        titre = "Résultat pour la recherche `" + motclef + "`"

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef
    )


@app.route("/browse")
def browse():
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = Obelisque.query.paginate(page=page, per_page=LIEUX_PAR_PAGE)

    return render_template(
        "pages/browse.html",
        resultats=resultats
    )


@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = Utilisateur.creer(
            utilisateur_login=request.form.get("login", None),
            utilisateur_mail=request.form.get("email", None),
            utilisateur_password=request.form.get("motdepasse", None)
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
        utilisateur = Utilisateur.identification(
            utilisateur_login=request.form.get("login", None),
            utilisateur_motdepasse=request.form.get("motdepasse", None)
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
