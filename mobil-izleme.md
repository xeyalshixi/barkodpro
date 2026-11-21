# Mobil İzləmə BarkodPRO — 1C hesabatları rəhbərin telefonunda

Mobil İzləmə BarkodPRO rəhbər və sahibkar üçündür: bu günün satışı, qazanc, kassalar, anbar qalığı, borclar və bütün sənədlər — ofisə gəlmədən. Rəqəmlər sizin 1C bazanızdan canlı gəlir, ara cədvəl yoxdur.

- Platforma: Android tətbiqi, iPhone və istənilən brauzer
- Bağlantı: 1C HTTP servisi (`/BarkodPRODatabase/hs/api1`)
- HTML versiya: <https://xeyalshixi.github.io/barkodpro/mobil-izleme.html>
- Demo və qiymət: [WhatsApp](https://wa.me/994516782878) · [051 678 28 78](tel:+994516782878)

## Ana ekran

- Bu günün satışı (nağd və nağdsız), qazanc və marja, çek sayı — əvvəlki dövrlə ▲▼ müqayisə.
- Günlük universal hesabat: ilkin qalıq, mədaxil, müştəridən qaytarma, anbarlararası yerdəyişmə, satış (məbləğ, endirim, mənfəət), tədarükçüyə qaytarma, silinmə, digər hərəkətlər, son qalıq — maya və satış qiyməti ilə; kassalar üzrə satış.

## 24 bölmə, 5 qrup

- **Sənədlər (6):** mal alışı, mal satışı, çeklər, qaytarmalar, tədarükçüyə qaytarma, anbar sənədləri (mədaxil, silinmə, yerdəyişmə, inventarizasiya).
- **Kassa (5):** kassa mədaxil (ПКО), kassa məxaric (РКО), sair xərclər, sair mədaxil, pul köçürməsi.
- **Nəzarət (2):** registrasiya olunmamış sənədlər, kassada silinən sətirlər.
- **Hesabatlar (10):** ümumi hesabat, günlük universal, satış (top mallar, qrafik), kassa və bank, malların hərəkəti, qalıq (skaner), qalıq (firma), kontragent borcları, müştəri borcları, xərclər.
- **Siyahı (1):** malların siyahısı (qruplar, qiymət, qalıq).

## Telefondan iş

- Kassa sənədləri yaratmaq: kassa mədaxil və məxaric, sair xərc, sair mədaxil, kassadan kassaya köçürmə; kontragent seçiləndə borcu görünür.
- Keçirilməmiş sənədləri toplu registrasiya etmək.
- Sənədə düzəliş: başlıq sahələri və cədvəl hissəsi (mal, miqdar, qiymət).
- Mal kartında alış və satış qiymətini dəyişmək (ayrıca icazə ilə).
- Kamera ilə barkod: EAN-13, EAN-8, UPC, Code128, Code39, ITF, QR, tərəzi barkodu.
- Çox mağaza rejimi: filialları siyahıdan seçib keçmək, hər filialın öz serveri ola bilər.

## Təhlükəsizlik

- Hər istifadəçi öz 1C hesabı ilə girir — hüquqlar 1C-dəki kimidir.
- Proqram imzası: hər sorğu vaxt damğası və SHA-256 imza ilə göndərilir; açar uyğun deyilsə server cavab vermir.
- Ayarlar şifrə ilə qorunur; bölmələr və hesabat sətirləri ayrıca açılıb-bağlanır.
- "Məbləğləri gizlət" rejimi; qiymət dəyişmə icazəsi defolt bağlıdır.

## Necə qoşulur

1. 1C bazasına `api1` HTTP servisi əlavə olunur (mövcud sənəd və hesabatlara toxunulmur).
2. Servis IIS və ya Apache ilə yayımlanır.
3. Ofisdən kənar giriş üçün statik IP, VPN və ya port yönləndirmə.
4. Telefonda tətbiq quraşdırılır və ya brauzerdə açılır; istifadəçi, şifrə və proqram açarı yazılır.

Adətən bir iş günü çəkir. Hər şey əvvəlcə bazanın surətində yoxlanılır.

## Suallar

- **Hansı 1C konfiqurasiyaları?** Ticarətin idarə edilməsi (УТ), Pərakəndə, BarkodPRO kassa və fərdi bazalar.
- **İnternet olmayanda?** Proqram bağlantının olmadığını göstərir; telefondan yaradılan sənəd yalnız server təsdiq edəndə yazılır.
- **Neçə istifadəçi?** Məhdudiyyət yoxdur; hər kəsə yalnız lazım olan bölmələr açılır.
- **Yeni hesabat əlavə etmək olar?** Olar — 1C tərəfində yazılıb proqrama ayrıca bölmə kimi əlavə olunur.

[BarkodPRO ana səhifəsi](https://xeyalshixi.github.io/barkodpro/index.md) · [llms.txt](https://xeyalshixi.github.io/barkodpro/llms.txt)
