#!/usr/bin/env python3
"""Brauzer testləri (Playwright): JS xətası yoxdur, gündüz rejimində bölmələr ağdır,
gecə rejimində tünddür, kalkulyatorlar və demo işləyir, telefonda üfüqi sürüşmə yoxdur.

Quraşdırma:  pip install playwright && playwright install chromium
İşə salmaq:  python3 tests/test_render.py
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "mobil-izleme.html", "about.html", "contact.html", "privacy.html"]
fails = []

def check(c, m):
    if not c: fails.append(m)

async def open_page(b, name, scheme, width=1280, hash_=""):
    pg = await b.new_page(viewport={"width": width, "height": 860}, color_scheme=scheme)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.route("**/fonts.g*/**", lambda r: r.abort())
    await pg.goto(f"file://{ROOT}/{name}{hash_}")
    await pg.wait_for_timeout(800)
    return pg, errs

def rgb(s):
    return tuple(int(x) for x in s[s.index("(") + 1:s.index(")")].split(",")[:3])

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for scheme in ("light", "dark"):
            for name in PAGES:
                pg, errs = await open_page(b, name, scheme)
                check(not errs, f"{scheme} {name}: JS xətası {errs}")
                bands = await pg.evaluate("[...document.querySelectorAll('.hero-band,section.dark,footer.dark,.out')].map(e=>getComputedStyle(e).backgroundColor)")
                for c in bands:
                    lum = sum(rgb(c)) / 3
                    if scheme == "light":
                        check(lum > 230, f"light {name}: tünd bölmə qalıb ({c})")
                    else:
                        check(lum < 40, f"dark {name}: bölmə açıq rəngdədir ({c})")
                # mətn fonla kontrast: başlıqlar oxunaqlıdır
                h_col = await pg.evaluate("getComputedStyle(document.querySelector('h1')).color")
                lum = sum(rgb(h_col)) / 3
                check(lum < 80 if scheme == "light" else lum > 180, f"{scheme} {name}: h1 rəngi fonla uyğun deyil ({h_col})")
                await pg.close()

        # Gecə/gündüz düyməsi işləyir və yadda qalır
        pg, _ = await open_page(b, "index.html", "light")
        await pg.click("#thm")
        bg = await pg.evaluate("getComputedStyle(document.querySelector('.hero-band')).backgroundColor")
        check(sum(rgb(bg)) / 3 < 40, "tema düyməsi hero-nu tünd etmədi")
        await pg.close()

        # Kalkulyatorlar
        pg, errs = await open_page(b, "index.html", "light")
        check((await pg.inner_text("#sBig")).startswith("865,00"), "maaş: 1000 ₼ → 865,00 gözlənilirdi")
        await pg.click("#ttabs [data-t=endirim]")
        check((await pg.inner_text("#dBig")).startswith("10,20"), "endirim: 12 ₼ −15% = 10,20 gözlənilirdi")
        await pg.click("#ttabs [data-t=dovr]")
        check((await pg.inner_text("#tBig")).startswith("22,5"), "dövriyyə: 45000/2000 = 22,5 gün gözlənilirdi")
        await pg.click("#ttabs [data-t=barkod]")
        # 476000123456 → yoxlama rəqəmi 4 (EAN-13)
        check((await pg.inner_text("#bMsg")).strip() == "Yoxlama rəqəmi: 4", "barkod: yoxlama rəqəmi səhvdir")
        check(await pg.get_attribute("#bDl", "download") == "barkod-4760001234564.svg", "barkod: SVG faylının adı səhvdir")
        await pg.close()

        # #maas kimi hash birbaşa aləti açır
        pg, _ = await open_page(b, "index.html", "light", hash_="#endirim")
        check(await pg.get_attribute("#ttabs [data-t=endirim]", "aria-selected") == "true", "#endirim hash aləti açmadı")
        await pg.close()

        # Mobil İzləmə demo tabları
        pg, _ = await open_page(b, "mobil-izleme.html", "light")
        await pg.click("#dtabs button:nth-child(5)")
        check("Yeni kassa məxaric" in await pg.inner_text("#scr"), "demo: kassa sənədi ekranı açılmadı")
        await pg.close()

        # Telefonda üfüqi sürüşmə yoxdur
        for name in PAGES:
            pg, _ = await open_page(b, name, "light", width=375)
            sw = await pg.evaluate("document.documentElement.scrollWidth")
            check(sw <= 375, f"{name}: telefonda üfüqi sürüşmə ({sw}px)")
            await pg.close()
        await b.close()

asyncio.run(main())
if fails:
    print(f"UĞURSUZ: {len(fails)} yoxlama")
    for f in fails: print("  ✗", f)
    sys.exit(1)
print("Bütün brauzer testləri keçdi ✓")
