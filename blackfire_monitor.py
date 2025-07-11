import requests
from bs4 import BeautifulSoup
import os

# Miljøvariabler til Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Blackfire URL
URL = "https://en.blackfire.cz/pokemon-company/pokemon-tcg?p=Products&cid=2024934&sort=newest&instock=0&p12=Pok%C3%A9mon+Company&p13=POK%C3%89MON"

# Funktion til at sende Telegram beskeder
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("Fejl ved afsendelse af besked:", response.text)

# Funktion til at finde produktnavne
def check_for_products():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find alle <a> links under produkter
    product_links = soup.select(".products-list a")
    
    product_names = []
    for link in product_links:
        text = link.get_text(strip=True)
        if text and "pokemon-tcg" in link.get("href", ""):
            product_names.append(text)

    if product_names:
        message = "🛒 Produkter fundet:\n\n" + "\n".join(f"• {name}" for name in product_names)
        send_telegram(message)
    else:
        send_telegram("⚠️ Ingen produkter fundet på siden.")

# Kør program
send_telegram("🛰️ Overvågning startet – tjekker produkter...")
check_for_products()
