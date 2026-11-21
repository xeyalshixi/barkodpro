#!/usr/bin/env python3
"""about.html, contact.html, privacy.html səhifələrini mobil-izleme.html-in başlıq/footer/stilindən yaradır.
Mətni dəyişmək üçün bu fayldakı page(...) çağırışlarını düzəldib işə salın:  python3 tools/gen_pages.py"""
import json,re,sys
import os
root=sys.argv[1] if len(sys.argv)>1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE='https://xeyalshixi.github.io/barkodpro/'
src=open(root+'/mobil-izleme.html',encoding='utf-8').read()
css=re.search(r'<style>(.*?)</style>',src,re.S).group(1)
# keep only generic parts (vars, base, header, buttons, footer)
keep=[]
for line in css.split('\n'):
    if line.startswith('/* hero */'):break
    keep.append(line)
foot=re.search(r'/\* footer \*/.*?(?=@media\(prefers-reduced-motion)',css,re.S).group(0)
css='\n'.join(keep)+'\n'+foot+'''
.page{max-width:820px}
.page h1{font-size:clamp(34px,4.5vw,52px);margin:8px 0 18px}
.page h2{font-size:clamp(22px,2.6vw,28px);margin:38px 0 12px}
.page p,.page li{color:var(--mute);font-size:17px;line-height:1.65}
.page p+p{margin-top:12px}
.page ul{padding-left:22px;display:grid;gap:6px;margin:10px 0 0}
.page b{color:var(--ink)}
.crumb{font-size:14px;color:var(--mute)}.crumb a{text-decoration:none}.crumb a:hover{color:var(--ink)}
.ways{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,230px),1fr));gap:12px;margin-top:20px}
.way{display:block;padding:18px;border:1px solid var(--line);border-radius:14px;text-decoration:none;background:var(--card)}
.way b{display:block;font-size:18px}.way span{color:var(--mute);font-size:14.5px}
.upd{font-size:14px;color:var(--mute);margin-top:30px;border-top:1px solid var(--line);padding-top:14px}
'''
hdr=re.search(r'<header>.*?</header>',src,re.S).group(0).replace(' aria-current="page"','')
ftr=re.search(r'<footer class="dark">.*?</footer>',src,re.S).group(0).replace('<a href="login.html">Müştəri girişi</a>','<a href="about.html">Haqqımızda</a><a href="contact.html">Əlaqə</a><a href="privacy.html">Məxfilik siyasəti</a><a href="login.html">Müştəri girişi</a>')
wa=re.search(r'<a class="wa".*?</a>',src,re.S).group(0)
script=re.search(r'/\* menyu \*/.*?(?=/\* ===== Canlı demo)',src,re.S).group(0)
ORG={"@type":["Organization","LocalBusiness"],"@id":BASE+"#org","name":"BarkodPRO","url":BASE,"telephone":"+994516782878","address":{"@type":"PostalAddress","addressLocality":"Şamaxı","addressCountry":"AZ"},"contactPoint":{"@type":"ContactPoint","telephone":"+994516782878","contactType":"customer support","availableLanguage":["az","ru"]}}
def page(fn,title,desc,typ,crumb,body):
    url=BASE+fn
    ld={"@context":"https://schema.org","@graph":[{"@type":typ,"@id":url+"#page","url":url,"name":title,"description":desc,"inLanguage":"az","about":{"@id":BASE+"#org"},"isPartOf":{"@type":"WebSite","url":BASE,"name":"BarkodPRO"}},ORG,
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"BarkodPRO","item":BASE},{"@type":"ListItem","position":2,"name":crumb,"item":url}]}]}
    html=f'''<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — BarkodPRO</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title} — BarkodPRO">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}assets/img/og-cover.png">
<meta property="og:site_name" content="BarkodPRO">
<meta property="og:locale" content="az_AZ">
<meta name="theme-color" content="#111214">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="text/plain" href="{BASE}llms.txt" title="llms.txt">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;800&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
{hdr}
<main class="band"><article class="wrap page">
<p class="crumb"><a href="index.html">BarkodPRO</a> / {crumb}</p>
{body}
</article></main>
{ftr}
{wa}
<script>
{{
const $=s=>document.querySelector(s);
{script}$('#yr').textContent=new Date().getFullYear();
}}
</script>
</body>
</html>
'''
    open(root+'/'+fn,'w',encoding='utf-8').write(html)

page('about.html','Haqqımızda','BarkodPRO — Azərbaycanda 1C:Enterprise əsasında kassa, e-kassa, anbar terminalı və mobil hesabat sistemləri quran müstəqil tərtibatçı. Necə işləyirik, nə edirik.','AboutPage','Haqqımızda','''
<h1>BarkodPRO haqqında</h1>
<p><b>BarkodPRO</b> — 1C:Enterprise əsasında ticarət və anbar sistemləri quran müstəqil tərtibatçıdır. Şamaxıda yerləşirik, işin çoxunu uzaqdan, bütün Azərbaycan üzrə görürük. 5 ildən artıqdır ki, market, restoran, aptek, anbar və topdan satış obyektləri üçün kassa, e-kassa inteqrasiyası, anbar terminalı və rəhbər üçün mobil hesabatlar qururuq — bu müddətdə 100-dən çox obyekt işə salınıb.</p>
<p>Biz hazır proqram satmırıq və müştərini proqrama uyğunlaşmağa məcbur etmirik. Sizin mövcud 1C bazanızı və ya yeni qurulan bazanı işinizə uyğunlaşdırırıq: lazım olan hesabatı, sənədi, çap formasını yazır, kassanı fiskal cihaza, anbarı barkod terminalına, rəhbəri isə telefon tətbiqinə bağlayırıq.</p>
<h2>Nə edirik</h2>
<ul>
<li><b>Kassa və e-kassa</b> — 1C kassasının fiskal cihazla inteqrasiyası, offline növbə, X/Z hesabatları, termal çek çapı.</li>
<li><b>Anbar Terminal</b> — Android terminallarda barkodla mal qəbulu, sayım, köçürmə; məlumat dərhal 1C-yə düşür.</li>
<li><b>Mobil İzləmə BarkodPRO</b> — rəhbər üçün satış, qazanc, kassa, qalıq və borclar telefonda.</li>
<li><b>1C düzəlişləri və inteqrasiyalar</b> — hesabatlar, sənədlər, hüquqlar, HTTP servislər, bank, onlayn mağaza, Telegram bildirişləri.</li>
<li><b>Server və IT</b> — Windows Server, SQL Server, IIS, ehtiyat nüsxələr, uzaqdan iş masası.</li>
<li><b>Aylıq müşayiət</b> — yeniləmələr, monitorinq, 24/7 təcili dəstək.</li>
</ul>
<h2>Necə işləyirik</h2>
<p>Hər layihə tanışlıqla başlayır: necə işlədiyinizi və nəyin mane olduğunu öyrənirik. Sonra yazılı tapşırıq, müddət və qiymət razılaşdırılır — iş başlamazdan əvvəl. Bütün dəyişiklikləri əvvəlcə bazanın surətində edir və yoxlayırıq; işçi baza toxunulmaz qalır. Keçiddən sonra avadanlığı sazlayır, işçiləri öyrədir və sonrakı suallarda yanınızda qalırıq.</p>
<p>Başqasının yazdığı bazalarla da işləyirik: əvvəlcə bazanı yoxlayır, nə edildiyini sənədləşdirir, sonra müşayiətə götürürük. Sizin bazanız üçün yazılan düzəlişlər sizin bazanızda qalır.</p>
<h2>Kimlər üçün</h2>
<p>Marketlər, restoran və kafelər, apteklər, anbar və topdan satış şirkətləri, uşaq əyləncə mərkəzləri, kiçik istehsal və onlayn mağazalar. Bir kassalı mağazadan bir neçə filialı və mərkəzi anbarı olan şəbəkəyə qədər.</p>
<h2>Rekvizitlər</h2>
<ul>
<li>Ad: BarkodPRO</li>
<li>Ünvan: Şamaxı, Azərbaycan (xidmət bütün ölkə üzrə)</li>
<li>Telefon: <a href="tel:+994516782878">+994 51 678 28 78</a> — 24/7 texniki dəstək</li>
<li>WhatsApp: <a href="https://wa.me/994516782878">wa.me/994516782878</a> · Telegram: <a href="https://t.me/k1r1pt0n">@k1r1pt0n</a></li>
</ul>
<p class="upd">«1C» — 1C şirkətinin ticarət nişanıdır. BarkodPRO müstəqil tərtibatçıdır və 1C şirkətinin rəsmi nümayəndəsi deyil.</p>
''')

page('contact.html','Əlaqə','BarkodPRO ilə əlaqə: telefon +994 51 678 28 78 (24/7 texniki dəstək), WhatsApp, Telegram. Müraciətdə nə yazmaq lazımdır, nə vaxt cavab veririk.','ContactPage','Əlaqə','''
<h1>Əlaqə</h1>
<p>Yeni layihə, 1C-də düzəliş, inteqrasiya və ya təcili problem — ən tez yol WhatsApp və ya zəngdir. Yazılı müraciətlərə <b>1 iş günü ərzində</b> cavab veririk; kassa işləmirsə və ya satış dayanıbsa, <b>istənilən vaxt zəng edin</b>.</p>
<div class="ways">
<a class="way" href="tel:+994516782878"><b>051 678 28 78</b><span>Zəng — texniki dəstək 24/7</span></a>
<a class="way" href="https://wa.me/994516782878" target="_blank" rel="noopener"><b>WhatsApp</b><span>+994 51 678 28 78</span></a>
<a class="way" href="https://t.me/k1r1pt0n" target="_blank" rel="noopener"><b>Telegram</b><span>@k1r1pt0n</span></a>
</div>
<h2>Müraciətdə nə yazmaq lazımdır</h2>
<p>Qısa təsvir kifayətdir — dəqiqləşdirici sualları özümüz verəcəyik. Aşağıdakılar cavabı və qiyməti sürətləndirir:</p>
<ul>
<li>Biznesin növü: market, restoran, aptek, anbar və s.</li>
<li>Mağaza, anbar və kassa sayı; e-kassa cihazının modeli və provayderi.</li>
<li>Hansı 1C konfiqurasiyası (məsələn, Ticarətin idarə edilməsi, Pərakəndə) və ya yeni qurulmalıdır.</li>
<li>Nə dəyişməlidir: yeni hesabat, sənəd, inteqrasiya, terminal, mobil hesabatlar.</li>
<li>Müddət: nə vaxta qədər lazımdır.</li>
</ul>
<h2>İş saatları və ərazi</h2>
<p>Texniki dəstək 24/7 telefonla. Planlı işlər və görüşlər razılaşdırılmış vaxtda. Ofisimiz Şamaxıdadır; işin çoxunu uzaqdan görürük, avadanlıq qoşulması, təlim və server işləri üçün bütün Azərbaycan üzrə yerində gəlirik.</p>
<h2>Dillər</h2>
<p>Azərbaycan və rus dillərində ünsiyyət qururuq. 1C interfeysləri adətən Azərbaycan dilində hazırlanır.</p>
<p class="upd">Müraciət zamanı göndərdiyiniz məlumatlar yalnız cavab vermək üçün istifadə olunur — ətraflı: <a href="privacy.html">Məxfilik siyasəti</a>.</p>
''')

page('privacy.html','Məxfilik siyasəti','BarkodPRO saytı və proqramları hansı məlumatları emal edir: sayt cookie və analitika istifadə etmir, müraciətlər WhatsApp/Telegram vasitəsilə gəlir, 1C məlumatları müştərinin öz serverində qalır.','WebPage','Məxfilik siyasəti','''
<h1>Məxfilik siyasəti</h1>
<p>Bu səhifə BarkodPRO saytının (<b>xeyalshixi.github.io/barkodpro</b>), Mobil İzləmə BarkodPRO və Anbar Terminal proqramlarının, həmçinin müşayiət işlərinin hansı məlumatları emal etdiyini izah edir. Sualınız varsa: <a href="tel:+994516782878">+994 51 678 28 78</a>.</p>
<h2>Sayt</h2>
<ul>
<li><b>Cookie və analitika yoxdur.</b> Sayt izləmə kodu, reklam və ya analitika skripti istifadə etmir.</li>
<li><b>Brauzer yaddaşı:</b> yalnız seçdiyiniz gecə/gündüz rejimi brauzerinizdə (<code>localStorage</code>, açar <code>bp-theme</code>) saxlanılır və heç yerə göndərilmir.</li>
<li><b>Kalkulyatorlar</b> (maaş, ƏDV, qiymət, barkod və s.) tam brauzerdə işləyir — yazdığınız rəqəmlər serverə göndərilmir.</li>
<li><b>Müraciət forması</b> məlumatı serverə göndərmir: "WhatsApp ilə göndər" düyməsi yazdığınız mətnlə WhatsApp-ı açır, "Telegram ilə göndər" mətni buferə kopyalayır. Mesajı göndərib-göndərməmək sizin qərarınızdır; göndərilən mesaj həmin xidmətin qaydaları ilə emal olunur.</li>
<li><b>Hostinq və şriftlər:</b> sayt GitHub Pages-də yerləşir, şriftlər Google Fonts-dan yüklənir. Bu xidmətlər texniki səbəblərlə IP ünvanınızı və brauzer məlumatlarını qeyd edə bilər — onların öz məxfilik siyasətləri tətbiq olunur.</li>
</ul>
<h2>Müraciət və əlaqə məlumatları</h2>
<p>Bizə yazdığınız və ya zəng etdiyiniz zaman adınız, telefon nömrəniz, şirkətin adı və tapşırığın təsviri yalnız müraciətə cavab vermək, qiymət təklifi hazırlamaq və razılaşdırılmış işi görmək üçün istifadə olunur. Bu məlumatları üçüncü şəxslərə satmırıq və reklam üçün istifadə etmirik.</p>
<h2>Mobil İzləmə və Anbar Terminal</h2>
<ul>
<li>Proqramlar birbaşa <b>sizin öz 1C serverinizlə</b> əlaqə saxlayır. Satış, qalıq, borc və sənəd məlumatları telefon ilə sizin server arasında ötürülür — BarkodPRO-nun serverinə getmir.</li>
<li>Bağlantı ayarları (server ünvanı, 1C istifadəçi adı, şifrə, proqram açarı) yalnız cihazın öz yaddaşında saxlanılır. "Çıxış" düyməsi şifrəni silir.</li>
<li>Kamera yalnız barkod oxumaq üçün, siz skaner düyməsini basanda açılır; görüntü yadda saxlanılmır və göndərilmir.</li>
</ul>
<h2>Müşayiət və 1C bazalarına giriş</h2>
<p>Düzəliş və müşayiət zamanı bazanıza yalnız razılaşdırılmış iş üçün, sizin verdiyiniz giriş vasitəsilə qoşuluruq. İş bazanın surətində aparılır; bazadakı kommersiya və şəxsi məlumatlar məxfi saxlanılır, üçüncü şəxslərə verilmir və işdən kənar məqsədlə istifadə olunmur. İş bitdikdən sonra müvəqqəti surətlər silinir və ya sizə qaytarılır. Girişi istənilən vaxt ləğv edə bilərsiniz.</p>
<h2>Hüquqlarınız</h2>
<p>Bizdə saxlanılan əlaqə məlumatlarınız haqqında soruşa, onların düzəldilməsini və ya silinməsini tələb edə bilərsiniz — <a href="https://wa.me/994516782878">WhatsApp</a> və ya telefonla yazın.</p>
<p class="upd">Son yenilənmə: 22 noyabr 2026.</p>
''')
