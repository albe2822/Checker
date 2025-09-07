import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import time

TELEGRAM_TOKEN = "8026059054:AAEL39Lnezjgsi_mmrrBst7C6DNMMAjH3Ic"
TELEGRAM_CHAT_ID = "5001230025"
URL = "https://b2b.blackfire.cz/pokemon-company?p=Products&p12=Pok%C3%A9mon+Company"
DATA_FILE = "last_products.txt"
CHECKED_FILE = "last_checked.txt"
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_telegram(message, chat_id=TELEGRAM_CHAT_ID):
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
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

def save_check_time():
    tz = ZoneInfo("Europe/Copenhagen")
    now = datetime.now(tz)
    formatted_time = now.strftime("%d %H:%M")  # fx "11 14:30"
    with open(CHECKED_FILE, "w", encoding="utf-8") as f:
        f.write(formatted_time)

def check_for_products():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except Exception as e:
        send_telegram(f"❌ Fejl ved hentning af siden: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    product_headers = soup.select("h4.item-name a")
    current_products = set(a.get_text(strip=True) for a in product_headers)

    last_products = load_last_products()
    new_products = current_products - last_products

    # Overskriv filen med kun de aktuelle produkter
    save_products(current_products)

    if new_products:
        message = "🆕 Nye produkter fundet:\n\n" + "\n".join(f"• {p}" for p in new_products)
        send_telegram(message)
    else:
        print("Ingen nye produkter.")

    save_check_time()

def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    try:
        response = requests.get(url, params=params, timeout=120)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Fejl ved hentning af opdateringer:", e)
        return None

def handle_updates():
    last_update_id = None
    while True:
        updates = get_updates(offset=last_update_id)
        if updates and updates.get("result"):
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                message = update.get("message")
                if not message:
                    continue
                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                if text == "/lc":
                    if os.path.exists(CHECKED_FILE):
                        with open(CHECKED_FILE, "r", encoding="utf-8") as f:
                            last_check = f.read().strip()
                        send_telegram(f"Seneste tjek var: {last_check}", chat_id=chat_id)
                    else:
                        send_telegram("Ingen oplysninger om sidste tjek endnu.", chat_id=chat_id)
                else:
                    send_telegram("Ukendt kommando: Prøv /lc", chat_id=chat_id)
        time.sleep(1)

if __name__ == "__main__":
    # Send start-besked
    send_telegram("🛰️ Overvågning startet – tjekker Blackfire...")

    # Tjek produkter én gang
    check_for_products()
