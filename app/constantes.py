from warnings import warn

RESULTATS_PAR_PAGE = 10

SECRET_KEY = "Carthago Delenda Est"
API_ROUTE = "/api"

if SECRET_KEY == "Carthago Delenda Est":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
