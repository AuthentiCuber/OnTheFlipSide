import pygame
from settings import Settings


class Game:
    def __init__(self) -> None:
        self.settings = Settings(max_fps=240)
        self.screen = self.settings.screen
        self.clock = pygame.Clock()
        self.dt = 0
        self.running = True

        self.scroll_speed = 1000
        self.scroll = pygame.Vector2(50, 50)

        self.grid_square_size = 70
        self.grid_size = (16, 9)

    def scene(self, dt: float) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                return

        self.screen.fill((10, 200, 80))
        self.handle_scroll(dt)
        self.draw_grid()

    def handle_scroll(self, dt) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.scroll.y += self.scroll_speed * dt
        if keys[pygame.K_DOWN]:
            self.scroll.y -= self.scroll_speed * dt
        if keys[pygame.K_LEFT]:
            self.scroll.x += self.scroll_speed * dt
        if keys[pygame.K_RIGHT]:
            self.scroll.x -= self.scroll_speed * dt

    def draw_grid(self) -> None:
        for x in range(self.grid_size[0]):
            pygame.draw.line(self.screen, "black", (x*self.grid_square_size + self.scroll.x, self.scroll.y),
                             (x*self.grid_square_size + self.scroll.x, self.grid_square_size * (self.grid_size[1] - 1) + self.scroll.y))
        for y in range(self.grid_size[1]):
            pygame.draw.line(self.screen, "black", (self.scroll.x, y*self.grid_square_size + self.scroll.y),
                             (self.grid_square_size * (self.grid_size[0] - 1) + self.scroll.x, y*self.grid_square_size + self.scroll.y))

    def loop(self) -> None:
        self.dt = self.clock.tick_busy_loop(self.settings.max_fps) / 1000

        self.scene(self.dt)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    while game.running:
        game.loop()
    pygame.quit()
