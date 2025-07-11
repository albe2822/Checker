import requests
from bs4 import BeautifulSoup
import os

TELEGRAM_TOKEN = "8026059054:AAEL39Lnezjgsi_mmrrBst7C6DNMMAjH3Ic"
TELEGRAM_CHAT_ID = "5001230025"
URL = "https://en.blackfire.cz/pokemon-company/pokemon-tcg?p=Products&cid=2024934&sort=newest&instock=0&p12=Pok%C3%A9mon+Company&p13=POK%C3%89MON"
DATA_FILE = "last_products.txt"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("❌ Fejl ved afsendelse af besked:", response.text)

def load_last_products():
    if not os.path.exists(DATA_FILE):
        return set()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def save_products(products):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for product in products:
            f.write(product + "\n")

def check_for_products():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    product_headers = soup.select("h4.item-name a")
    current_products = set(a.get_text(strip=True) for a in product_headers)

    last_products = load_last_products()

    new_products = current_products - last_products

    if new_products:
        message = "🆕 Nye produkter fundet:\n\n" + "\n".join(f"• {p}" for p in new_products)
        send_telegram(message)
        save_products(current_products)
    else:
        print("Ingen nye produkter.")

if __name__ == "__main__":
    send_telegram("🛰️ Overvågning startet – tjekker Blackfire...")
    check_for_products()
