from sqlalchemy import Enum

class UserType(str, Enum):
    client = "client"
    magasin = "magasin"
    admin = "admin"

class MagasinType(str, Enum):
    proximite = "proximite"
    restaurant = "restaurant"
    fastfood = "fastfood"
    bar = "bar"
    coiffeur = "coiffeur"
    boulangerie = "boulangerie"
    boucherie = "boucherie"
    epicerie = "epicerie"
    supermarche = "supermarche"
    primeur = "primeur"
    fleuriste = "fleuriste"
    librairie = "librairie"
