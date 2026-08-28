from game.creature import Creature


class Simulation:
    def __init__(self, world):
        self.world = world
        self.generation = 0

    def count_neighbors(self, x, y):
        count = 0

        for dy in range(-1, 2):
            for dx in range(-1, 2):

                # Don't count the cell itself
                if dx == 0 and dy == 0:
                    continue

                nx = x + dx
                ny = y + dy

                # Ignore cells outside the world
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

                neighbors = self.count_neighbors(x, y)
                alive = self.world.is_alive(x, y)

                # Conway's Game of Life rules
                if alive and neighbors in (2, 3):
                    new_grid[y][x] = self.world.get_creature(x, y)

                elif not alive and neighbors == 3:
                    new_grid[y][x] = Creature()

        self.world.grid = new_grid
        self.generation += 1