"""Punctul central de intrare în aplicație."""

import argparse
import time
import sys
from utils.io_utils import citeste_matrice, salveaza_rezultat
from utils.backtracking import rezolva_tsp_backtracking
from hill_climbing_tsp import rezolva_tsp_hc

def main():
    """Parsează argumentele din consolă și orchestrează execuția algoritmului."""
    parser = argparse.ArgumentParser(description="Rezolvarea problemei TSP folosind Backtracking.")
    parser.add_argument("intrare", help="Calea către fișierul text cu matricea de distanțe.")
    parser.add_argument("--iesire", "-o", help="Calea opțională pentru salvarea rezultatului.", default=None)
    
    args = parser.parse_args()
    
    try:
        n, matrice = citeste_matrice(args.intrare)
        print(f"Număr de orașe: {n}")
        
        start = time.perf_counter()
        traseu, cost = rezolva_tsp_backtracking(n, matrice)
        durata = time.perf_counter() - start
        
        if traseu:
            sir_traseu = " -> ".join(map(str, traseu))
            sir_traseu += f" -> {traseu[0]}"
            print(f"Traseu optim:   {sir_traseu}")
            print(f"Cost minim:     {cost}")
        else:
            print("Nu a fost găsit niciun traseu valid.")
            
        print(f"Timp de execuție: {durata:.6f} secunde")
        
        if args.iesire:
            salveaza_rezultat(args.iesire, traseu, cost, durata)
            print(f"-> Rezultatele au fost salvate în: {args.iesire}")
            
    except Exception as e:
        print(f"Eroare fatală la rulare: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()