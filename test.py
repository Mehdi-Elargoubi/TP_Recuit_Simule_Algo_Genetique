import random
import math

# Fonction donnée pour générer l'état initial
def etatInitial(N):
    etat = []
    for i in range(N):
        etat.append(random.randint(0, N - 1))
    return etat

# Fonction donnée pour afficher l'échiquier
def afficher(etat):
    N = len(etat)
    for i in range(N):
        for j in range(N):
            if etat[j] == i:
                print("|Q", end="")
            else:
                print("| ", end="")
        print("|")

# Fonction donnée pour évaluer le nombre de conflits
def evaluer(etat):
    eval = 0
    N = len(etat)
    for i in range(N):
        for j in range(i + 1, N):
            if etat[i] == etat[j] or abs(i - j) == abs(etat[i] - etat[j]):
                eval += 1
    return eval

# Génération d'un voisin aléatoire
def voisin(etat):
    """
    Génère un voisin aléatoire en déplaçant une reine dans une colonne choisie aléatoirement.
    """
    voisin = etat[:]
    col = random.randint(0, len(etat) - 1)
    voisin[col] = random.randint(0, len(etat) - 1)
    return voisin

# Algorithme de recuit simulé corrigé
def recuit_simule(N, T0, refroidissement, temperature_min=0.01):
    """
    Résout le problème des N-Reines avec l'algorithme du recuit simulé.
    
    Arguments :
    - N : Taille de l'échiquier (N x N).
    - T0 : Température initiale.
    - refroidissement : Facteur de diminution de la température.
    - temperature_min : Température minimale avant arrêt.
    
    Retourne :
    - L'état solution trouvé.
    """
    # Initialisation
    n = etatInitial(N)  # Noeud initial
    t = T0  # Température initiale

    print("Début de l'algorithme")
    print("État initial:", n)
    afficher(n)
    print("Conflits initiaux:", evaluer(n))

    while t > temperature_min:
        # Générer un voisin
        n_prime = voisin(n)
        
        # Calcul de la variation d'énergie
        delta_E = evaluer(n_prime) - evaluer(n)

        # Décision d'acceptation
        if delta_E < 0:
            n = n_prime
        else:
            if random.random() < math.exp(-delta_E / t):
                n = n_prime

        # Refroidir (diminuer la température)
        t *= refroidissement

        # Affichage pour le débogage
        # print(f"Température: {t:.2f}, Conflits: {evaluer(n)}")

        if evaluer(n) == 0:  # Si solution trouvée
            break

    return n

# Test de l'algorithme
if __name__ == "__main__":
    # Paramètres du problème
    N = 8  # Taille de l'échiquier
    T0 = 100  # Température initiale
    refroidissement = 0.99  # Taux de refroidissement

    # Exécution de l'algorithme
    solution = recuit_simule(N, T0, refroidissement)

    # Résultats
    print("Solution trouvée :")
    afficher(solution)
    print("Conflits finaux:", evaluer(solution))

