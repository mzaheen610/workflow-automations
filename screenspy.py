"""A script to capture the desktop screen and send it to a Telegram chat at regular intervals."""
import os
import time

import dotenv
import pyautogui
import requests
import schedule

dotenv.load_dotenv()

# Configuration
TOKEN = os.getenv("TELEGRAM_BOT_API")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("CHAT_ID")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def print_full_screen(image_name: str, target):
        image_name = os.path.join(BASE_DIR, "Screenshots", f"{image_name}.png")
        image = pyautogui.screenshot(image_name)
        image.save(image_name)
        return image_name

def send_screenshot():
    if not TOKEN:
        print("Error: TELEGRAM_BOT_API is not set")
        return

    if not CHAT_ID:
        print("Error: TELEGRAM_CHAT_ID or CHAT_ID is not set")
        return

    # Capture screen
    image_name = f"screenshot_{int(time.time())}"
    screenshot_path = print_full_screen(image_name, "primary")
    # Send to Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    with open(screenshot_path, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID, "caption": "Desktop Update"}
        try:
            response = requests.post(url, files=files, data=data, timeout=30)
            response.raise_for_status()
            payload = response.json()
            if not payload.get("ok"):
                print(f"Telegram API error: {payload}")
        except Exception as e:
            print(f"Error: {e}")
            
    # Clean up
    os.remove(screenshot_path)

# Schedule every 10 minutes
schedule.every(10).minutes.do(send_screenshot)

print("Monitoring started...")
while True:
    schedule.run_pending()
    time.sleep(1)