
import random
from simpleai.search import SearchProblem, hill_climbing_random_restarts


class TSPHillClimbing(SearchProblem):
    def __init__(self, n, matrice):
        self.n = n                # numarul de orase
        self.matrice = matrice    # matricea de distante
        # Starea initiala: ordinea naturala a oraselor
        super().__init__(initial_state=tuple(range(n)))

    # Metoda folosita de simpleai pentru reporniri aleatorii
    def generate_random_state(self):
        state = list(range(self.n))
        random.shuffle(state)
        return tuple(state)

    # Generarea tuturor perechilor de indici pentru operatia 2-opt
    def actions(self, state):
        return [(i, j) for i in range(self.n) for j in range(i + 1, self.n)]

    # Rezultatul aplicarii unei actiuni: inversarea segmentului i..j
    def result(self, state, action):
        i, j = action
        new_state = list(state)
        new_state[i:j+1] = reversed(new_state[i:j+1])
        return tuple(new_state)

    # Functia de evaluare (valoare negativa a costului, deoarece hill climbing maximizeaza)
    def value(self, state):
        cost = sum(self.matrice[state[k]][state[(k+1)%self.n]] for k in range(self.n))
        return -cost

# Functie publica care rezolva TSP folosind hill_climbing cu reporniri aleatorii
def rezolva_tsp_hc(n, matrice, reporniri=20):
    problem = TSPHillClimbing(n, matrice)
    solution = hill_climbing_random_restarts(problem, restarts_limit=reporniri)
    return list(solution.state), -solution.value

# Test rapid daca rulam direct fisierul
if __name__ == "__main__":
    matrice_exemplu = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    traseu, cost = rezolva_tsp_hc(4, matrice_exemplu, reporniri=5)
    print("Hill Climbing - traseu:", traseu, "cost:", cost)