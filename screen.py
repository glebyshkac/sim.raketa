import pygame

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("Arial", 16)
        self.background = None
        self.house_image = None
        self.load_background()
        self.load_house_image()

    def load_background(self):
        try:
            self.background = pygame.image.load('assets/city_map.jpg').convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except:
            print("city_map.jpg не знайдено — чорний фон")
            self.background = None

    def load_house_image(self):
        try:
            self.house_image = pygame.image.load('assets/house.jpg').convert_alpha()
            self.house_image = pygame.transform.scale(self.house_image, (20, 20))
        except:
            print("house.jpg не знайдено — малюємо вручну")
            self.house_image = None

    def draw_background(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

    def draw_launchers(self, launchers):
        for launcher in launchers:
            pygame.draw.circle(self.screen, (0, 0, 255), launcher.position, 10)
            text = self.font.render(str(len(launcher.rockets)), True, (255, 255, 255))
            self.screen.blit(text, (launcher.position[0] - 5, launcher.position[1] - 25))

    def draw_targets(self, targets):
        for x, y in targets:
            # корпус будинку
            pygame.draw.rect(self.screen, (150, 75, 0), (x - 15, y - 10, 30, 30))
            # дах
            pygame.draw.polygon(self.screen, (200, 0, 0), [(x - 20, y - 10), (x + 20, y - 10), (x, y - 35)])
            # вікна
            pygame.draw.rect(self.screen, (0, 191, 255), (x - 10, y, 8, 8))
            pygame.draw.rect(self.screen, (0, 191, 255), (x + 2, y, 8, 8))

    def draw_rockets(self, rockets):
        for rocket in rockets:
            if rocket.is_active():
                x, y, z = rocket.get_position()

                # корпус (горизонтальний прямокутник, летить ліворуч)
                pygame.draw.rect(self.screen, (200, 200, 200), (x - 15, y - 4, 30, 8))

                # ніс (трикутник зліва)
                pygame.draw.polygon(self.screen, (255, 0, 0), [(x - 20, y), (x - 15, y - 4), (x - 15, y + 4)])

                # крила (зверху і знизу, ближче до хвоста)
                pygame.draw.polygon(self.screen, (100, 100, 100), [(x + 10, y - 6), (x, y - 4), (x + 15, y - 4)])
                pygame.draw.polygon(self.screen, (100, 100, 100), [(x + 10, y + 6), (x, y + 4), (x + 15, y + 4)])

            elif rocket.destroyed and rocket.explosion_time and pygame.time.get_ticks() - rocket.explosion_time * 1000 < 500:
                pygame.draw.circle(self.screen, (255, 100, 0), rocket.explosion_pos, 20)
                pygame.draw.circle(self.screen, (255, 255, 0), rocket.explosion_pos, 10)

    def draw_air_defenses(self, air_defenses):
        for ad in air_defenses:
            pygame.draw.circle(self.screen, (0, 255, 0), ad.position, 15)

    def flip(self):
        pygame.display.flip()
