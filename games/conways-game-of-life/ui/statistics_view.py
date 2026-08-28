import pygame

from game.config import CREATURE_COLORS


class StatisticsView:
    def __init__(self, screen, statistics, world):
        self.screen = screen
        self.statistics = statistics
        self.world = world

        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 34)

        self.panel_x = 1020
        self.panel_width = 360

    def draw(self):
        self.draw_background()
        self.draw_title()
        self.draw_statistics()
        self.draw_creatures()
        self.draw_pie_chart()
        self.draw_population_graph()

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
            ("Elapsed Time", f"{minutes:02d}:{seconds:02d}"),
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

    # ---------------------------------------------------------
    # PIE CHART
    # ---------------------------------------------------------

    def draw_pie_chart(self):

        population = self.statistics.get_population(
            self.world
        )

        population_by_type = (
            self.statistics.get_population_by_type(
                self.world
            )
        )

        if population == 0:
            return

        center = (
            self.panel_x + 105,
            495,
        )

        radius = 70

        start_angle = 0

        for creature_type, count in population_by_type.items():

            percentage = count / population
            angle = percentage * 360

            color = CREATURE_COLORS.get(
                creature_type,
                (200, 200, 200),
            )

            self.draw_pie_slice(
                center,
                radius,
                start_angle,
                start_angle + angle,
                color,
            )

            start_angle += angle

    def draw_pie_slice(
        self,
        center,
        radius,
        start_angle,
        end_angle,
        color,
    ):

        import math

        points = [center]

        steps = max(
            2,
            int(abs(end_angle - start_angle) / 3),
        )

        for i in range(steps + 1):

            angle = start_angle + (
                (end_angle - start_angle)
                * i
                / steps
            )

            radians = math.radians(angle)

            x = center[0] + math.cos(radians) * radius
            y = center[1] + math.sin(radians) * radius

            points.append((x, y))

        pygame.draw.polygon(
            self.screen,
            color,
            points,
        )

    # ---------------------------------------------------------
    # POPULATION HISTORY GRAPH
    # ---------------------------------------------------------

    def draw_population_graph(self):

        title = self.small_font.render(
            "POPULATION HISTORY",
            True,
            (240, 240, 240),
        )

        self.screen.blit(
            title,
            (self.panel_x + 20, 585),
        )

        history = self.statistics.population_history

        if len(history) < 2:
            return

        graph_x = self.panel_x + 20
        graph_y = 615

        graph_width = 320
        graph_height = 150

        # Background
        pygame.draw.rect(
            self.screen,
            (20, 20, 20),
            (
                graph_x,
                graph_y,
                graph_width,
                graph_height,
            ),
        )

        # Border
        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            (
                graph_x,
                graph_y,
                graph_width,
                graph_height,
            ),
            1,
        )

        max_population = max(history)

        if max_population == 0:
            return

        # Only display the most recent values if the
        # simulation has been running for a long time.
        visible_history = history[-100:]

        points = []

        for i, population in enumerate(
            visible_history
        ):

            if len(visible_history) == 1:
                x = graph_x
            else:
                x = (
                    graph_x
                    + (
                        i
                        / (len(visible_history) - 1)
                    )
                    * graph_width
                )

            y = (
                graph_y
                + graph_height
                - (
                    population
                    / max_population
                )
                * graph_height
            )

            points.append((x, y))

        if len(points) >= 2:

            pygame.draw.lines(
                self.screen,
                (100, 220, 100),
                False,
                points,
                2,
            )

        # Maximum population label
        max_text = self.small_font.render(
            str(max_population),
            True,
            (160, 160, 160),
        )

        self.screen.blit(
            max_text,
            (
                graph_x + 5,
                graph_y + 5,
            ),
        )

        # Zero label
        zero_text = self.small_font.render(
            "0",
            True,
            (160, 160, 160),
        )

        self.screen.blit(
            zero_text,
            (
                graph_x + 5,
                graph_y + graph_height - 20,
            ),
        )

        # Generation label
        generation_text = self.small_font.render(
            f"Gen {self.statistics.generation}",
            True,
            (160, 160, 160),
        )

        self.screen.blit(
            generation_text,
            (
                graph_x + graph_width - 75,
                graph_y + graph_height + 3,
            ),
        )