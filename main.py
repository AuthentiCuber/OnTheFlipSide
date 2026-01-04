import pygame

import scenes
from player import Player
from settings import Settings


class Game:
    def __init__(self) -> None:
        self.settings = Settings(
            resolution=(1280, 720), max_fps=240, fullscreen=False
        )
        self.screen = self.settings.screen
        self.subscreen = pygame.Surface((1920, 1080))
        self.dt = 0.0
        self.clock = pygame.Clock()
        self.running = True

        self.player = Player()
        self.scene: scenes.Scene = scenes.Level1(self.player)

    def loop(self) -> None:
        self.dt = self.clock.tick_busy_loop(self.settings.max_fps) / 1000

        result = self.scene.timestep(self.dt, self.subscreen)

        match result:
            case scenes.ReturnCode.EXIT:
                self.running = False
                return
            case scenes.ReturnCode.RESET:
                self.scene.reset()

        # preserve 16:9 subscreen aspect ratio
        # while scaling to as big as will fit
        draw_resolution = pygame.Vector2()
        window_aspect_ratio = (
            self.settings.resolution[0] / self.settings.resolution[1]
        )
        if window_aspect_ratio < 16 / 9:
            draw_resolution.update(
                self.settings.resolution[0],
                self.settings.resolution[0] * (9 / 16),
            )
        else:
            draw_resolution.update(
                self.settings.resolution[1] * (16 / 9),
                self.settings.resolution[1],
            )

        scaled_subscreen = pygame.transform.scale(
            self.subscreen, draw_resolution
        )
        # then draw scaled subscreen centered
        self.screen.blit(
            scaled_subscreen,
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
