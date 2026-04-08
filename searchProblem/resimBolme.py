"""
Bu kodun amacı, imgs klasörüne yüklenmiş olan görseli 9 eşit parcaya ayırmaktır. Bu parçalar, yapbozun parçaları
olarak kullanılacaktır.

author : Muhammed Hayri ÖZCAN
date: 04.07.2026

"""

from PIL import Image
import os

"""
goruntu = görüntü yolu yazılır
x = x ekseninde kaç parçaya bölüneceği yazılır
y = y ekseninde kaç parçaya bölüneceği yazılır
cikis_klasoru = görüntülerin hangi klasöre kaydedileceğini gösterir.
"""
"""
def goruntuBolme(goruntu_yolu, x, y, cikis_klasoru):
    # Çıkış klasörü yoksa oluştur
    if not os.path.exists(cikis_klasoru):
        os.makedirs(cikis_klasoru)

    # Görüntüyü aç
    img = Image.open(goruntu_yolu)
    genislik, yukseklik = img.size

    parca_genislik = genislik // x
    parca_yukseklik = yukseklik // y

    sayac = 1
    for i in range(3):  # Satırlar (Y ekseni)
        for j in range(3):  # Sütunlar (X ekseni)

            # Kesilecek alanın koordinatlarını belirle (sol, üst, sağ, alt)
            sol = j * parca_genislik
            ust = i * parca_yukseklik
            sag = (j + 1) * parca_genislik
            alt = (i + 1) * parca_yukseklik

            # Görüntüyü kırp
            parca = img.crop((sol, ust, sag, alt))

            # Parçayı kaydet
            parca.save(f"{cikis_klasoru}/parca_{sayac}.png")
            print(f"Parça {sayac} kaydedildi: {sol}, {ust}, {sag}, {alt}")
            sayac += 1

yol = 'imgs/fatih-portre.jpg'
cikisYolu = 'imgs'

goruntuBolme(yol, 3, 3, cikisYolu)
"""

import cv2
import numpy as np
import os

# Klasör yoksa oluştur
if not os.path.exists('imgs'):
    os.makedirs('imgs')

# 216x216 boyutunda siyah görüntü (Pikseller: 0)
black_image = np.zeros((216, 216, 3), dtype="uint8")

# Görüntüyü kaydet
cv2.imwrite('imgs/siyah_resim.png', black_image)
print("Siyah resim başarıyla oluşturuldu!")
