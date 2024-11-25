import pygame
from settings import Settings
from player import Player
import tiles


class Game:
    def __init__(self) -> None:
        self.settings = Settings()
        self.screen = self.settings.screen
        self.subscreen = pygame.Surface((1920, 1080))
        self.dt: float = 0
        self.clock = pygame.Clock()
        self.running = True
        self.scene = self.level1

        self.player = Player()
        self.tiles = tiles.load_level()

    def level1(self, dt: float) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.running = False
                return

        self.subscreen.fill((150, 150, 150))

        self.tiles.draw(self.subscreen)

        self.player.update(dt)
        self.player.collide(self.tiles)
        self.player.move()
        self.player.draw(self.subscreen)

    def loop(self) -> None:
        self.dt = self.clock.tick_busy_loop(self.settings.max_fps) / 1000

        self.scene(self.dt)

        pygame.transform.scale(self.subscreen, self.settings.resolution, self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    while game.running:
        game.loop()
    pygame.quit()
