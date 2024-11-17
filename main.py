import pygame
from settings import Settings

from pathlib import Path

from player import Player
from levels import loadlevel


def get_relative_file(path: str) -> str:
    return str(Path(__file__).parent.resolve()) + path


class Game:
    def __init__(self) -> None:
        self.settings = Settings()
        self.screen = self.settings.screen
        self.subscreen = pygame.Surface((1920, 1080))
        self.dt = 0
        self.clock = pygame.Clock()
        self.running = True
        self.scene = self.level1

        self.player = Player()
        self.tiles = loadlevel(get_relative_file(
            "/level.txt"), 120)

    def level1(self, dt: float) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
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

        pygame.transform.scale(
            self.subscreen, self.settings.resolution, self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    while game.running:
        game.loop()
    pygame.quit()
