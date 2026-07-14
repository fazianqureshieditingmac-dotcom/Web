import requests
import time
import random
from bs4 import BeautifulSoup

# =========================
# SETTINGS
# =========================
URL = "https://www.goethe.de/ins/pk/en/spr/prf/gza1.cfm"
WEBHOOK_URL = "https://discord.com/api/webhooks/1526522806991585391/BoVGmryW_u90BTD2JcxYrRZweDG_WxZuEO6Emnzlle4GxAwDUYxPLSftJPZ1kGeIAcG7"
CHECK_INTERVAL = 30  # Check every 30 seconds

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7790.70 Safari/537.36"
}

# =========================
# SEND DISCORD NOTIFICATION
# =========================
def send_discord(message):
    try:
        data = {"content": message}
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("✅ Discord notification sent!")
        else:
            print(f"⚠️ Discord error: {response.status_code}")
    except Exception as e:
        print(f"❌ Discord failed: {e}")

# =========================
# CHECK WEBSITE
# =========================
def check_button():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        # Check if btnGruen button exists
        buttons = soup.find_all("button", class_="btnGruen")
        return len(buttons) > 0

    except Exception as e:
        print(f"⚠️ Check error: {e}")
        return False

# =========================
# MAIN MONITOR LOOP
# =========================
print("🔍 Goethe Monitor Started!")
print(f"🌐 Watching: {URL}")
print(f"⏱️  Checking every {CHECK_INTERVAL} seconds")
print("Running in cloud — will notify on Discord when button appears!\n")

# Send startup message
send_discord("🟢 **Goethe Monitor Started!**\nWatching for booking button on:\n" + URL)

check_count = 0

while True:
    check_count += 1
    print(f"[Check #{check_count}] Checking website...")

    button_found = check_button()

    if button_found:
        print("🔔 BUTTON FOUND!")
        send_discord(
            f"🔔 @everyone **BOOKING BUTTON IS LIVE!**\n"
            f"🚨 GO REGISTER NOW!\n"
            f"🔗 {URL}\n"
            f"⏰ Found on check #{check_count}"
        )
        # Keep checking every 5 minutes to re-notify in case you missed it
        print("✅ Notification sent! Re-checking every 5 minutes...")
        time.sleep(300)
    else:
        print(f"[Check #{check_count}] ❌ Button not found — waiting {CHECK_INTERVAL}s...")
        time.sleep(CHECK_INTERVAL + random.uniform(1, 10))
