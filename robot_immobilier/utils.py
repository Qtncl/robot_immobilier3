# utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL, EMAIL_PASSWORD, DEST_EMAIL

def envoyer_email(biens):
    try:
        subject = "Nouvelles bonnes affaires immobilières"
        body = "\n\n".join([f"{bien['title']} - {bien['prix']} € - {bien['surface']} m² - {bien['chambres']} chambres\nLien: {bien['lien']}" for bien in biens])

        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = DEST_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL, DEST_EMAIL, msg.as_string())
        server.quit()

        print("Email envoyé avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

def filtrer_bons_plans(biens, prix_m2_ville):
    bons_plans = []
    for bien in biens:
        prix_m2_bien = bien['prix'] / bien['surface']
        if prix_m2_bien < prix_m2_ville * 0.8:  # Si le prix/m² est inférieur à 80% du prix moyen
            bons_plans.append(bien)
    return bons_plans
