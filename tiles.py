import pickle
from typing import Any, Callable, ParamSpec

import pygame
from pygame.typing import ColorLike


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, x: float, y: float, size: float, colour: ColorLike
    ) -> None:
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.size = size
        self.collideable = True
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(colour)
        self.rect = self.image.get_frect(topleft=self.pos)


class WallTile(Tile):
    def __init__(self, x: float, y: float, size: float) -> None:
        super().__init__(x, y, size, (100, 100, 100))


class LavaTile(Tile):
    def __init__(self, x: float, y: float, size: float) -> None:
        super().__init__(x, y, size, (200, 50, 50))


class StartPos(Tile):
    def __init__(self, x: float, y: float, size: float) -> None:
        super().__init__(x, y, size, (200, 200, 200))
        self.collideable = False


tiles = tuple(Tile.__subclasses__())


P = ParamSpec("P")


def create_tile(
    tile_type: Callable[P, Tile], *args: P.args, **kwargs: P.kwargs
) -> Tile:
    return tile_type(*args, **kwargs)


def level_data_to_tiles(
    level_data: list[dict[str, Any]],
) -> pygame.sprite.Group[Tile]:
    return pygame.sprite.Group(
        [
            create_tile(
                tiles[tile["type"]], tile["pos"].x, tile["pos"].y, tile["size"]
            )
            for tile in level_data
        ]
    )


def tiles_to_level_data(
    tile_list: pygame.sprite.Group[Tile],
) -> list[dict[str, Any]]:
    level_data = []
    for tile in tile_list.sprites():
        tile_dict = {
            "type": tiles.index(type(tile)),
            "pos": tile.pos,
            "size": tile.size,
        }

        level_data.append(tile_dict)
    return level_data


def save_level(tile_list: pygame.sprite.Group[Tile]) -> None:
    with open("level", "wb") as file:
        pickle.dump(tiles_to_level_data(tile_list), file)


def load_level() -> pygame.sprite.Group[Tile]:
    with open("level", "rb") as file:
        return level_data_to_tiles(pickle.load(file))


if __name__ == "__main__":
    level_tiles = pygame.sprite.Group(WallTile(1, 1, 1), LavaTile(2, 2, 2))
    level_data = tiles_to_level_data(level_tiles)
    print(level_data)
    print(level_data_to_tiles(level_data).sprites())
