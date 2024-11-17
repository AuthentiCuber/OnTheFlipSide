import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, tile_size: float):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill("gray30")
        self.rect = self.image.get_rect(topleft=(x, y))


class Hazard(Tile):
    def __init__(self, x: float, y: float, tile_size: float):
        super().__init__(x, y, tile_size)
        self.image.fill("red")


class End(Tile):
    def __init__(self, x: float, y: float, tile_size: float):
        super().__init__(x, y, tile_size)
        self.image.fill("yellow")


# List of possible tiles
all_tiles = Tile.__subclasses__()
all_tiles.insert(0, Tile)


def loadlevel(path: str, tile_size: float) -> pygame.sprite.Group:
    with open(path, "r") as file:
        tiles = pygame.sprite.Group()
        x = 0
        y = 0
        for line in file.readlines():
            for character in line.strip():
                if character.isnumeric():
                    tile_type = int(character)
                    tile = all_tiles[tile_type-1](x, y, tile_size)

                    tiles.add(tile)

                x += tile_size
            y += tile_size
            x = 0
        return tiles
