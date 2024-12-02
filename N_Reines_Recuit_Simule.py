import random

# Génération d'un état initial
def etatInitial(N):
    """
    Crée un état aléatoire où chaque colonne a une reine dans une ligne aléatoire.
    """
    return [random.randint(0, N - 1) for _ in range(N)]

# Évalue le nombre de conflits
def evaluer(etat):
    """
    Compte le nombre de conflits dans un état donné.
    """
    conflits = 0
    N = len(etat)
    for i in range(N):
        for j in range(i + 1, N):
            # Même ligne ou même diagonale
            if etat[i] == etat[j] or abs(i - j) == abs(etat[i] - etat[j]):
                conflits += 1
    return conflits

# Fonction de fitness
def fitness(etat):
    """
    Retourne un score basé sur le nombre de conflits.
    Un état parfait (sans conflit) a un fitness maximal.
    """
    return 1 / (1 + evaluer(etat))  # Plus les conflits sont faibles, plus le fitness est élevé

# Génère une population initiale
def population_initiale(taille_population, N):
    """
    Crée une population initiale de taille donnée pour un échiquier N x N.
    """
    population = []
    for i in range(taille_population):
        population.append(etatInitial(N))
    return population

# Sélectionne un individu avec sélection par roulette
def selection(population):
    """
    Sélectionne un individu de la population proportionnellement à son fitness.
    """
    total = 0
    for solution in population:
        total += fitness(solution)
    r = random.uniform(0, total)
    cumulative_fitness = 0
    for solution in population:
        cumulative_fitness += fitness(solution)
        if cumulative_fitness >= r:
            return solution

# Effectue un croisement entre deux parents
def croisement(parent1, parent2):
    """
    Réalise un croisement entre deux parents pour produire un enfant.
    Utilise un point de croisement unique.
    """
    point = random.randint(1, len(parent1) - 1)  # Point de croisement
    enfant = parent1[:point] + parent2[point:]
    
    return enfant

# Applique une mutation sur un individu
def mutation(etat):
    """
    Applique une mutation aléatoire à un individu en modifiant la position d'une reine.
    """
    col = random.randint(0, len(etat) - 1)  # Colonne à modifier
    etat[col] = random.randint(0, len(etat) - 1)  # Nouvelle position pour cette colonne
    return etat

# Algorithme génétique
def algorithme_genetique(N, taille_population, nombre_generations, taux_mutation):
    # Initialisation de la population
    population = population_initiale(taille_population, N)
    print(population)
    for generation in range(nombre_generations):
        nouvelle_population = []

        for i in range(taille_population // 2):  # On crée des paires de parents
            parent1 = selection(population)
            parent2 = selection(population)
            enfant = croisement(parent1, parent2)
            if random.random() < taux_mutation:  # Applique une mutation avec probabilité
                enfant = mutation(enfant)
            nouvelle_population.extend([parent1, parent2, enfant])  # Ajoute les individus

        population = nouvelle_population  # Remplace l'ancienne population par la nouvelle

        # Affiche les informations sur la meilleure solution actuelle
        meilleure_solution = max(population, key=fitness)
        print(f"Génération {generation + 1}: Conflits = {evaluer(meilleure_solution)}")

        # Si une solution parfaite est trouvée, on arrête
        if evaluer(meilleure_solution) == 0:
            print("Solution parfaite trouvée !")
            return meilleure_solution

    # Retourne le meilleur individu de la population finale
    return max(population, key=fitness)

# Test de l'algorithme
if __name__ == "__main__":
    N = 4  # Taille de l'échiquier
    taille_population = 4  # Taille de la population
    nombre_generations = 500  # Nombre maximal de générations
    taux_mutation = 0.1  # Probabilité de mutation

    solution = algorithme_genetique(N, taille_population, nombre_generations, taux_mutation)
    print("Meilleure solution trouvée :", solution)
    print("Conflits :", evaluer(solution))
