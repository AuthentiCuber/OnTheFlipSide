from enum import Enum, auto
from typing import Protocol, runtime_checkable

import pygame

import player
import tiles


class ReturnCode(Enum):
    CONTINUE = auto()
    EXIT = auto()
    RESET = auto()


class Scene(Protocol):
    def timestep(self, dt: float, screen: pygame.Surface) -> ReturnCode: ...

    def reset(self) -> None: ...


@runtime_checkable
class Level(Scene, Protocol):
    tiles: pygame.sprite.Group[tiles.Tile]
    player: player.Player


class Level1:
    def __init__(self, player: player.Player) -> None:
        self.tiles = tiles.load_level("levels/level1")
        self.player = player
        self.reset()

    def timestep(self, dt: float, screen: pygame.Surface) -> ReturnCode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                return ReturnCode.EXIT

        screen.fill((150, 150, 150))

        self.tiles.draw(screen)

        self.player.update(dt)

        for tile in self.tiles:
            if not tile.collideable:
                continue

            result = self.player.collide(tile)

            match result:
                case player.Collision.DAMAGE:
                    self.reset()
                    break

        self.player.move()
        self.player.draw(screen)

        return ReturnCode.CONTINUE

    def reset(self) -> None:
        startpos_tiles = [
            tile for tile in self.tiles if isinstance(tile, tiles.StartPos)
        ]

        if len(startpos_tiles) != 1:
            raise RuntimeError("There must only be one startpos in level1")
        startpos = startpos_tiles[0]

        half_grid_size = startpos.size // 2
        self.player.rect.center = (
            startpos.pos.x + half_grid_size,
            startpos.pos.y + half_grid_size,
        )
        self.player.gravity.update(0, 1)
        self.player.vel = pygame.Vector2(0, 0)


if __name__ == "__main__":
    p1 = player.Player()
    level: Scene = Level1(p1)
    _level: Level = Level1(p1)
