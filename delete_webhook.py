import os
import requests

TOKEN = os.environ.get("BOT_TOKEN")  # Railway-də Config Vars-da əlavə olunmuş token

if not TOKEN:
    print("❌ BOT_TOKEN təyin edilməyib!")
else:
    url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
    response = requests.get(url)
    print(response.json())