from collections import Counter


class Statistics:
    def __init__(self):
        self.generation = 0

        self.total_births = 0
        self.total_deaths = 0

        self.peak_population = 0
        self.previous_population = 0

        self.population_history = []

        self.simulation_time = 0

        self.deaths_by_type = Counter()
        self.births_by_type = Counter()

    def record_birth(self, creature):
        self.total_births += 1
        self.births_by_type[creature.creature_type] += 1

    def record_death(self, creature):
        self.total_deaths += 1
        self.deaths_by_type[creature.creature_type] += 1

    def update(self, world, delta_time):
        self.generation += 1

        self.simulation_time += delta_time

        population = self.get_population(world)

        self.peak_population = max(
            self.peak_population,
            population
        )

        self.population_history.append(population)

        self.previous_population = population

    def get_population(self, world):
        population = 0

        for row in world.grid:
            for creature in row:
                if creature is not None:
                    population += 1

        return population

    def get_population_by_type(self, world):
        counts = Counter()

        for row in world.grid:
            for creature in row:
                if creature is not None:
                    counts[creature.creature_type] += 1

        return counts

    def get_population_change(self, world):
        population = self.get_population(world)

        if len(self.population_history) < 2:
            return 0

        return population - self.population_history[-2]

    def get_average_age(self, world):
        creatures = []

        for row in world.grid:
            for creature in row:
                if creature is not None:
                    creatures.append(creature)

        if not creatures:
            return 0

        return sum(
            creature.age for creature in creatures
        ) / len(creatures)