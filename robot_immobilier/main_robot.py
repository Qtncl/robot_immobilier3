# main_robot.py
from scraper_leboncoin import chercher_biens_leboncoin
from scraper_seloger import chercher_biens_seloger
from prix_m2_scraper import get_prix_m2
from utils import envoyer_email, filtrer_bons_plans
from config import VILLE, PRIX_MAX, SURFACE_MIN, CHAMBRES_MIN, RAYON

def main():
    print("Début de la recherche immobilière...")

    prix_m2_ville = get_prix_m2(VILLE)
    print(f"Prix moyen au m2 pour {VILLE} : {prix_m2_ville} €")

    biens = []
    biens += chercher_biens_leboncoin(VILLE, PRIX_MAX, SURFACE_MIN, CHAMBRES_MIN, RAYON)
    biens += chercher_biens_seloger(VILLE, PRIX_MAX, SURFACE_MIN, CHAMBRES_MIN, RAYON)

    print(f"Nombre total de biens trouvés : {len(biens)}")

    bons_plans = filtrer_bons_plans(biens, prix_m2_ville)

    if bons_plans:
        print(f"{len(bons_plans)} bonnes affaires trouvées, envoi de l'email...")
        envoyer_email(bons_plans)
    else:
        print("Aucune bonne affaire détectée pour cette recherche.")

if __name__ == "__main__":
    main()
