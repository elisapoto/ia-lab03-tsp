"""Modul pentru operații de intrare/ieșire specifice problemei TSP."""

import os
from typing import List, Tuple

def citeste_matrice(cale_fisier: str) -> Tuple[int, List[List[int]]]:
    """Citește matricea de distanțe dintr-un fișier text.

    Formatul așteptat al fișierului: prima linie conține N (numărul de orașe),
    iar următoarele N linii conțin câte N întregi separați prin spații.

    Args:
        cale_fisier (str): Calea către fișierul de intrare.

    Returns:
        Tuple[int, List[List[int]]]: Un tuplu format din:
            - n (int): Numărul de orașe.
            - matrice (List[List[int]]): Matricea de distanțe NxN.

    Raises:
        FileNotFoundError: Dacă fișierul specificat nu există.
        ValueError: Dacă formatul fișierului este invalid sau datele nu pot fi convertite.
    """
    if not os.path.exists(cale_fisier):
        raise FileNotFoundError(f"Fișierul nu a fost găsit la calea: {cale_fisier}")

    with open(cale_fisier, 'r', encoding='utf-8') as f:
        linii = [linie.strip() for linie in f if linie.strip()]
        
    if not linii:
        raise ValueError("Fișierul este gol.")

    try:
        n = int(linii[0])
        matrice = [[int(x) for x in linii[i + 1].split()] for i in range(n)]
    except (ValueError, IndexError) as e:
        raise ValueError(f"Format invalid al fișierului de intrare: {e}")

    return n, matrice

def salveaza_rezultat(cale_fisier: str, traseu: List[int], cost: int, durata: float) -> None:
    """Salvează rezultatul rulării algoritmului într-un fișier text.

    Args:
        cale_fisier (str): Calea către fișierul de ieșire.
        traseu (List[int]): Lista cu ordinea orașelor vizitate.
        cost (int): Costul minim al traseului optim.
        durata (float): Timpul de execuție în secunde.
        
    Raises:
        IOError: Dacă apar probleme la scrierea în fișier.
    """
    try:
        with open(cale_fisier, 'w', encoding='utf-8') as f:
            if traseu:
                sir_traseu = " -> ".join(map(str, traseu))
                sir_traseu += f" -> {traseu[0]}"
                f.write(f"Traseu optim: {sir_traseu}\n")
                f.write(f"Cost minim: {cost}\n")
            else:
                f.write("Nu a fost gasit niciun traseu valid.\n")
            f.write(f"Timp de executie: {durata:.6f} secunde\n")
    except IOError as e:
        raise IOError(f"Eroare la scrierea fișierului de rezultate: {e}")