"""Modul pentru evaluarea performanței și generarea de date sintetice."""

import sys
import os
import time
import random
import logging
from typing import List, Tuple, Callable
import matplotlib.pyplot as plt

# Configurare afișare mesaje în terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

# Adăugăm rădăcina proiectului ca să funcționeze importurile oriunde ai rula
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


# IMPORTANT: Asigură-te că fișierele sunt exact în aceste foldere!
from src.utils.backtracking import rezolva_tsp_backtracking
from src.hill_climbing_tsp import rezolva_tsp_hc
from src.hill_climbing_manual import rezolva_tsp_hc_manual

def genereaza_instanta_tsp(n: int, limita_maxima: int = 100, seed: int = 42) -> Tuple[int, List[List[int]]]:
    """Generează o instanță aleatorie validă a problemei TSP (matrice simetrică)."""
    random.seed(seed)
    matrice = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            distanta = random.randint(1, limita_maxima)
            matrice[i][j] = distanta
            matrice[j][i] = distanta  # TSP Simetric
    return n, matrice

def masoara_timpul(functie: Callable, *args) -> float:
    """Măsoară cât durează execuția unei funcții în secunde."""
    start = time.perf_counter()
    functie(*args)
    return time.perf_counter() - start

def genereaza_grafic(n_bt, timpi_bt, n_hc, timpi_hc_simpleai, timpi_hc_manual):
    """Desenează graficul comparativ cu 3 linii și îl salvează ca imagine."""
    logging.info("Generez graficul...")
    plt.figure(figsize=(10, 6))
    
    # Desenăm cele 3 linii
    plt.plot(n_bt, timpi_bt, 'o-', color='red', label='Backtracking (Exact)', linewidth=2)
    plt.plot(n_hc, timpi_hc_simpleai, 's-', color='blue', label='HC SimpleAI (Euristic)', linewidth=2)
    plt.plot(n_hc, timpi_hc_manual, '^-', color='green', label='HC Manual (Euristic)', linewidth=2)
    
    # Setări vizuale
    plt.title("Comparare Performanță Algoritmi TSP", fontsize=14)
    plt.xlabel("Număr de orașe (N)", fontsize=12)
    plt.ylabel("Timp de execuție (secunde)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=11)
    
    # Salvăm imaginea
    nume_fisier = "grafic_comparativ_final.png"
    plt.savefig(nume_fisier, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info(f"Graficul a fost salvat cu succes ca: {nume_fisier}")


def ruleaza_experiment():
    """Rulează experimentul comparativ și adună datele pentru grafic."""
    # Backtracking "crapă" la N mare, deci îl testăm doar pe numere mici
    valori_n_bt = [4, 5, 6, 7, 8, 9, 10]
    
    # Hill Climbing duce și numere mai mari
    valori_n_hc = [4, 5, 6, 7, 8, 9, 10, 15, 20, 30]
    
    timpi_bt = []
    timpi_hc_simpleai = []
    timpi_hc_manual = []

    logging.info("START EXPERIMENT")

    # 1. Măsurăm Backtracking
    logging.info("--> Rulez Backtracking...")
    for n in valori_n_bt:
        _, matrice = genereaza_instanta_tsp(n)
        timp = masoara_timpul(rezolva_tsp_backtracking, n, matrice)
        timpi_bt.append(timp)
        print(f"  Backtracking pt N={n} a durat {timp:.5f} secunde")

    # 2. Măsurăm Hill Climbing SimpleAI
    logging.info("--> Rulez Hill Climbing (SimpleAI)...")
    for n in valori_n_hc:
        _, matrice = genereaza_instanta_tsp(n)
        timp = masoara_timpul(rezolva_tsp_hc, n, matrice, 10) # 10 reporniri
        timpi_hc_simpleai.append(timp)
        print(f"  HC SimpleAI pt N={n} a durat {timp:.5f} secunde")

    # 3. Măsurăm Hill Climbing Manual
    logging.info("--> Rulez Hill Climbing (Manual)...")
    for n in valori_n_hc:
        _, matrice = genereaza_instanta_tsp(n)
        timp = masoara_timpul(rezolva_tsp_hc_manual, n, matrice, 10) # 10 reporniri
        timpi_hc_manual.append(timp)
        print(f"  HC Manual pt N={n} a durat {timp:.5f} secunde")

    # Desenăm rezultatele
    genereaza_grafic(valori_n_bt, timpi_bt, valori_n_hc, timpi_hc_simpleai, timpi_hc_manual)
    logging.info("EXPERIMENT FINALIZAT")

if __name__ == "__main__":
    ruleaza_experiment()