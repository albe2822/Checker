import os
import time
import requests

TELEGRAM_TOKEN = "8026059054:AAEL39Lnezjgsi_mmrrBst7C6DNMMAjH3Ic"
TELEGRAM_CHAT_ID = "5001230025"
CHECKED_FILE = "last_checked.txt"
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, data=payload)

def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def main():
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

                if text == "/lastcheck":
                    if os.path.exists(CHECKED_FILE):
                        with open(CHECKED_FILE, "r") as f:
                            last_check = f.read().strip()
                        send_message(chat_id, f"Seneste tjek var: {last_check}")
                    else:
                        send_message(chat_id, "Ingen oplysninger om sidste tjek endnu.")
                else:
                    send_message(chat_id, "Ukendt kommando. Prøv /lastcheck")

        time.sleep(1)  # Undgå at spamme API'en

if __name__ == "__main__":
    main()
