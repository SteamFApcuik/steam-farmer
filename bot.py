import time, threading, requests, random, json, os
from telegram import Update
from telegram.ext import Application, CommandHandler

BOT_TOKEN = "8921104068:AAGEV1oPzJqViDGbofYQub4f-3sca92nMEw"

STEAM_LOGIN = "mikimayc39"
STEAM_PASS = "keklolorbidol12#"
GAMES = [570, 730, 440]

stats = {"hours": 0, "games_running": 0}
session = None
running = False

def fm(a):
    if a >= 1000: return f"{a/1000:.0f}K"
    return str(a)

def steam_login():
    global session
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    try:
        r = session.post("https://steamcommunity.com/login/getrsakey", data={"username": STEAM_LOGIN, "donotcache": 0}, timeout=10)
        if r.status_code != 200: return False
        rsa = r.json()
        resp = session.post("https://steamcommunity.com/login/dologin", data={
            "username": STEAM_LOGIN, "password": STEAM_PASS,
            "emailauth": "", "captchagid": "-1", "captcha_text": "",
            "emailsteamid": "", "rsatimestamp": rsa.get("timestamp", 0),
            "remember_login": "false"
        }, timeout=15)
        return resp.status_code == 200 and resp.json().get("success")
    except: return False

def idle_game(appid, minutes=60):
    try:
        session.post(f"https://api.steampowered.com/ISteamApps/UpToDateCheck/v1/", data={"appid": appid, "version": 0}, timeout=5)
        for _ in range(minutes):
            if not running: break
            time.sleep(60)
        stats["hours"] += 1
    except: pass

def farm_loop():
    global running
    while running:
        for appid in GAMES:
            if not running: break
            idle_game(appid, 60)
        time.sleep(10)

async def start(update, context):
    global running
    kb = [[InlineKeyboardButton("🚀 ЗАПУСТИТЬ", callback_data='on')], [InlineKeyboardButton("⏹ ОСТАНОВИТЬ", callback_data='off')], [InlineKeyboardButton("📊 СТАТС", callback_data='st')]]
    await update.message.reply_text(f"🎮 STEAM FARMER\n\nСтатус: {'🟢' if running else '🔴'}\nЧасов: {stats['hours']}\nИгр: {len(GAMES)}\n\nЗапускай:", reply_markup=InlineKeyboardMarkup(kb))

async def btn(update, context):
    global running
    q = update.callback_query; await q.answer(); d = q.data
    if d == 'on':
        if not steam_login():
            await q.edit_message_text("❌ Не удалось зайти в Steam. Проверь логин/пароль.")
            return
        running = True
        threading.Thread(target=farm_loop, daemon=True).start()
        await q.edit_message_text("🚀 Фарм запущен! Dota 2 + CS2 + TF2.\nЧасы идут каждую минуту.")
    elif d == 'off':
        running = False
        await q.edit_message_text(f"⏹ Остановлен. Часов: {stats['hours']}")
    elif d == 'st':
        await q.edit_message_text(f"📊 Статус: {'🟢' if running else '🔴'}\nЧасов: {stats['hours']}\nИгр: {len(GAMES)}")

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btn))
    app.run_polling()

if __name__ == "__main__":
    main()
