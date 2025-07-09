import pygame

import tiles
from player import Player
from settings import Settings


class Game:
    def __init__(self) -> None:
        self.settings = Settings(
            resolution=(1280, 720), max_fps=240, fullscreen=False
        )
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

        draw_resolution = pygame.Vector2()
        window_aspect_ratio = (
            self.settings.resolution[0] / self.settings.resolution[1]
        )
        subscreen_aspect_ratio = (
            self.subscreen.get_size()[0] / self.subscreen.get_size()[1]
        )
        if subscreen_aspect_ratio > window_aspect_ratio:
            draw_resolution.update(
                self.settings.resolution[0],
                self.settings.resolution[0] * (9 / 16),
            )
        else:
            draw_resolution.update(
                self.settings.resolution[1] * (16 / 9),
                self.settings.resolution[1],
            )

        self.screen.blit(
            pygame.transform.scale(self.subscreen, draw_resolution),
            (
                (self.settings.resolution[0] - draw_resolution.x) / 2,
                (self.settings.resolution[1] - draw_resolution.y) / 2,
            ),
        )

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    while game.running:
        game.loop()
    pygame.quit()
