import random  # Module pour générer des nombres aléatoires
import math  # Module pour utiliser des fonctions mathématiques comme exp()

# Génération de l'état initial
def etatInitial(N):
    """
    Génère un état aléatoire pour un échiquier de taille N x N.
    Chaque colonne contient une reine placée dans une ligne aléatoire.
    """
    etat = []  # Liste qui contiendra les positions des reines
    for i in range(N):  # Boucle pour chaque colonne
        etat.append(random.randint(0, N - 1))  # Place une reine dans une ligne aléatoire
    return etat  # Retourne l'état généré

# Affichage de l'échiquier
def afficher(etat):
    """
    Affiche graphiquement un échiquier à partir d'une liste de positions.
    Chaque valeur dans la liste représente la ligne où se trouve la reine dans une colonne donnée.
    """
    N = len(etat)  # Taille de l'échiquier (nombre de colonnes)
    for i in range(N):  # Boucle pour chaque ligne
        for j in range(N):  # Boucle pour chaque colonne
            if etat[j] == i:  # Si une reine est sur cette position
                print("|Q", end="")  # Affiche une reine 'Q'
            else:
                print("| ", end="")  # Sinon, affiche une case vide
        print("|")  # Passe à la ligne suivante

# Fonction pour évaluer un état
def evaluer(etat):
    """
    Calcule le nombre de conflits dans un état donné.
    Les conflits se produisent si deux reines sont :
    - Sur la même ligne
    - Sur la même diagonale
    """
    eval = 0  # Initialise le nombre de conflits à 0
    N = len(etat)  # Taille de l'échiquier
    for i in range(N):  # Boucle pour la première reine
        for j in range(i + 1, N):  # Boucle pour la deuxième reine (évite de compter deux fois)
            if etat[i] == etat[j] or abs(i - j) == abs(etat[i] - etat[j]):  
                # Même ligne ou même diagonale
                eval += 1  # Augmente le nombre de conflits
    return eval  # Retourne le nombre total de conflits

# Génération d'un voisin
def voisin(etat):
    """
    Génère un état voisin en modifiant aléatoirement la position d'une reine.
    """
    voisin = etat[:]  # Copie de l'état actuel
    col = random.randint(0, len(etat) - 1)  # Choisit une colonne au hasard
    voisin[col] = random.randint(0, len(etat) - 1)  # Déplace la reine dans une autre ligne
    return voisin  # Retourne le nouvel état

# Algorithme de recuit simulé
def recuit_simule(N, T0, refroidissement, temperature_min=0.01):
    """
    Implémente l'algorithme du recuit simulé pour résoudre le problème des N-Reines.
    
    Arguments :
    - N : Taille de l'échiquier (N x N)
    - T0 : Température initiale
    - refroidissement : Facteur de diminution de la température
    - temperature_min : Température minimale pour arrêter l'algorithme
    """
    # Initialisation de l'état et de la température
    n = etatInitial(N)  # Génère un état initial aléatoire
    print("État initial :")
    afficher(n)  # Affiche l'état initial
    print(f"Conflits initiaux : {evaluer(n)}\n")  # Affiche le nombre de conflits initiaux
    
    t = T0  # Définit la température initiale

    while t > temperature_min:  # Continue tant que la température n'est pas trop basse
        n_prime = voisin(n)  # Génère un voisin aléatoire
        delta_E = evaluer(n_prime) - evaluer(n)  # Calcule la variation d'énergie (changement de conflits)

        # Décide si on accepte l'état voisin
        if delta_E < 0:  # Si le voisin est meilleur (moins de conflits)
            n = n_prime  # Accepte l'état voisin
        else:  # Sinon, accepte avec une certaine probabilité
            if random.random() < math.exp(-delta_E / t):  # Probabilité décroissante avec la température
                n = n_prime  # Accepte l'état voisin malgré qu'il soit pire

        t *= refroidissement  # Réduit la température selon le facteur de refroidissement

        # Affiche les informations sur l'état courant
        print(f"Température: {t:.2f}, Conflits: {evaluer(n)}")

        if evaluer(n) == 0:  # Si une solution sans conflits est trouvée
            break  # Arrête l'algorithme

    return n  # Retourne l'état solution trouvé

# Exécution principale
if __name__ == "__main__":
    """
    Définit les paramètres et exécute l'algorithme de recuit simulé.
    """
    N = 8  # Taille de l'échiquier
    T0 = 100  # Température initiale
    refroidissement = 0.99  # Facteur de refroidissement

    # Lance l'algorithme et récupère la solution
    solution = recuit_simule(N, T0, refroidissement)

    # Affiche la solution trouvée
    print("Solution trouvée :")
    afficher(solution)
