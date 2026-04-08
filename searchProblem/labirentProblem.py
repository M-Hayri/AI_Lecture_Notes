"""
Burada amaç, labirent problemlerini simüle etmek ve DFS ve BFS algoritmalarını kavramaktır.
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import threading
from collections import deque

# LABİRENTİN TASARLANMASI
# Labirent Matrisi (Görüntüden tek tek sayılmıştır)
# 0: Yol, 1: Duvar, 2: Start (A), 3: End (B)
labirent_matrisi = np.array([
    [0, 1, 0, 1, 3, 1, 1, 1, 0, 0, 1, 0], # Satır 0 (En Üst)
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0], # Satır 1
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0], # Satır 2
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0], # Satır 3
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], # Satır 4
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], # Satır 5
    [2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]  # Satır 6 (En Alt)
])


def labirenti_goster(matris):
    plt.figure(figsize=(10, 6))

    # Renk haritası oluştur: 0=Sarı, 1=Gri, 2=Kırmızı, 3=Yeşil
    renkler = ['#FFD700', '#333333', '#FF0000', '#008000']
    cmap = ListedColormap(renkler)

    plt.imshow(matris, cmap=cmap)

    # Harfleri ekle (A ve B)
    for y in range(matris.shape[0]):
        for x in range(matris.shape[1]):
            if matris[y, x] == 2:
                plt.text(x, y, 'A', ha='center', va='center', color='white', fontweight='bold')
            elif matris[y, x] == 3:
                plt.text(x, y, 'B', ha='center', va='center', color='white', fontweight='bold')

    # Izgara çizgilerini belirginleştir
    plt.xticks(np.arange(-.5, 12, 1), [])
    plt.yticks(np.arange(-.5, 7, 1), [])
    plt.grid(color='black', linestyle='-', linewidth=2)

    plt.title("Görüntüden Aktarılan Labirent Matrisi")
    plt.show()

# LABİRENT TASARLANDIKTAN SONRA ADIM ADIM BSF VE DSF İÇİN FONKSIYON YAZIMINA GEÇİYORUZ

def DFS_Algoritmasi(matris, baslangic, hedef):
    """
    ---DEPT FOR SEARCH (DFS) ALGORİTMASI---
    Bir yol seçer ve o yol üzerinde mümkün olduğunca derine gider. Yol çıkmaza giderse geri dönerek başka yolu dener.

    DFS Özellikleri
        -- Basit ve Anlaşılması kolaydır
        -- Çoğu zaman bellek kullanımı düşüktür.
        -- Her zaman en kısa yolu bulmaz
        -- Yahlış bir yola saparsa uzun süre o tarafta kalabilir
    """

    satir_sayisi, sutun_sayisi = matris.shape
    stack = [(baslangic, [baslangic])]
    ziyaret_edilenler = set()
    adim = 0

    while stack:
        (r, c), su_anki_yol = stack.pop()
        if (r, c) == hedef:
            yield (ziyaret_edilenler, su_anki_yol, adim, True)
            return
        if (r, c) not in ziyaret_edilenler:
            ziyaret_edilenler.add((r, c))
            adim += 1
            # Mevcut durumu dışarıya gönder (yield)
            yield (ziyaret_edilenler, su_anki_yol, adim, False)

            for dr, dc in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < satir_sayisi and 0 <= nc < sutun_sayisi:
                    if matris[nr, nc] != 1 and (nr, nc) not in ziyaret_edilenler:
                        stack.append(((nr, nc), su_anki_yol + [(nr, nc)]))


def BFS_Algoritmasi(matris, baslangic, hedef):
    """
    ---BREADTH FOR SEARCH ALGORİTMASI---
    Başlangıca en yakın düğümleri önce inceler. Sonra bir alt seviyeye geçer. Bu nedenle katman katman ilerleyen bir
    yöntemdir.

    BFS Özellikleri
    -- Birim maliyetli problemlerde en kısa yoldur.
    -- Sistemli ilerler
    -- çok sayıda düğüm saklandığı için bellek kullanımı artabilir.
    """
    satir_sayisi, sutun_sayisi = matris.shape
    queue = deque([(baslangic, [baslangic])])
    ziyaret_edilenler = {baslangic}
    adim = 0

    while queue:
        (r, c), su_anki_yol = queue.popleft()
        if (r, c) == hedef:
            yield (ziyaret_edilenler, su_anki_yol, adim, True)
            return
        adim += 1
        yield (ziyaret_edilenler, su_anki_yol, adim, False)

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < satir_sayisi and 0 <= nc < sutun_sayisi:
                if matris[nr, nc] != 1 and (nr, nc) not in ziyaret_edilenler:
                    ziyaret_edilenler.add((nr, nc))
                    queue.append(((nr, nc), su_anki_yol + [(nr, nc)]))


# --- ORGANİZE ÇALIŞTIRMA KISMI (AYNI ANDA HAREKET) ---

# 1. Ana ekranı ve yan yana iki alanı hazırlıyoruz
plt.ion()  # İnteraktif modu aç (hareket için şart)
#fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Orijinal fonksiyonları yedekleyelim
orijinal_subplots = plt.subplots
orijinal_show = plt.show


# --- ÇALIŞTIRMA VE ANIMASYON KISMI ---

def simulasyon_yarisi(matris, baslangic, hedef):
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    cmap = ListedColormap(['#FFD700', '#333333', '#FF0000', '#008000', '#B0C4DE', '#00008B'])

    # Generator objelerini oluştur
    dfs_gen = DFS_Algoritmasi(matris, baslangic, hedef)
    bfs_gen = BFS_Algoritmasi(matris, baslangic, hedef)

    dfs_bitti = False
    bfs_bitti = False

    while not (dfs_bitti and bfs_bitti):
        # DFS Adımı
        if not dfs_bitti:
            try:
                ziyaret, yol, adim, bitti = next(dfs_gen)
                display = matris.copy().astype(float)
                for zr, zc in ziyaret: display[zr, zc] = 4
                for yr, yc in yol: display[yr, yc] = 5
                ax1.clear()
                ax1.imshow(display, cmap=cmap)
                ax1.set_title(f"DFS Adım: {adim}")
                ax1.axis('off')
                if bitti: dfs_bitti = True
            except StopIteration:
                dfs_bitti = True

        # BFS Adımı
        if not bfs_bitti:
            try:
                ziyaret, yol, adim, bitti = next(bfs_gen)
                display = matris.copy().astype(float)
                for zr, zc in ziyaret: display[zr, zc] = 4
                for yr, yc in yol: display[yr, yc] = 5
                ax2.clear()
                ax2.imshow(display, cmap=cmap)
                ax2.set_title(f"BFS Adım: {adim}")
                ax2.axis('off')
                if bitti: bfs_bitti = True
            except StopIteration:
                bfs_bitti = True

        plt.draw()
        plt.pause(0.3)  # Animasyon hızı

    plt.ioff()
    plt.show()


# Yarışı Başlat
simulasyon_yarisi(labirent_matrisi, (6, 0), (0, 4))