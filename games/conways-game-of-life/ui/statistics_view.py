import pygame

from game.config import CREATURE_COLORS


class StatisticsView:
    def __init__(self, screen, statistics, world):
        self.screen = screen
        self.statistics = statistics
        self.world = world

        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 23)
        self.title_font = pygame.font.Font(None, 34)

        self.panel_x = 1020
        self.panel_width = 360

    def draw(self):
        self.draw_background()
        self.draw_title()
        self.draw_statistics()
        self.draw_creatures()

    def draw_background(self):
        pygame.draw.rect(
            self.screen,
            (30, 30, 30),
            (
                self.panel_x,
                0,
                self.panel_width,
                800,
            ),
        )

    def draw_title(self):
        title = self.title_font.render(
            "STATISTICS",
            True,
            (240, 240, 240),
        )

        self.screen.blit(
            title,
            (self.panel_x + 20, 20),
        )

    def draw_statistics(self):

        population = self.statistics.get_population(
            self.world
        )

        population_change = (
            self.statistics.get_population_change(
                self.world
            )
        )

        average_age = (
            self.statistics.get_average_age(
                self.world
            )
        )

        elapsed_seconds = (
            self.statistics.simulation_time / 1000
        )

        minutes = int(elapsed_seconds // 60)
        seconds = int(elapsed_seconds % 60)

        statistics = [
            ("Population", population),
            ("Generation", self.statistics.generation),
            ("Births", self.statistics.total_births),
            ("Deaths", self.statistics.total_deaths),
            ("Peak Population", self.statistics.peak_population),
            ("Population Change", population_change),
            ("Average Age", f"{average_age:.1f}"),
            (
                "Elapsed Time",
                f"{minutes:02d}:{seconds:02d}"
            ),
        ]

        y = 75

        for label, value in statistics:

            text = self.font.render(
                f"{label}: {value}",
                True,
                (220, 220, 220),
            )

            self.screen.blit(
                text,
                (self.panel_x + 20, y),
            )

            y += 30

    def draw_creatures(self):

        title = self.font.render(
            "CREATURES",
            True,
            (240, 240, 240),
        )

        self.screen.blit(
            title,
            (self.panel_x + 20, 330),
        )

        population = self.statistics.get_population(
            self.world
        )

        population_by_type = (
            self.statistics.get_population_by_type(
                self.world
            )
        )

        y = 365

        for creature_type, count in population_by_type.items():

            if population > 0:
                percentage = (count / population) * 100
            else:
                percentage = 0

            color = CREATURE_COLORS.get(
                creature_type,
                (200, 200, 200),
            )

            pygame.draw.rect(
                self.screen,
                color,
                (
                    self.panel_x + 20,
                    y + 3,
                    15,
                    15,
                ),
            )

            text = self.small_font.render(
                f"{creature_type}: "
                f"{count} ({percentage:.1f}%)",
                True,
                (220, 220, 220),
            )

            self.screen.blit(
                text,
                (self.panel_x + 45, y),
            )

            y += 28