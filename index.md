# BarkodPRO — barkoddan fiskal çekə qədər, hər şey 1C-də

BarkodPRO — 1C:Enterprise əsasında kassa, e-kassa inteqrasiyası, anbar terminalı, rəhbər üçün mobil hesabatlar və texniki müşayiət. Market, restoran, aptek və anbarlar üçün. Şamaxı, Azərbaycan — uzaqdan bütün ölkə üzrə.

- Telefon / 24/7 texniki dəstək: [051 678 28 78](tel:+994516782878)
- WhatsApp: <https://wa.me/994516782878>
- Telegram: <https://t.me/k1r1pt0n>
- HTML versiya: <https://xeyalshixi.github.io/barkodpro/>
- Agentlər üçün: [llms.txt](https://xeyalshixi.github.io/barkodpro/llms.txt) · [sitemap.xml](https://xeyalshixi.github.io/barkodpro/sitemap.xml)

5+ il təcrübə · 100+ tamamlanmış obyekt · 24/7 texniki dəstək

## Hazır həllər

Hər modul 1C-yə birbaşa bağlıdır: məlumat bir dəfə daxil olur, hər yerdə görünür.

- **Web Kassa** — internet kəsiləndə də satışı dayandırmayan kassa: offline növbə, növbə hesabatı, termal çek çapı.
- **E-kassa inteqrasiyası** — 1C-dən fiskal cihaza birbaşa çek: satış, qaytarma, X/Z hesabatları. Bir neçə provayderlə işləyirik.
- **[Anbar Terminalı](https://xeyalshixi.github.io/barkodpro/anbar-terminal.html)** — Zebra TC20 kimi Android terminallarda barkodla qəbul, sayım, köçürmə. Məlumat dərhal 1C-yə düşür.
- **[Mobil İzləmə BarkodPRO](https://xeyalshixi.github.io/barkodpro/mobil-izleme.html)** — rəhbər üçün telefonda satış, qazanc, kassa, qalıq və borclar; telefondan kassa sənədi, registrasiya, qiymət dəyişmə.
- **Restoran və ofisiant sifarişi** — ofisiant telefondan masaya sifariş açır, sifariş 1C restoran modulunda və mətbəxdə görünür.
- **Onlayn sifariş forması** — müştəri link ilə sifariş verir, sifariş birbaşa 1C-də sənəd kimi yaranır.
- **Uşaq əyləncə mərkəzi** — kartla giriş, tarif və uşaq sayı, canlı geri sayım siyahısı, çıxışda avtomatik çek.
- **Onlayn mağaza inteqrasiyası** — Shopify və digər platformalarla qalıq, qiymət və sifariş sinxronizasiyası.

Sahələr: marketlər, restoran və kafelər, apteklər, anbar və topdan satış, əyləncə mərkəzləri, istehsal, onlayn mağazalar.

## Nə edirik

Kiçik düzəlişdən tam avtomatlaşdırmaya qədər — işi əvvəlcə bazanın surətində edir, sonra işçi bazaya keçiririk.

- **Sıfırdan 1C qurulması** — konfiqurasiyanın seçilməsi, qalıqların köçürülməsi, kassaların və printerlərin qoşulması.
- **1C-də düzəlişlər** — yeni hesabatlar, çap formaları, sənədlər, hüquqların ayrılması — sizin iş prosesinizə görə.
- **İnteqrasiyalar** — e-kassa, bank, onlayn mağaza, terminallar, Telegram bildirişləri, HTTP servislər.
- **Barkod və avadanlıq** — skaner, etiket printeri, çek printeri, tərəzi, terminal — seçirik, qoşuruq, sazlayırıq.
- **Server və IT** — Windows Server, SQL Server, IIS, uzaqdan iş masası, avtomatik ehtiyat nüsxələr.
- **Kassir və operator təlimi** — yeni sistemə keçiddə işçilərə yerində və ya uzaqdan qısa, praktik təlim.

## 1C-də istənilən düzəliş və inteqrasiya

Hazır konfiqurasiya işinizə tam uyğun gəlmirsə, 1C-ni sizə uyğunlaşdırırıq. Kodu özümüz yazırıq, əvvəlcə bazanın surətində yoxlayırıq.

- Hesabat və çap formaları (qaimə, etiket, akt, kassir hesabatı)
- Sənəd və emal — sizin iş prosesinizə görə
- E-kassa: satış, qaytarma, X/Z, növbə
- HTTP servis / API: mobil, sayt, terminal, Shopify
- Bank və ödəniş: çıxarış, POS terminal
- Telegram bildirişləri: Z-hesabat, minimum qalıq
- Hüquqlar və ayrım: mağaza, kassa, istifadəçi
- Tərəzi və skaner: barkod formatları, PLU

Nümunə — 1C HTTP servisi (Mobil İzləmə üçün):

```bsl
// HTTP servis api1: /hs/api1/menu?action=esas
Функция MenuGET(Запрос)
  Действие = Запрос.ПараметрыЗапроса.Получить("action");
  Если Не ImzaDuzgundur(Запрос) Тогда
    Возврат JSONОтвет(Новый Структура("error", "İmza yanlışdır"), 403);
  КонецЕсли;
  Если Действие = "esas" Тогда
    Возврат JSONОтвет(GununXulasesi(НачалоДня(ТекущаяДата())), 200);
  КонецЕсли;
  Возврат JSONОтвет(Новый Структура("error", "Naməlum əmr"), 400);
КонецФункции
```

## Faydalı alətlər — pulsuz

Brauzerdə işləyir, heç bir məlumat göndərilmir:

- [Maaş](https://xeyalshixi.github.io/barkodpro/#maas) — hesablanan ↔ əlinə çatan, 2026 qaydaları (qeyri-neft-qaz, özəl sektor)
- [ƏDV](https://xeyalshixi.github.io/barkodpro/#edv) — daxil və ya üstünə
- [Qiymət və marja](https://xeyalshixi.github.io/barkodpro/#qiymet) — əlavə % və marja %
- [Endirim və aksiya](https://xeyalshixi.github.io/barkodpro/#endirim) — faiz və ya "X al — Y pulsuz"
- [Barkod generatoru](https://xeyalshixi.github.io/barkodpro/#barkod) — EAN-13, yoxlama rəqəmi, SVG
- [Tərəzi barkodu](https://xeyalshixi.github.io/barkodpro/#terezi) — çəki və məbləğ formatları
- [Kassa sayımı](https://xeyalshixi.github.io/barkodpro/#kassa) — əskinas və xırda pul, 1C ilə fərq
- [Mal dövriyyəsi](https://xeyalshixi.github.io/barkodpro/#dovr) — dövriyyə günü, minimum ehtiyat

## Aylıq müşayiət paketləri

| Paket | Qiymət | Ayda saat | Təcili reaksiya |
|---|---|---|---|
| Start | 150 AZN / ay | 6 saat | 2 saat, iş günləri 9:00–19:00 |
| Biznes | 350 AZN / ay | 14 saat | 30 dəqiqə, şəxsi məsul mütəxəssis |
| Korporativ | 750 AZN / ay | 30+ saat | 15 dəqiqə, 24/7, yerində gəliş |

Bütün paketlərdə: yeniləmələr surətdə yoxlanılır, ehtiyat nüsxələr bərpa üçün test edilir, görülən işlər üzrə hesabat verilir. İstifadə olunmamış saatlar növbəti aya keçir. Bir dəfəlik iş: 25 AZN / saat.

## Layihə necə gedir

1. **Tanışlıq** — zəng və ya görüş: necə işləyirsiniz, nə mane olur.
2. **Qiymət və plan** — yazılı tapşırıq, müddət və qiymət — işə başlamazdan əvvəl.
3. **Surətdə işləmə** — hər şeyi bazanın surətində edirik, işçi baza toxunulmaz qalır.
4. **İşə salma** — keçid, avadanlığın sazlanması və işçilərin təlimi.
5. **Müşayiət** — sonrakı suallar, yeniləmələr və yeni istəklər.

## Tez-tez verilən suallar

- **Uzaqdan işləyirsiniz, yoxsa gəlirsiniz?** Əksər işi uzaqdan görürük. Avadanlıq qoşulması, təlim və ya server işləri üçün yerində gəlirik.
- **Başqasının yazdığı 1C bazası ilə işləyirsiniz?** Bəli. Əvvəlcə bazanı yoxlayırıq, nə edildiyini sənədləşdiririk, sonra müşayiətə götürürük.
- **Hansı e-kassa provayderləri ilə işləyirsiniz?** Bazarda istifadə olunan bir neçə provayderlə inteqrasiyamız var. Cihazınızın adını yazın — uyğunluğu dəqiqləşdirək.
- **Müşayiət olmadan bir dəfəlik iş sifariş etmək olar?** Olar. Saatlıq qiymətlə edirik.
- **Yazılan kod kimə məxsusdur?** Sizin bazanız üçün yazılan düzəlişlər sizin bazanızda qalır. Lisenziyalı modullarımızın şərtləri ayrıca razılaşdırılır.
- **İnternet kəsiləndə kassa işləyir?** Web Kassa offline rejimdə satışı davam etdirir, əlaqə bərpa olunanda çeklər avtomatik 1C-yə göndərilir.

## Əlaqə

Tapşırığı yazın — 1 iş günü ərzində cavab veririk. WhatsApp və Telegram-da daha tez cavab alırsınız.

- Telefon: +994 51 678 28 78
- WhatsApp: <https://wa.me/994516782878>
- Telegram: <https://t.me/k1r1pt0n>
- [Haqqımızda](https://xeyalshixi.github.io/barkodpro/about.html) · [Əlaqə](https://xeyalshixi.github.io/barkodpro/contact.html) · [Məxfilik](https://xeyalshixi.github.io/barkodpro/privacy.html)

«1C» — 1C şirkətinin ticarət nişanıdır. BarkodPRO müstəqil tərtibatçıdır.
