import requests
from bs4 import BeautifulSoup
import os

# Hent Telegram info fra miljøvariabler
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = "https://en.blackfire.cz/pokemon-company/pokemon-tcg?p=Products&cid=2024934&sort=newest&instock=0&p12=Pok%C3%A9mon+Company&p13=POK%C3%89MON"

# Funktion til at sende Telegram besked
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

# Send besked når programmet starter
send_telegram("🔍 Overvågning startet – jeg holder øje med Blackfire!")

# Hent siden og find produkter
def check_for_products():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select(".products-list .product")
    if products:
        product_names = [p.select_one(".product-name").get_text(strip=True) for p in products[:3]]
        message = "🆕 Nye produkter fundet:\n" + "\n".join(f"- {name}" for name in product_names)
        send_telegram(message)
    else:
        print("Ingen produkter fundet.")

# Kør overvågning
check_for_products()
