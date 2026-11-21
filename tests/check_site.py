#!/usr/bin/env python3
"""Statik yoxlamalar: metadata, JSON-LD, sitemap, robots, llms.txt, Markdown versiyalar,
etibar səhifələri, 404 və daxili linklər. Yalnız standart kitabxana.

İşə salmaq:  python3 tests/check_site.py
"""
import html.parser, json, os, re, sys, xml.etree.ElementTree as ET
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://xeyalshixi.github.io/barkodpro/"
INDEXABLE = ["index.html", "mobil-izleme.html", "anbar-terminal.html", "about.html", "contact.html", "privacy.html"]
TRUST = ["about.html", "contact.html", "privacy.html"]
AI_AGENTS = ["GPTBot", "ClaudeBot", "Claude-User", "PerplexityBot", "Google-Extended", "OAI-SearchBot", "ChatGPT-User"]

fails = []
def check(cond, msg):
    if not cond:
        fails.append(msg)
    return cond

def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()

def local_path(url):
    """BASE altındakı URL-i repo faylına çevirir (yoxdursa None)."""
    if not url.startswith(BASE):
        return None
    path = urlparse(url).path[len("/barkodpro/"):] or "index.html"
    return path

class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None; self.meta = {}; self.links = []; self.ld = []; self.hrefs = []
        self.text = []; self._ld = False; self._skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang")
        if tag == "meta":
            k = a.get("property") or a.get("name")
            if k: self.meta[k] = a.get("content", "")
        if tag == "link": self.links.append(a)
        if tag == "a" and a.get("href"): self.hrefs.append(a["href"])
        if tag == "script":
            self._skip += 1
            if a.get("type") == "application/ld+json": self._ld = True; self.ld.append("")
        if tag == "style": self._skip += 1
    def handle_endtag(self, tag):
        if tag in ("script", "style"): self._skip -= 1; self._ld = False
    def handle_data(self, d):
        if self._ld: self.ld[-1] += d
        elif not self._skip: self.text.append(d)

def parse(name):
    p = Parser(); p.feed(read(name)); return p

def ld_nodes(p):
    nodes = []
    for raw in p.ld:
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError as e:
            fails.append(f"JSON-LD parse xətası: {e}"); continue
        nodes += doc.get("@graph", [doc])
    return nodes

def types(n):
    t = n.get("@type", []); return t if isinstance(t, list) else [t]

# 1. Metadata hər indekslənən səhifədə
sitemap_locs = []
for name in INDEXABLE:
    p = parse(name)
    check(p.lang == "az", f"{name}: <html lang> yoxdur")
    canon = [l["href"] for l in p.links if l.get("rel") == "canonical"]
    check(len(canon) == 1 and canon[0].startswith(BASE), f"{name}: canonical BASE altında deyil: {canon}")
    check(p.meta.get("og:image", "").startswith("https://"), f"{name}: og:image mütləq URL deyil")
    check(p.meta.get("og:type") == "website", f"{name}: og:type yoxdur")
    check(p.meta.get("og:url") == (canon[0] if canon else None), f"{name}: og:url canonical ilə eyni deyil")
    check(bool(p.meta.get("description")), f"{name}: description yoxdur")
    check(len(p.ld) >= 1, f"{name}: JSON-LD yoxdur")
    nodes = ld_nodes(p)
    org = [n for n in nodes if "Organization" in types(n)]
    check(org, f"{name}: Organization JSON-LD yoxdur")
    for o in org:
        cps = o.get("contactPoint"); cps = cps if isinstance(cps, list) else [cps]
        check(all(c and c.get("telephone") and c.get("contactType") for c in cps), f"{name}: contactPoint natamamdır")
        check((o.get("address") or {}).get("@type") == "PostalAddress", f"{name}: PostalAddress yoxdur")

# 2. Ana səhifə — tam Organization, açar sözlər, Markdown alternativi, GitHub linki
home = parse("index.html")
org = next(n for n in ld_nodes(home) if "Organization" in types(n))
for k in ("name", "url", "description", "logo", "sameAs", "knowsAbout", "makesOffer"):
    check(org.get(k), f"index.html: Organization.{k} yoxdur")
alt_md = [l["href"] for l in home.links if l.get("type") == "text/markdown"]
check(alt_md == [BASE + "index.md"], f"index.html: Markdown alternate link: {alt_md}")
check(any("github.com/xeyalshixi" in h for h in home.hrefs), "index.html: GitHub linki yoxdur")
check(bool(home.meta.get("keywords")), "index.html: meta keywords yoxdur")

# 3. Sitemap
try:
    tree = ET.parse(os.path.join(ROOT, "sitemap.xml"))
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    check(tree.getroot().tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset", "sitemap: urlset namespace səhvdir")
    for u in tree.getroot().findall("s:url", ns):
        loc = u.findtext("s:loc", namespaces=ns); lm = u.findtext("s:lastmod", namespaces=ns)
        sitemap_locs.append(loc)
        lp = local_path(loc)
        check(lp and os.path.isfile(os.path.join(ROOT, lp)), f"sitemap: fayl yoxdur: {loc}")
        check(lm and re.fullmatch(r"\d{4}-\d{2}-\d{2}", lm), f"sitemap: lastmod səhvdir: {loc}")
    check(os.path.getsize(os.path.join(ROOT, "sitemap.xml")) < 50 * 1024 * 1024, "sitemap: 50MB-dan böyükdür")
except ET.ParseError as e:
    fails.append(f"sitemap.xml XML deyil: {e}")
for name in INDEXABLE:
    want = BASE if name == "index.html" else BASE + name
    check(want in sitemap_locs, f"sitemap: {want} yoxdur")
for blocked in ("dashboard.html", "login.html", "404.html"):
    check(BASE + blocked not in sitemap_locs, f"sitemap: {blocked} olmamalıdır")

# 4. robots.txt
robots = read("robots.txt")
check(f"Sitemap: {BASE}sitemap.xml" in robots.splitlines(), "robots.txt: Sitemap sətri yoxdur")
check(not re.search(r"^Disallow:\s*/\s*$", robots, re.M), "robots.txt: bütün sayt bağlanıb")
for ua in AI_AGENTS:
    check(not re.search(rf"User-agent:\s*{ua}\s*\n\s*Disallow:\s*/\s*$", robots, re.M | re.I), f"robots.txt: {ua} bloklanıb")

# 5. llms.txt (llmstxt.org formatı)
llms = read("llms.txt"); lines = llms.splitlines()
check(lines[0].startswith("# ") and not lines[0].startswith("## "), "llms.txt: H1 ilə başlamır")
first_body = next(l for l in lines[1:] if l.strip())
check(first_body.startswith("> "), "llms.txt: H1-dən sonra blockquote xülasə yoxdur")
check("When to use" in llms, "llms.txt: 'When to use' bölməsi yoxdur")
check("How an agent should engage" in llms, "llms.txt: agentin necə müraciət edəcəyi yazılmayıb")
pre_h2 = llms.split("\n## ")[0]
check(not re.search(r"^#{2,} ", pre_h2, re.M), "llms.txt: ilk H2-dən əvvəl başlıq olmamalıdır")
for sec in llms.split("\n## ")[1:]:
    for l in sec.splitlines()[1:]:
        if l.strip():
            check(re.match(r"^- \[[^\]]+\]\([^)]+\)(:.*)?", l), f"llms.txt: link siyahısı formatı səhvdir: {l[:60]}")
for url in re.findall(r"\]\((https?://[^)]+)\)", llms):
    lp = local_path(url.split("#")[0])
    if lp is not None:
        check(os.path.isfile(os.path.join(ROOT, lp)), f"llms.txt: fayl yoxdur: {url}")

# 6. Markdown versiyalar
for md in ("index.md", "mobil-izleme.md"):
    t = read(md)
    check(t.startswith("# ") and len(t) > 1000, f"{md}: boş və ya başlıqsızdır")
check(os.path.isfile(os.path.join(ROOT, ".nojekyll")), ".nojekyll yoxdur (.md fayllar xam verilməlidir)")

# 7. Etibar səhifələri ≥500 simvol mətn
for name in TRUST:
    text = re.sub(r"\s+", " ", " ".join(parse(name).text)).strip()
    main = text.split("BarkodPRO /", 1)[-1]
    check(len(main) >= 500, f"{name}: məzmun qısadır ({len(main)} simvol)")

# 8. 404 — agentlər üçün izah və linklər
nf = parse("404.html")
check("404" in " ".join(nf.text) and "/barkodpro/llms.txt" in nf.hrefs and "/barkodpro/sitemap.xml" in nf.hrefs, "404.html: llms.txt/sitemap linki yoxdur")
check(all(not re.match(r"^(?!https?:|#|tel:|mailto:|/)", h) for h in nf.hrefs), "404.html: nisbi link var (iç-içə yollarda qırılır)")

# 9. Daxili linklər mövcud fayllara aparır
for name in INDEXABLE + ["404.html"]:
    for h in parse(name).hrefs:
        if re.match(r"^(https?:|#|tel:|mailto:)", h):
            continue
        path = h.split("#")[0]
        if path.startswith("/barkodpro/"): path = path[len("/barkodpro/"):]
        path = path or "index.html"
        check(os.path.isfile(os.path.join(ROOT, path)), f"{name}: qırıq link {h}")

# 10. Məxfilik siyasətindəki iddia: izləmə skripti yoxdur
for name in [f for f in os.listdir(ROOT) if f.endswith(".html")] + ["assets/js/site.js"]:
    check(not re.search(r"gtag\(|googletagmanager|google-analytics|mc\.yandex|fbq\(", read(name)), f"{name}: analitika skripti var — privacy.html-i yeniləyin")

if fails:
    print(f"UĞURSUZ: {len(fails)} yoxlama")
    for f in fails: print("  ✗", f)
    sys.exit(1)
print("Bütün statik yoxlamalar keçdi ✓")
