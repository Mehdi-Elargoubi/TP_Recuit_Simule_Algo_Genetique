import random  # Module pour générer des nombres aléatoires

# Génération d'un état initial
def etatInitial(N):
    """
    Crée un état aléatoire où chaque colonne a une reine dans une ligne aléatoire.
    """
    # Retourne une liste de N entiers. Chaque entier représente la ligne où se trouve la reine dans une colonne donnée.
    return [random.randint(0, N - 1) for _ in range(N)]

# Évalue le nombre de conflits
def evaluer(etat):
    """
    Compte le nombre de conflits dans un état donné.
    """
    conflits = 0  # Initialise le compteur de conflits à 0
    N = len(etat)  # Taille de l'échiquier
    # Compare chaque reine avec toutes les reines suivantes
    for i in range(N):
        for j in range(i + 1, N):
            # Un conflit existe si deux reines sont sur la même ligne ou sur une diagonale
            if etat[i] == etat[j] or abs(i - j) == abs(etat[i] - etat[j]):
                conflits += 1  # Incrémente le compteur de conflits
    return conflits

# Fonction de fitness
def fitness(etat):
    """
    Retourne un score basé sur le nombre de conflits.
    Un état parfait (sans conflit) a un fitness maximal.
    """
    # Fitness est calculé comme l'inverse du nombre de conflits (plus c'est élevé, mieux c'est)
    return 1 / (1 + evaluer(etat))

# Génère une population initiale
def population_initiale(taille_population, N):
    """
    Crée une population initiale de taille donnée pour un échiquier N x N.
    """
    population = []  # Liste pour stocker la population
    # Génère 'taille_population' individus aléatoires
    for i in range(taille_population):
        population.append(etatInitial(N))  # Ajoute un état généré aléatoirement
    return population

# Sélectionne un individu avec sélection par roulette
def selection(population):
    """
    Sélectionne un individu de la population proportionnellement à son fitness.
    """
    total = 0  # Initialisation de la somme totale des fitness
    for solution in population:
        total += fitness(solution)  # Calcule la somme totale des fitness
    r = random.uniform(0, total)  # Tire un nombre aléatoire entre 0 et la somme totale
    cumulative_fitness = 0  # Initialisation de la somme cumulative
    for solution in population:
        cumulative_fitness += fitness(solution)  # Ajoute le fitness de l'individu courant
        if cumulative_fitness >= r:  # Si la somme cumulative dépasse 'r', on sélectionne cet individu
            return solution

# Effectue un croisement entre deux parents
def croisement(parent1, parent2):
    """
    Réalise un croisement entre deux parents pour produire un enfant.
    Utilise un point de croisement unique.
    """
    # Point de croisement choisi aléatoirement entre 1 et len(parent1) - 1
    point = random.randint(1, len(parent1) - 1)
    # Combine les gènes du parent1 avant le point avec ceux du parent2 après le point
    enfant = parent1[:point] + parent2[point:]
    return enfant

# Applique une mutation sur un individu
def mutation(etat):
    """
    Applique une mutation aléatoire à un individu en modifiant la position d'une reine.
    """
    col = random.randint(0, len(etat) - 1)  # Choisit une colonne au hasard
    etat[col] = random.randint(0, len(etat) - 1)  # Change la ligne de la reine dans cette colonne
    return etat

# Algorithme génétique
def algorithme_genetique(N, taille_population, nombre_generations, taux_mutation):
    """
    Implémente l'algorithme génétique pour résoudre le problème des N-Reines.
    
    Arguments :
    - N : Taille de l'échiquier
    - taille_population : Nombre d'individus dans la population
    - nombre_generations : Nombre maximal de générations
    - taux_mutation : Probabilité de mutation
    
    Retourne :
    - La meilleure solution trouvée
    """
    # Génère la population initiale
    population = population_initiale(taille_population, N)

    # Pour chaque génération
    for generation in range(nombre_generations):
        nouvelle_population = []  # Liste pour stocker la nouvelle population

        # Crée des enfants à partir de paires de parents
        for i in range(taille_population // 2):  # Divise la population en paires
            parent1 = selection(population)  # Sélectionne le premier parent
            parent2 = selection(population)  # Sélectionne le second parent
            enfant = croisement(parent1, parent2)  # Produit un enfant par croisement

            # Avec une probabilité 'taux_mutation', applique une mutation à l'enfant
            if random.random() < taux_mutation:
                enfant = mutation(enfant)

            # Ajoute les parents et l'enfant à la nouvelle population
            nouvelle_population.extend([parent1, parent2, enfant])

        # Remplace l'ancienne population par la nouvelle
        population = nouvelle_population

        # Cherche la meilleure solution dans la population actuelle
        meilleure_solution = max(population, key=fitness)  # Individu avec le meilleur fitness
        print(f"Génération {generation + 1}: Conflits = {evaluer(meilleure_solution)}")

        # Si une solution parfaite est trouvée, arrête l'algorithme
        if evaluer(meilleure_solution) == 0:
            print("Solution parfaite trouvée !")
            return meilleure_solution

    # Retourne la meilleure solution de la dernière population
    return max(population, key=fitness)

# Test de l'algorithme
if __name__ == "__main__":
    # Paramètres du problème
    N = 8  # Taille de l'échiquier
    taille_population = 20  # Nombre d'individus dans la population
    nombre_generations = 100  # Nombre maximal de générations
    taux_mutation = 0.1  # Probabilité de mutation

    # Exécution de l'algorithme génétique
    solution = algorithme_genetique(N, taille_population, nombre_generations, taux_mutation)

    # Affiche la meilleure solution trouvée et le nombre de conflits
    print("Meilleure solution trouvée :", solution)
    print("Conflits :", evaluer(solution))
