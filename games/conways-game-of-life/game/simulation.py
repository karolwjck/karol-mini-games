from game.creature import Creature


class Simulation:
    def __init__(self, world, statistics):
        self.world = world
        self.statistics = statistics

    def count_neighbors(self, x, y):
        count = 0

        for dy in range(-1, 2):
            for dx in range(-1, 2):

                if dx == 0 and dy == 0:
                    continue

                nx = x + dx
                ny = y + dy

                if nx < 0 or nx >= self.world.width:
                    continue

                if ny < 0 or ny >= self.world.height:
                    continue

                if self.world.is_alive(nx, ny):
                    count += 1

        return count

    def update(self):
        new_grid = [
            [None for _ in range(self.world.width)]
            for _ in range(self.world.height)
        ]

        for y in range(self.world.height):
            for x in range(self.world.width):

                creature = self.world.get_creature(x, y)
                neighbors = self.count_neighbors(x, y)

                # Existing creature survives
                if creature is not None and neighbors in (2, 3):

                    creature.update()

                    new_grid[y][x] = creature

                # Existing creature dies
                elif creature is not None:

                    self.statistics.record_death(creature)

                # New creature is born
                elif creature is None and neighbors == 3:

                    new_creature = Creature()

                    self.statistics.record_birth(new_creature)

                    new_grid[y][x] = new_creature

        self.world.grid = new_grid