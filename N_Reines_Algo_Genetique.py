import random

def etatInitial(N):
    return [random.randint(0, N - 1) for _ in range(N)]

def evaluer(etat):
    conflits = 0
    N = len(etat)
    for i in range(N):
        for j in range(i + 1, N):
            if etat[i] == etat[j] or abs(i - j) == abs(etat[i] - etat[j]):
                conflits += 1
    return conflits

def fitness(etat):
    return 1 / (1 + evaluer(etat))

def population_initiale(taille_population, N):
    return [etatInitial(N) for _ in range(taille_population)]

def selection(population):
    total = sum(fitness(solution) for solution in population)
    r = random.uniform(0, total)
    cumulative_fitness = 0
    for solution in population:
        cumulative_fitness += fitness(solution)
        if cumulative_fitness >= r:
            return solution

def croisement(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]

def mutation(etat):
    col = random.randint(0, len(etat) - 1)
    etat[col] = random.randint(0, len(etat) - 1)
    return etat

def algorithme_genetique(N, taille_population, nombre_generations, taux_mutation):
    population = population_initiale(taille_population, N)
    #print(population)
    for generation in range(nombre_generations):
        nouvelle_population = []
        for i in range(taille_population // 2):
            parent1 = selection(population)
            parent2 = selection(population)
            enfant = croisement(parent1, parent2)
            if random.random() < taux_mutation:
                enfant = mutation(enfant)
            nouvelle_population.extend([parent1, parent2, enfant])
        population = nouvelle_population
        meilleure_solution = max(population, key=fitness)
        print(f"Génération {generation + 1}: Conflits = {evaluer(meilleure_solution)}")
        if evaluer(meilleure_solution) == 0:
            print("Solution parfaite trouvée !")
            return meilleure_solution
    return max(population, key=fitness)

if __name__ == "__main__":
    N = 8
    taille_population = 8
    nombre_generations = 100
    taux_mutation = 0.1

    solution = algorithme_genetique(N, taille_population, nombre_generations, taux_mutation)
    print("Meilleure solution trouvée :", solution)
    print("Conflits :", evaluer(solution))
