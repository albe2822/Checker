import requests
from bs4 import BeautifulSoup

# Direkte Telegram-oplysninger
TELEGRAM_TOKEN = "8026059054:AAEL39Lnezjgsi_mmrrBst7C6DNMMAjH3Ic"
TELEGRAM_CHAT_ID = "5001230025"

# URL til siden du vil overvåge
URL = "https://en.blackfire.cz/pokemon-company/pokemon-tcg?p=Products&cid=2024934&sort=newest&instock=0&p12=Pok%C3%A9mon+Company&p13=POK%C3%89MON"

# Funktion til at sende beskeder via Telegram
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

# Funktion til at hente og parse produkterne
def check_for_products():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    product_headers = soup.select("h4.item-name a")
    product_names = [a.get_text(strip=True) for a in product_headers]

    if product_names:
        message = "🛒 Fundne produkter:\n\n" + "\n".join(f"• {name}" for name in product_names)
        send_telegram(message)
    else:
        send_telegram("⚠️ Ingen produkter fundet.")

# Startbesked og kørsel
send_telegram("🛰️ Overvågning startet – tjekker Blackfire...")
check_for_products()
