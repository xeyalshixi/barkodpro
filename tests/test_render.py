#!/usr/bin/env python3
"""Brauzer testləri (Playwright): JS xətası yoxdur, gündüz rejimində bölmələr ağdır,
gecə rejimində tünddür, kalkulyatorlar və demo işləyir, telefonda üfüqi sürüşmə yoxdur.

Quraşdırma:  pip install playwright && playwright install chromium
İşə salmaq:  python3 tests/test_render.py
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "mobil-izleme.html", "about.html", "contact.html", "privacy.html", "login.html"]
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
    """rgb(...)/rgba(...) və color(srgb r g b / a) formatlarını 0–255 RGB-yə çevirir."""
    inner = s[s.index("(") + 1:s.rindex(")")]
    if inner.startswith("srgb"):
        return tuple(round(float(x) * 255) for x in inner.split("/")[0].split()[1:4])
    return tuple(int(float(x)) for x in inner.split(",")[:3])

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
                h_col = await pg.evaluate("getComputedStyle(document.querySelector('main h1, main h2')).color")
                lum = sum(rgb(h_col)) / 3
                check(lum < 80 if scheme == "light" else lum > 180, f"{scheme} {name}: h1 rəngi fonla uyğun deyil ({h_col})")
                await pg.close()

        # Giriş → POS paneli: hər iki rejimdə tema, satış, çek, qaytarma, növbə
        for scheme in ("light", "dark"):
            pg, errs = await open_page(b, "login.html", scheme)
            pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await pg.fill("#u", "Test"); await pg.fill("#pw", "x")
            for i, c in enumerate("123456"):
                await pg.fill(f"#otp input:nth-child({i+1})", c)
            await pg.click("#go"); await pg.wait_for_url("**/dashboard.html*"); await pg.wait_for_timeout(400)
            check(not errs, f"{scheme} login/dashboard: JS xətası {errs}")
            check(await pg.inner_text("#av") == "T", f"{scheme}: istifadəçi adı panelə ötürülmədi")
            for sel in (".top", ".card", ".pc"):
                c = await pg.evaluate(f"getComputedStyle(document.querySelector('{sel}')).backgroundColor")
                lum = sum(rgb(c)) / 3
                check(lum > 200 if scheme == "light" else lum < 50, f"{scheme} dashboard {sel}: rəng temaya uyğun deyil ({c})")
            await pg.evaluate("localStorage.removeItem('bp-pos-demo-v3')")
            for i in (1, 2, 2): await pg.click(f"#pgrid .pc:nth-child({i})")
            check(await pg.locator("#lines .ln").count() == 2, f"{scheme}: səbətdə 2 sətir gözlənilirdi")
            n0 = await pg.evaluate("D.sales.length")
            await pg.click("#payBtn"); await pg.wait_for_timeout(200)
            check(await pg.evaluate("D.sales.length") == n0 + 1, f"{scheme}: satış yazılmadı")
            check("Satış tamamlandı" in await pg.inner_text("#mT"), f"{scheme}: çek pəncərəsi açılmadı")
            await pg.click("#mX")
            for s in ("panel", "mallar", "qebul", "sayim", "satislar", "hesabat", "novbe", "musteri", "tedarukcu", "ayarlar"):
                await pg.evaluate(f"go('{s}')")
                check(await pg.is_visible(f"#s-{s}"), f"dashboard: {s} ekranı açılmadı")
            await pg.evaluate("go('satislar')"); await pg.click("#slTab tr:first-child button[title=Qaytar]")
            check(await pg.evaluate("D.sales[D.sales.length-1].status") == "ret", f"{scheme}: qaytarma işləmədi")
            no = await pg.evaluate("D.shift.no"); await pg.evaluate("go('novbe')"); await pg.click("#zRep"); await pg.click("#zOk")
            check(await pg.evaluate("D.shift.no") == no + 1, f"{scheme}: növbə bağlanmadı")
            check(not errs, f"{scheme} dashboard axını: JS xətası {errs}")
            await pg.close()

        # Telefonda: alt menyu, səbət vərəqi, üfüqi sürüşmə yoxdur
        mc = await b.new_context(viewport={"width": 375, "height": 812}, is_mobile=True, has_touch=True)
        mp = await mc.new_page(); await mp.route("**/fonts.g*/**", lambda r: r.abort())
        await mp.goto(f"file://{ROOT}/dashboard.html"); await mp.wait_for_timeout(400)
        check(await mp.is_visible("#bnav") and not await mp.is_visible(".side"), "telefon: alt menyu görünmür")
        await mp.tap("#pgrid .pc:nth-child(1)"); await mp.tap("#cbar"); await mp.wait_for_timeout(350)
        box = await mp.locator("#cart").bounding_box()
        check(box and box["y"] < 812 * 0.5, "telefon: səbət vərəqi açılmadı")
        check(await mp.evaluate("document.documentElement.scrollWidth") <= 375, "telefon: dashboard üfüqi sürüşür")
        await mc.close()

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
