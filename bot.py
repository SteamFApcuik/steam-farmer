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
