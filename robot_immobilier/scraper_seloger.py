# scraper_seloger.py
import requests
from bs4 import BeautifulSoup

def chercher_biens_seloger(ville, prix_max, surface_min, chambres_min, rayon):
    print("Scraping SeLoger...")
    biens = []

    # Attention : SeLoger utilise une API interne donc ici c’est simplifié
    try:
        url = f"https://www.seloger.com/list.htm?types=1&places=[{{\"ci\":680066}}]&priceMax={prix_max}&surfaceMin={surface_min}&bedroomsMin={chambres_min}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            annonces = soup.find_all("div", class_="c-pa-list")

            for annonce in annonces:
                try:
                    title = annonce.find("h2", class_="c-pa-link").text.strip()
                    prix = annonce.find("div", class_="c-pa-price").text.strip()
                    prix = int(prix.replace("€", "").replace("\u202f", "").replace(" ", "").replace("\n", ""))

                    surface = annonce.find("div", class_="c-pa-criterion").text.strip()
                    surface = int(surface.split("m²")[0].strip())

                    chambres_text = annonce.find_all("div", class_="c-pa-criterion")[1].text.strip()
                    chambres = int(chambres_text.split(" ")[0])

                    lien = "https://www.seloger.com" + annonce.find("a", class_="c-pa-link").get("href")

                    if surface >= surface_min and chambres >= chambres_min:
                        biens.append({
                            "title": title,
                            "prix": prix,
                            "surface": surface,
                            "chambres": chambres,
                            "lien": lien
                        })
                except Exception as e:
                    print(f"Erreur parsing annonce SeLoger: {e}")
        else:
            print(f"Erreur chargement SeLoger: {response.status_code}")
    except Exception as e:
        print(f"Erreur connexion SeLoger: {e}")

    return biens
