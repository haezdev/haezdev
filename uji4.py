import time, urllib.request as u
from playwright.sync_api import sync_playwright

URL = "https://haezdev.github.io/haezdev/v/?v=5"

# tunggu GitHub Pages siap bina
for i in range(14):
    try:
        req = u.Request(URL, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
        t = u.urlopen(req, timeout=25).read().decode("utf-8", "replace")
        if "Ketuk untuk buka jemputan" in t:
            print("PAGES SIAP:", i, "len", len(t))
            break
        print(i, "belum, len", len(t))
    except Exception as e:
        print(i, "err", e)
    time.sleep(10)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 412, "height": 900}, has_touch=True, is_mobile=True)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL, wait_until="load", timeout=60000)
    time.sleep(2.5)

    awal = pg.evaluate("() => { const v=document.getElementById('player'); return {paused:v.paused, muted:v.muted, opacity:getComputedStyle(v).opacity, skrin:'pintu'}; }")
    print("SEBELUM KLIK :", awal)
    pg.screenshot(path="C:/Users/TOSHIBA/vidwork/before.png")

    pg.tap("#pintu")
    time.sleep(2.2)

    lepas = pg.evaluate("() => { const v=document.getElementById('player'); return {paused:v.paused, muted:v.muted, vol:v.volume, t:+v.currentTime.toFixed(2), opacity:getComputedStyle(v).opacity, pintu:getComputedStyle(document.getElementById('pintu')).opacity}; }")
    print("SELEPAS KLIK :", lepas)
    pg.screenshot(path="C:/Users/TOSHIBA/vidwork/after.png")
    print("JS_ERRORS    :", errs)
    b.close()
