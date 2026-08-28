class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.grid = [
            [None for _ in range(width)]
            for _ in range(height)
        ]

    def get_creature(self, x, y):
        return self.grid[y][x]

    def set_creature(self, x, y, creature):
        self.grid[y][x] = creature

    def is_alive(self, x, y):
        return self.grid[y][x] is not None