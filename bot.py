import time, threading, json, os, urllib.request, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

BOT_TOKEN = "8921104068:AAGEV1oPzJqViDGbofYQub4f-3sca92nMEw"
STEAM_LOGIN = "mikimayc39"
STEAM_PASS = "keklolorbidol12#"
GAMES = [570, 730, 440]
stats = {"hours": 0}
session_cookies = ""
running = False

def http_post(url, data):
    d = urllib.parse.urlencode(data).encode()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://steamcommunity.com",
        "Referer": "https://steamcommunity.com/login/",
    }
    req = urllib.request.Request(url, data=d, headers=headers)
    return urllib.request.urlopen(req, timeout=15).read().decode()

def steam_login():
    global session_cookies
    try:
        # Сначала заходим на страницу логина (получаем куки)
        opener = urllib.request.build_opener()
        opener.open(urllib.request.Request("https://steamcommunity.com/login/", headers={"User-Agent": "Mozilla/5.0"}))
        
        r = http_post("https://steamcommunity.com/login/getrsakey", {"username": STEAM_LOGIN, "donotcache": 0})
        rsa = json.loads(r)
        resp = http_post("https://steamcommunity.com/login/dologin", {
            "username": STEAM_LOGIN, "password": STEAM_PASS,
            "emailauth": "", "captchagid": "-1", "captcha_text": "",
            "emailsteamid": "", "rsatimestamp": rsa.get("timestamp", 0),
            "remember_login": "true"
        })
        result = json.loads(resp)
        if result.get("success"):
            return True
        elif result.get("requires_twofactor"):
            print("Нужен Steam Guard код!")
            return False
        elif result.get("message"):
            print(f"Ошибка: {result['message']}")
            return False
        return False
    except Exception as e:
        print(f"Login error: {e}")
        return False

def idle_game(appid, minutes=60):
    try:
        http_post("https://api.steampowered.com/ISteamApps/UpToDateCheck/v1/", {"appid": appid, "version": 0})
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

async def start(update, context):
    kb = [[InlineKeyboardButton("🚀 ЗАПУСТИТЬ", callback_data='on')], [InlineKeyboardButton("⏹ СТОП", callback_data='off')], [InlineKeyboardButton("📊 СТАТС", callback_data='st')]]
    await update.message.reply_text(f"🎮 STEAM FARMER\nСтатус: {'🟢' if running else '🔴'}\nЧасов: {stats['hours']}\nИгр: {len(GAMES)}", reply_markup=InlineKeyboardMarkup(kb))

async def btn(update, context):
    global running
    q = update.callback_query; await q.answer(); d = q.data
    if d == 'on':
        if not steam_login():
            await q.edit_message_text("❌ Не удалось зайти в Steam.")
            return
        running = True
        threading.Thread(target=farm_loop, daemon=True).start()
        await q.edit_message_text("🚀 Фарм запущен! Dota 2 + CS2 + TF2.")
    elif d == 'off':
        running = False
        await q.edit_message_text(f"⏹ Стоп. Часов: {stats['hours']}")
    elif d == 'st':
        await q.edit_message_text(f"📊 Статус: {'🟢' if running else '🔴'}\nЧасов: {stats['hours']}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btn))
    app.run_polling()

if __name__ == "__main__":
    main()
