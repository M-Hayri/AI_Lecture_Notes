"""
BAYES AĞLARI
Bayes Ağlarının en büyük gücü, karmaşık bir ortak dağılımı, birbirini etkileyen daha küçük ve anlamlı parçalara ayırarak ifade etmesidir.
Bu sayede sistem, elindeki sınırlı bilgiyi (kanıtı) kullanarak bilmediği bir değişken (sorgu) hakkında Olasılıksal Çıkarım (Inference) yapabilir

Bu algoritmada bir trenin gecikme veya zamanında gelme olasılığını yağmur durumu ve bakım durumuna göre hesaplamaya çalışıyoruz.

Trenin gecikme/gecikmeme durumu -----> Yağmur ve bakım durumuna bağlı
Bakım durumu -----> Yağmur şiddetine bağlı
Yağmur siddeti -----> Kök düğüm

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
SORU: P(yağmur: hafif | bakım: yok | tren: gecikmeli) senaryosunun olma olasılığı
"""
# --- SORU ÇÖZÜMÜ (Doldurulması Gereken Kısım) ---

# P(yağmur: hafif)
hafif_yagmur = yagmur_siddeti['hafif']

# P(bakım: yok | yağmur: hafif) -> [doldur]
bakim_yok = bakim_durumu['hafif']['yok']

# P(tren: gecikmeli | yağmur: hafif, bakım: yok) -> [doldur]
tren_gecikmeli = tren_gecikme_durumu[('hafif', 'yok')]['gecikmeli']

# Ortak Olasılık Hesabı
olasilik = hafif_yagmur * bakim_yok * tren_gecikmeli

print(f"Senaryonun gerçekleşme olasılığı: {olasilik:.3f}")
