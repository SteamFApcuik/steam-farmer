import subprocess, time, threading, os, json
from telegram import Update
from telegram.ext import Application, CommandHandler

BOT_TOKEN = "8921104068:AAGEV1oPzJqViDGbofYQub4f-3sca92nMEw"

STEAM_CONFIG = {
    "SteamLogin": "mikimayc39",
    "SteamPassword": "keklolorbidol12#",
    "Enabled": True,
    "GamesPlayedWhileIdle": [570],
    "FarmOffline": False,
    "HoursUntilCardDrops": 0
}

async def start(update, context):
    await update.message.reply_text("Бот работает. Dota 2 фармится 24/7.")

def setup_asf():
    os.makedirs("/app/asf/config", exist_ok=True)
    with open("/app/asf/config/bot.json", "w") as f:
        json.dump(STEAM_CONFIG, f)
    subprocess.Popen(["dotnet", "ArchiSteamFarm.dll", "--headless"], cwd="/app/asf")

def main():
    threading.Thread(target=setup_asf, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
