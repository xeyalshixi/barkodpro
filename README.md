# BarkodPRO — sayt

BarkodPRO-nun rəsmi saytı: 1C:Enterprise, vergi kassası, POS, barkod, anbar terminalı və API inteqrasiyaları.

## Səhifələr

| Fayl | Nədir |
|---|---|
| `index.html` | Ana səhifə: sorğu konsolu, həllər, Mobil İzləmə tanıtımı, xidmətlər, 1C düzəliş və inteqrasiya (kod nümunələri), faydalı alətlər (maaş, ƏDV, qiymət/marja, endirim, barkod, tərəzi barkodu, kassa sayımı, mal dövriyyəsi), müşayiət paketləri, kalkulyator, FAQ, əlaqə. Tək fayl — CSS və JS içindədir |
| `mobil-izleme.html` | Mobil İzləmə BarkodPRO məhsul səhifəsi (canlı telefon demosu ilə). Tək fayl |
| `anbar-terminal.html` | Anbar Terminal (Android) məhsul səhifəsi |
| `login.html` | Müştəri girişi (demo rejimi — `dashboard.html`-ə keçir) |
| `dashboard.html` | POS / satış demo paneli (dəyişməyib) |
| `404.html` | Səhifə tapılmadı (GitHub Pages bunu avtomatik göstərir) |

## Qovluqlar

```
assets/css/site.css     bütün səhifələrin dizaynı (rənglər faylın əvvəlində :root-da)
assets/js/site.js       menyu, dil, filtr, sistem xəritəsi, sorğu forması, WhatsApp, şəkil böyütmə
assets/js/i18n.js       AZ və RU mətnlər
assets/img/             favicon, sosial şəbəkə şəkli (og-cover.png), Anbar Terminal ekranları
```

## Mətni dəyişmək

* Azərbaycanca mətn HTML-də yazılıb. Rusca qarşılığı `assets/js/i18n.js`-dədir.
* Bir mətni dəyişəndə həm HTML-də, həm `i18n.js`-də `az` və `ru` hissəsində eyni açarı (`data-i18n="..."`) düzəldin.

## Əlaqə məlumatları

* WhatsApp nömrəsi: `assets/js/site.js` (`WA`) və HTML-dəki `wa.me/994516782878` linkləri.
* Telegram: `t.me/k1r1pt0n` (index.html, anbar-terminal.html).
