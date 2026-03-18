"""Modul pentru rezolvarea TSP folosind Hill Climbing (Implementare Manuală)."""

import random
from typing import List, Tuple

def calculeaza_cost(traseu: List[int], matrice: List[List[int]]) -> int:
    """Calculează costul total al unui traseu, inclusiv întoarcerea."""
    cost = 0
    n = len(traseu)
    for i in range(n - 1):
        cost += matrice[traseu[i]][traseu[i+1]]
    cost += matrice[traseu[-1]][traseu[0]]
    return cost

def genereaza_vecini_2opt(traseu: List[int]) -> List[List[int]]:
    """Generează toți vecinii posibili folosind metoda 2-opt (inversare segmente).
    Orașul de start (index 0) rămâne mereu fix."""
    vecini = []
    n = len(traseu)
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            # Copiem traseul și inversăm segmentul de la i la j
            vecin = traseu[:]
            vecin[i:j+1] = reversed(vecin[i:j+1])
            vecini.append(vecin)
    return vecini

def hc_o_rulare(n: int, matrice: List[List[int]]) -> Tuple[List[int], int]:
    """Execută o singură rulare de Hill Climbing până la un optim local."""
    # Generăm o soluție inițială aleatorie (orașul 0 e mereu primul)
    traseu_curent = [0] + random.sample(range(1, n), n - 1)
    cost_curent = calculeaza_cost(traseu_curent, matrice)
    
    while True:
        vecini = genereaza_vecini_2opt(traseu_curent)
        cel_mai_bun_vecin = None
        cel_mai_bun_cost = cost_curent
        
        # Căutăm cel mai bun vecin din împrejurimi
        for vecin in vecini:
            cost_vecin = calculeaza_cost(vecin, matrice)
            if cost_vecin < cel_mai_bun_cost:
                cel_mai_bun_cost = cost_vecin
                cel_mai_bun_vecin = vecin
                
        # Dacă nu am găsit niciun vecin mai bun, ne oprim (optim local)
        if cel_mai_bun_vecin is None:
            break
            
        # Altfel, facem "pasul" către noul vecin
        traseu_curent = cel_mai_bun_vecin
        cost_curent = cel_mai_bun_cost
        
    return traseu_curent, cost_curent

def rezolva_tsp_hc_manual(n: int, matrice: List[List[int]], reporniri: int = 10) -> Tuple[List[int], int]:
    """Rezolvă TSP folosind Hill Climbing cu reporniri aleatorii (Random Restarts)."""
    cel_mai_bun_traseu_global = []
    cel_mai_bun_cost_global = float('inf')
    
    # Rulăm de mai multe ori din puncte diferite de start pentru a evita blocajele
    for _ in range(reporniri):
        traseu, cost = hc_o_rulare(n, matrice)
        if cost < cel_mai_bun_cost_global:
            cel_mai_bun_cost_global = cost
            cel_mai_bun_traseu_global = traseu
            
    return cel_mai_bun_traseu_global, cel_mai_bun_cost_global

# Bloc de testare
if __name__ == "__main__":
    test_matrice = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    traseu, cost = rezolva_tsp_hc_manual(4, test_matrice)
    print(f"Traseu HC Manual: {traseu} | Cost: {cost}")