"""Modul pentru rezolvarea TSP folosind Backtracking recursiv."""

import sys
from typing import List, Tuple

def rezolva_tsp_backtracking(n: int, matrice: List[List[int]]) -> Tuple[List[int], int]:
    """Rezolvă problema comis-voiajorului (TSP) prin backtracking recursiv.

    Explorează exhaustiv spațiul de soluții pentru a găsi traseul de cost minim,
    folosind prunere branch-and-bound. Elimină variabilele globale folosind
    un dicționar intern pentru memorarea stării optime.

    Args:
        n (int): Numărul de orașe.
        matrice (List[List[int]]): Matricea de distanțe NxN.

    Returns:
        Tuple[List[int], int]: Un tuplu conținând:
            - traseu_optim (List[int]): Lista indicilor orașelor în ordinea vizitării.
            - cost_minim (int): Costul total al traseului optim. 
              (Returnează liste goale și sys.maxsize dacă eșuează).
    """
    # Folosim un dicționar mutabil pentru a reține starea fără variabile "global"
    stare_optima = {
        'cost_minim': sys.maxsize,
        'traseu_optim': []
    }
    
    vizitat = [False] * n
    vizitat[0] = True
    
    def _backtracking(oras_curent: int, traseu: List[int], cost: int) -> None:
        """Funcție internă recursivă (closure) pentru explorarea soluțiilor."""
        # Caz de bază: am vizitat toate orașele
        if len(traseu) == n:
            cost_total = cost + matrice[oras_curent][traseu[0]]
            if cost_total < stare_optima['cost_minim']:
                stare_optima['cost_minim'] = cost_total
                stare_optima['traseu_optim'] = traseu[:]
            return
            
        # Generăm vecinii
        for urmator in range(n):
            if vizitat[urmator]:
                continue
                
            cost_nou = cost + matrice[oras_curent][urmator]
            
            # Prunere: abandonăm ramura dacă depășim costul minim deja găsit
            if cost_nou >= stare_optima['cost_minim']:
                continue
                
            vizitat[urmator] = True
            traseu.append(urmator)
            
            _backtracking(urmator, traseu, cost_nou)
            
            # Revenire (backtrack)
            traseu.pop()
            vizitat[urmator] = False

    # Inițiem căutarea pornind din orașul 0
    _backtracking(0, [0], 0)
    
    return stare_optima['traseu_optim'], stare_optima['cost_minim']