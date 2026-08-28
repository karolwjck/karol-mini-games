class Creature:
    def __init__(self, creature_type="Basic"):
        self.creature_type = creature_type
        self.age = 0

    def update(self):
        self.age += 1