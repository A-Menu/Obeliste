from warnings import warn

LIEUX_PAR_PAGE = 2
SECRET_KEY = "Carthago Delenda Est"
API_ROUTE = "/api"

if SECRET_KEY == "Carthago Delenda Est":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
