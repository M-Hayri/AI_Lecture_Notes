"""
Bu algoritma, girilen görüntüyü 8 eşit parcaya ayırıp karıştırır. Daha sonrasında düzenle talimatı verildiğinde
adım adım düzenli bir şekilde yapbozu çözer.

author : Muhammed Hayri ÖZCAN
date: 04.07.2026
"""

import random
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from queue import PriorityQueue

# --- BÖLÜM 1: TANIMLAMALAR (Dokunulmadı) ---
parca1 = 'imgs/parca_1.png'
parca2 = 'imgs/parca_2.png'
parca3 = 'imgs/parca_3.png'
parca4 = 'imgs/parca_4.png'
parca5 = 'imgs/parca_5.png'
parca6 = 'imgs/parca_6.png'
parca7 = 'imgs/parca_7.png'
parca8 = 'imgs/parca_8.png'
bosluk = 'imgs/siyah_resim.png'

# Algoritmanın kolay çalışması için yolları bir listede (map) tutalım
# İndeksler: 0,1,2,3,4,5,6,7 -> Parçalar | 8 -> Boşluk (Siyah)
PATH_LIST = [parca1, parca2, parca3, parca4, parca5, parca6, parca7, parca8, bosluk]
GOAL_STATE = (0, 1, 2, 3, 4, 5, 6, 7, 8)


# --- BÖLÜM 2: AGENT VE STATE MANTIĞI ---

def get_manhattan_distance(state):
    """Sezgisel (Heuristic) Fonksiyon: Her parçanın hedefteki yerine olan uzaklığı."""
    distance = 0
    for i in range(9):
        val = state[i]
        if val != 8:  # Boşluk (siyah resim) mesafeye dahil edilmez
            current_row, current_col = divmod(i, 3)
            target_row, target_col = divmod(val, 3)
            distance += abs(current_row - target_row) + abs(current_col - target_col)
    return distance


def get_neighbors(state):
    """Action: Boşluğun gidebileceği yönleri ve yeni durumları üretir."""
    neighbors = []
    idx = state.index(8)  # Boşluğun (8) konumunu bul
    row, col = divmod(idx, 3)

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Yukarı, Aşağı, Sol, Sağ
    for dr, dc in moves:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            n_idx = nr * 3 + nc
            new_state = list(state)
            new_state[idx], new_state[n_idx] = new_state[n_idx], new_state[idx]
            neighbors.append(tuple(new_state))
    return neighbors


def solve_puzzle(initial_state):
    """A* Search Algoritması: Hedefe giden en kısa yolu bulur."""
    queue = PriorityQueue()
    # (Öncelik, Mevcut Durum, Gidilen Yol)
    queue.put((0, initial_state, []))
    visited = {initial_state}

    while not queue.empty():
        _, current, path = queue.get()

        if current == GOAL_STATE:
            return path

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                # f(n) = g(n) + h(n) -> Adım sayısı + Manhattan Mesafesi
                priority = len(path) + 1 + get_manhattan_distance(neighbor)
                queue.put((priority, neighbor, path + [neighbor]))
    return None


# --- BÖLÜM 3: GÖRSELLEŞTİRME VE ANİMASYON ---

def ekrana_bas(state, ax_list, fig, title):
    """Durumu ekrandaki mevcut subplotlar üzerine çizer."""
    for i, ax in enumerate(ax_list.flat):
        ax.clear()
        img = mpimg.imread(PATH_LIST[state[i]])
        ax.imshow(img)
        ax.axis('off')
    fig.suptitle(title, fontsize=16)
    plt.draw()
    plt.pause(0.5)  # Animasyon hızı


# --- UYGULAMA BAŞLANGICI ---

# 1. Başlangıç Durumunu Oluştur (Karıştır)
initial_state_list = list(GOAL_STATE)
random.shuffle(initial_state_list)
initial_state = tuple(initial_state_list)

# 2. Arayüzü Hazırla
plt.ion()  # İnteraktif mod açık (Animasyon için şart)
fig, axes = plt.subplots(3, 3, figsize=(6, 6))
plt.subplots_adjust(wspace=0.05, hspace=0.05)

print("Agent çözüm arıyor...")
yol = solve_puzzle(initial_state)

if yol:
    print(f"Çözüm bulundu! {len(yol)} hamlede tamamlanacak.")
    # Başlangıç halini göster
    ekrana_bas(initial_state, axes, fig, "Başlangıç Durumu (Karışık)")
    time.sleep(1.5)

    # Yol üzerindeki her durumu (State) animasyonla göster
    for i, step in enumerate(yol):
        ekrana_bas(step, axes, fig, f"Düzenleniyor... Hamle: {i + 1}/{len(yol)}")

    fig.suptitle("Bulmaca Çözüldü!", color='green', fontsize=20)
    plt.ioff()
    plt.show()
else:
    # Not: 8-puzzle'da tüm rastgele dizilimler çözülemez.
    # Eğer bu mesajı alırsan kodu tekrar çalıştır.
    print("Seçilen dizilim matematiksel olarak çözülemez. Tekrar deneniyor...")