from enum import Enum
"""
Bu bölümde Knowledge Engineering sistematiğini kavramaya çalışıyoruz. 

KNOWLEDGE ENGİNEERİNG: Bir problemi mantik ile çözebilmek için önce uygun semboller ve cümleler seçilmelidir. Bu sürece 
knowledge engireering denir.

Bir Problemi çözmek için şu sorular sorulur:
    * Hangi temel bilgileri sembollerle göstermeliyim?
    * Doğru kabul ettiğim kurallar nelerdir?
    * Hangi sonucu sorgulamak istiyorum?

Bu sorular cevaplandıktan sonra aşama aşama bir problem mantık ile çözülebilir

AŞAĞIDAKI ALGORİTMA'NIN AMACI

Aşağıda yazdığımız sistem, 5 tane hastalığı ve bu hastelıkların etkilerine göre sınıflandırmak için bir knowledge engineering 
kullanır.
1. Hastalık teşhisi sırasında her bir belirtecin etkisi classlar ile sınıflandırılmıştır. 
2. Her bir hastalığın belirteçlerinin derecesine göre durumları "hastalik_kurallari" isimli listede yer almaktadır.
3. Teşhis koyma aşamasına gelince her bir veri sırasıyla alınır. Alınan sonuçlar hastalık ve belirteçlerine göre incelenir.
    Sonucunda ise en yakın sonuc verdiği hastalık türü kişide var olarak kabul edilir.
    
Burada temel bilgiler class formuna çevrildi. Temel bilgilerin doğru kabul ettiği sonuclar "hastalik_kurallari" isimli listede
tanımlandı. Ve test aşamasında 3 tane hastanın verileri sorgulandı.
"""

""" author: Muhammed Hayri ÖZCAN"""

# --- 1. TEŞHİSLERİN SINIFLANDIRILMASI ---
class Ates(Enum):
    YOK = 0
    DUSUK = 1 # 37.5 - 38.5
    YUKSEK = 2 # > 38.5

class Oksuruk(Enum):
    YOK = 0
    KURU = 1
    BALGAMLI = 2
    SIDDETLI = 3

class BurunAkintisi(Enum):
    YOK = 0
    SEFFAF = 1
    KOYU = 2 # Sarı-Yeşil

class BasAgrisi(Enum):
    YOK = 0
    HAFIF = 1
    SIDDETLI = 2

class BogazAgrisi(Enum):
    YOK = 0
    HAFIF = 1
    SIDDETLI_KIZARIK = 2

class NefesDarligi(Enum):
    YOK = 0
    VAR = 1
    KRITIK = 2

class VucutAgrisi(Enum):
    YOK = 0
    HAFIF = 1
    YAYGIN_AGRI = 2

class KulakDurumu(Enum):
    NORMAL = 0
    AGRILI = 1
    AKINTILI = 2


# --- 2.Bilgi Tabanı (Knowledge Base) ---
hastalik_kurallari = [
    {
        "hastalik": "Grip (İnfluenza)",
        "kosullar": {
            "ates": Ates.YUKSEK,
            "oksuruk": Oksuruk.KURU,
            "bas_agrisi": BasAgrisi.SIDDETLI,
            "vucut_agrisi": VucutAgrisi.YAYGIN_AGRI
        }
    },
    {
        "hastalik": "Soğuk Algınlığı (Nezle)",
        "kosullar": {
            "ates": Ates.DUSUK,
            "burun_akintisi": BurunAkintisi.SEFFAF,
            "bas_agrisi": BasAgrisi.HAFIF,
            "vucut_agrisi": VucutAgrisi.HAFIF
        }
    },
    {
        "hastalik": "Farenjit",
        "kosullar": {
            "bogaz_agrisi": BogazAgrisi.SIDDETLI_KIZARIK,
            "ates": Ates.DUSUK,
            "oksuruk": Oksuruk.KURU
        }
    },
    {
        "hastalik": "Sinüzit",
        "kosullar": {
            "burun_akintisi": BurunAkintisi.KOYU,
            "bas_agrisi": BasAgrisi.SIDDETLI,
            "ates": Ates.DUSUK
        }
    },
    {
        "hastalik": "Bronşit",
        "kosullar": {
            "oksuruk": Oksuruk.BALGAMLI,
            "nefes_darligi": NefesDarligi.VAR,
            "ates": Ates.DUSUK
        }
    },
    {
        "hastalik": "Zatürre (Pnömoni)",
        "kosullar": {
            "ates": Ates.YUKSEK,
            "oksuruk": Oksuruk.SIDDETLI,
            "nefes_darligi": NefesDarligi.KRITIK,
            "vucut_agrisi": VucutAgrisi.YAYGIN_AGRI
        }
    },
    {
        "hastalik": "Orta Kulak İltihabı",
        "kosullar": {
            "kulak_durumu": KulakDurumu.AGRILI,
            "ates": Ates.YUKSEK,
            "bas_agrisi": BasAgrisi.HAFIF
        }
    }
]


# --- 3. ÇIKARIM MOTORU (Inference Engine) ---
def teshis_koy(hasta_verisi):
    olasi_hastaliklar = []

    for kural in hastalik_kurallari:
        eslesme = True
        # Kuraldaki her bir koşulun hasta verisinde olup olmadığını kontrol et
        for semptom, deger in kural["kosullar"].items():
            if hasta_verisi.get(semptom) != deger:
                eslesme = False
                break

        if eslesme:
            olasi_hastaliklar.append(kural['hastalik'])

    if not olasi_hastaliklar:
        return "⚠️ Sonuç: Belirtilerle tam eşleşen bir hastalık bulunamadı."

    return f"✅ Teşhis Edilen Olasılıklar: {', '.join(olasi_hastaliklar)}"

# --- 4. TEST SENARYOLARI ---
test_hastalari = [
    {
        "isim": "Hasta A (Grip Şüphesi)",
        "veriler": {"ates": Ates.YUKSEK, "oksuruk": Oksuruk.KURU, "bas_agrisi": BasAgrisi.SIDDETLI, "vucut_agrisi": VucutAgrisi.YAYGIN_AGRI}
    },
    {
        "isim": "Hasta B (Sinüzit Şüphesi)",
        "veriler": {"burun_akintisi": BurunAkintisi.KOYU, "bas_agrisi": BasAgrisi.SIDDETLI}
    },
    {
        "isim": "Hasta C (Kritik Durum)",
        "veriler": {"ates": Ates.YUKSEK, "oksuruk": Oksuruk.SIDDETLI, "nefes_darligi": NefesDarligi.KRITIK}
    }
]

for hasta in test_hastalari:
    print(f"--- {hasta['isim']} ---")
    print(teshis_koy(hasta['veriler']))
    print()



