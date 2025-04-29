# prix_m2_scraper.py
import requests
from bs4 import BeautifulSoup

def get_prix_m2(ville):
    print(f"Récupération du prix moyen au m² pour {ville}...")
    url = f"https://www.meilleursagents.com/prix-immobilier/{ville}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    prix_m2 = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            prix_m2 = soup.find("div", class_="price").text.strip().split()[0]
            prix_m2 = int(prix_m2.replace("€", "").replace("\u202f", "").replace(" ", ""))
        except Exception as e:
            print(f"Erreur parsing prix m2 : {e}")
    else:
        print(f"Erreur lors du chargement de MeilleursAgents: {response.status_code}")

    return prix_m2
