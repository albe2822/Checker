import requests
from bs4 import BeautifulSoup
import hashlib
import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

URL = "https://en.blackfire.cz/pokemon-company/pokemon-tcg?p=Products&cid=2024934&sort=newest&instock=0&p12=Pok%C3%A9mon+Company&p13=POK%C3%89MON"
HASH_FILE = "last_product_hash.txt"

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(telegram_url, data=payload)
        if response.status_code != 200:
            print("Fejl ved afsendelse af besked:", response.text)
    except Exception as e:
        print("Fejl:", e)

def get_site_content():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    product_elements = soup.select('.product-title a')
    product_names = [p.text.strip() for p in product_elements]
    return "\n".join(product_names)

def get_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

def load_last_hash():
    try:
        with open(HASH_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def save_hash(hash_value):
    with open(HASH_FILE, "w") as f:
        f.write(hash_value)

def main():
    send_telegram_message("✅ Blackfire overvågning startet.")

    content = get_site_content()
    current_hash = get_hash(content)
    old_hash = load_last_hash()

    if current_hash != old_hash:
        send_telegram_message("⚠️ Der er nye Pokémon-produkter på Blackfire!\n" + URL)
        save_hash(current_hash)
    else:
        print("Ingen nye produkter.")

if __name__ == "__main__":
    main()