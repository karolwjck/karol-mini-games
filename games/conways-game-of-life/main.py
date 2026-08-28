import pygame

from game.config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GRID_WIDTH,
    GRID_HEIGHT,
    FPS,
    GENERATIONS_PER_SECOND,
    CELL_SIZE,
)

from game.world import World
from game.simulation import Simulation
from game.creature import Creature
from game.statistics import Statistics

from ui.game_view import GameView
from ui.statistics_view import StatisticsView


def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )

    pygame.display.set_caption(
        "Game of Life"
    )

    clock = pygame.time.Clock()

    world = World(
        GRID_WIDTH,
        GRID_HEIGHT,
    )

    statistics = Statistics()

    simulation = Simulation(
        world,
        statistics,
    )

    game_view = GameView(
        screen,
        world,
    )

    statistics_view = StatisticsView(
        screen,
        statistics,
        world,
    )

    # Initial glider
    glider = [
        (10, 10),
        (11, 11),
        (9, 12),
        (10, 12),
        (11, 12),
    ]

    for x, y in glider:

        creature = Creature()

        world.set_creature(
            x,
            y,
            creature,
        )

        statistics.record_birth(
            creature
        )

    running = True
    paused = False

    generation_timer = 0

    while running:

        delta_time = clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse_x, mouse_y = event.pos

                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE

                if (
                    0 <= grid_x < world.width
                    and 0 <= grid_y < world.height
                ):

                    if world.is_alive(
                        grid_x,
                        grid_y,
                    ):

                        creature = world.get_creature(
                            grid_x,
                            grid_y,
                        )

                        statistics.record_death(
                            creature
                        )

                        world.set_creature(
                            grid_x,
                            grid_y,
                            None,
                        )

                    else:

                        creature = Creature()

                        world.set_creature(
                            grid_x,
                            grid_y,
                            creature,
                        )

                        statistics.record_birth(
                            creature
                        )

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:

            generation_timer += delta_time

            generation_interval = (
                1000 / GENERATIONS_PER_SECOND
            )

            if generation_timer >= generation_interval:

                simulation.update()

                statistics.update(
                    world,
                    generation_interval,
                )

                generation_timer = 0

        game_view.draw()

        statistics_view.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()