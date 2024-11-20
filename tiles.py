import pygame


class Tile:
    def __init__(self, x: float, y: float, size: float, colour: tuple[int, int, int]) -> None:
        self.pos = pygame.Vector2(x, y)
        self.image = pygame.Surface((size, size))
        self.image.fill(colour)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.pos)

    # used for determining unique instances for use in sets
    def __hash__(self) -> int:
        return hash((self.pos.x, self.pos.y))

    def __eq__(self, other) -> bool:
        return self.pos == other.pos


class WallTile(Tile):
    def __init__(self, x: float, y: float, size: float) -> None:
        super().__init__(x, y, size, (100, 100, 100))


class LavaTile(Tile):
    def __init__(self, x: float, y: float, size: float) -> None:
        super().__init__(x, y, size, (200, 50, 50))


tiles = tuple(Tile.__subclasses__())

if __name__ == "__main__":
    print(tiles == (WallTile, LavaTile))
