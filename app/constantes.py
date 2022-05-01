from warnings import warn

# On définit le nombre de résultats affichés par page
RESULTATS_PAR_PAGE = 18

SECRET_KEY = "Carthago Delenda Est"

if SECRET_KEY == "Carthago Delenda Est":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
