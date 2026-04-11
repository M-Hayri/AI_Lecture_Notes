"""
Bayes ağlarında bazen olasılıkları elle veya formülle hesaplamak (tam çıkarım) çok karmaşık hale gelebilir.
İşte burada Rejection Sampling (Reddederek Örnekleme) devreye girer. Bu yöntem, bir matematikçiden ziyade bir
gözlemci gibi davranarak sonucu tahmin etmektir.

Diyelim ki elimizde bu sistemin kuralları (olasılık tabloları) var ama formülleri bilmiyoruz. Şunu yaparız:
"Hadi 1000 gün boyunca bu dünyayı simüle edelim.

"Örnekleme (Sampling): Her gün için önce yağmurun yağıp yağmayacağına (zar atarak) karar verirsin. Sonra o
yağmur durumuna göre bakımın olup olmayacağına karar verirsin. En son trenin durumuna bakarsın.

Kanıt (Evidence): Diyelim ki biz şunu merak ediyoruz: "Yağmurun hafif olduğunu bildiğimizde (R = light),
trenin gecikme olasılığı nedir?"Bu soruda "Yağmurun hafif olması" bizim kanıtımızdır.

2. "Reddetme" (Rejection) Kısmı Neresi?Simülasyonu başlattın ve 1000 tane örnek gün oluşturdun.
    1. Gün: Yağmur yok, Bakım var, Tren zamanında. (Bu günü ÇÖPE AT, çünkü yağmur hafif değil.)
    2. Gün: Yağmur hafif, Bakım yok, Tren gecikmeli. (TUT, çünkü yağmur hafif.)
    3. Gün: Yağmur şiddetli, Bakım yok, Tren gecikmeli. (ÇÖPE AT, çünkü yağmur hafif değil.)

İşte bu yüzden adı Rejection Sampling'dir. Kanıtımıza (Yağmurun hafif olması) uymayan her senaryoyu sistemden dışlarız.
"""

# Yağmurun şiddet sınıflandırması ve olasılıkları
yagmur_siddeti = {'yagmur_yok': 0.7,
                  'hafif': 0.2,
                  'şiddetli': 0.1}

# Bakım çalışmalarının yağmurun yağma durumuna göre olma olasılığı
bakim_durumu = {
    'yagmur_yok': {'var': 0.4, 'yok': 0.6},
    'hafif': {'var': 0.2, 'yok': 0.8},
    'şiddetli': {'var': 0.1, 'yok': 0.9}
}

# Trenin zamanında gelme veya gecikme olasılığının yağmur ve bakıma göre sınıflandırılması
tren_gecikme_durumu = {
    ('yagmur_yok', 'var'): {'zamaninda': 0.8, 'gecikmeli': 0.2},
    ('yagmur_yok', 'yok'): {'zamaninda': 0.9, 'gecikmeli': 0.1},
    ('hafif', 'var'):      {'zamaninda': 0.6, 'gecikmeli': 0.4},
    ('hafif', 'yok'):      {'zamaninda': 0.7, 'gecikmeli': 0.3},
    ('şiddetli', 'var'):   {'zamaninda': 0.4, 'gecikmeli': 0.6},
    ('şiddetli', 'yok'):   {'zamaninda': 0.5, 'gecikmeli': 0.5},
}


"""
1. Olasılık durumlarının farklı kombinasyonlarını üret
2. Kanıta uygun olmayan kombinasyonlardan şartları sağlamayanları ele
3. Kalan kombinasyonlardan olasılık hesapla
"""

import random


# --- VERİ SETİ (Sözlüklerin aynı kaldığını varsayıyoruz) ---
# ... (yagmur_siddeti, bakim_durumu, tren_gecikme_durumu yukarıdaki gibi) ...

def simulation(n_samples=10000):
    samples = []

    for _ in range(n_samples):
        # 1. ADIM: Yağmur Durumunu Örnekle (Kök Düğüm)
        r_keys = list(yagmur_siddeti.keys())
        r_probs = list(yagmur_siddeti.values())
        r_draw = random.choices(r_keys, weights=r_probs)[0]

        # 2. ADIM: Bakım Durumunu Örnekle (Yağmura Bağlı)
        m_options = bakim_durumu[r_draw]
        m_keys = list(m_options.keys())
        m_probs = list(m_options.values())
        m_draw = random.choices(m_keys, weights=m_probs)[0]

        # 3. ADIM: Tren Durumunu Örnekle (Yağmur ve Bakıma Bağlı)
        t_options = tren_gecikme_durumu[(r_draw, m_draw)]
        t_keys = list(t_options.keys())
        t_probs = list(t_options.values())
        t_draw = random.choices(t_keys, weights=t_probs)[0]

        # Kombinasyonu kaydet
        samples.append({'rain': r_draw, 'maintenance': m_draw, 'train': t_draw})

    return samples


# --- REJECTION SAMPLING UYGULAMASI ---

# Soru: P(train: gecikmeli | rain: hafif)
kanit = 'hafif'
n_iter = 100000  # Daha doğru sonuç için örnek sayısını artırdık
tum_ornekler = simulation(n_iter)

# 1. Filtreleme (Reddetme): Sadece yağmurun 'hafif' olduğu günleri tut
hafif_yagmurlu_gunler = [s for s in tum_ornekler if s['rain'] == kanit]

# 2. Sayma: Bu günlerin kaçında tren gecikti?
gecikmeli_ve_hafif = [s for s in hafif_yagmurlu_gunler if s['train'] == 'gecikmeli']

# 3. Olasılık Hesabı
toplam_uygun_gun = len(hafif_yagmurlu_gunler)
gecikme_sayisi = len(gecikmeli_ve_hafif)

if toplam_uygun_gun > 0:
    olasilik = gecikme_sayisi / toplam_uygun_gun
    print(f"Simülasyon Toplam Gün: {n_iter}")
    print(f"Kanıta Uyan Gün Sayısı (Hafif Yağmur): {toplam_uygun_gun}")
    print(f"Gecikme Yaşanan Gün Sayısı: {gecikme_sayisi}")
    print(f"Tahmini Olasılık: {olasilik:.4f}")
else:
    print("Kanıta uyan hiçbir örnek bulunamadı, örnek sayısını artırın.")
