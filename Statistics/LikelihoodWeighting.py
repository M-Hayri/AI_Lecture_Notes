import random

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


# Likelihood Weighting Mantığı
def likelihood_weighting(n_samples=1000):
    total_weight_delayed = 0
    total_weight_all = 0

    for _ in range(n_samples):
        w = 1.0

        # 1. Yağmur (Kanıt: heavy)
        # Zar atmıyoruz, ağırlığı güncelliyoruz
        w *= yagmur_siddeti['şiddetli']  # w = 0.1
        r_val = 'şiddetli'

        # 2. Bakım (Kanıt: yok)
        # Zar atmıyoruz, ağırlığı güncelliyoruz
        w *= bakim_durumu[r_val]['yok']  # w = 0.1 * 0.9 = 0.09
        m_val = 'yok'

        # 3. Tren (Kanıt değil, ZAR AT)
        t_probs = tren_gecikme_durumu[(r_val, m_val)]
        t_val = random.choices(list(t_probs.keys()), weights=list(t_probs.values()))[0]

        # Sonuçları ağırlığa göre topla
        if t_val == 'gecikmeli':
            total_weight_delayed += w
        total_weight_all += w

    return total_weight_delayed / total_weight_all

print(likelihood_weighting(1000))