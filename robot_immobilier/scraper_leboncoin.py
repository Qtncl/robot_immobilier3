# scraper_leboncoin.py
import requests
from bs4 import BeautifulSoup

def chercher_biens_leboncoin(ville, prix_max, surface_min, chambres_min, rayon):
    print("Scraping Leboncoin...")
    url = f"https://www.leboncoin.fr/recherche?category=9&locations={ville}_68000__{rayon}&real_estate_type=1&price_max={prix_max}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    biens = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        annonces = soup.find_all("a", class_="styles_adCard__2YFTi")

        for annonce in annonces:
            try:
                title = annonce.find("p", class_="styles_title__2Yz3_").text
                prix = int(annonce.find("span", class_="styles_price__2x_kN").text.replace("€", "").replace("\u202f", "").replace(" ", ""))
                details = annonce.find("div", class_="styles_adCardFooter__2MZ0g").text

                surface = None
                chambres = None
                if "m²" in details:
                    surface = int(details.split("m²")[0].strip())
                if "chambre" in details:
                    chambres = int(details.split("chambre")[0][-1])

                lien = "https://www.leboncoin.fr" + annonce.get("href")

                if surface and chambres and surface >= surface_min and chambres >= chambres_min:
                    biens.append({
                        "title": title,
                        "prix": prix,
                        "surface": surface,
                        "chambres": chambres,
                        "lien": lien
                    })
            except Exception as e:
                print(f"Erreur parsing annonce Leboncoin: {e}")
    else:
        print(f"Erreur lors du chargement de Leboncoin: {response.status_code}")

    return biens
