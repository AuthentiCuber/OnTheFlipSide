from enum import Enum, auto

import pygame

import tiles
from settings import Settings


class EditorMode(Enum):
    DELETE = auto()
    PLACE = auto()


class Game:
    def __init__(self) -> None:
        self.settings = Settings(max_fps=240)
        self.screen = self.settings.screen
        self.subscreen = pygame.Surface((1920, 1080))
        self.clock = pygame.Clock()
        self.dt = 0.0
        self.running = True

        self.grid_cell_size = 120
        self.grid_dimensions = (17, 10)

        self.level: pygame.sprite.Group[tiles.Tile] = pygame.sprite.Group()
        self.current_tile_type: type[tiles.Tile] = tiles.WallTile

        self.mode = EditorMode.PLACE

    def scene(self, dt: float) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.running = False
                return
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_F1:
                        tiles.save_level(self.level, "levels/level1")
                    case pygame.K_F2:
                        self.level = tiles.load_level("levels/level1")
                    case pygame.K_DELETE:
                        self.mode = (
                            EditorMode.DELETE
                            if self.mode == EditorMode.PLACE
                            else EditorMode.PLACE
                        )

        self.subscreen.fill((10, 200, 80))
        self.draw_grid()
        self.handle_place()
        self.draw_tiles()

    def draw_grid(self) -> None:
        for x in range(self.grid_dimensions[0]):
            pygame.draw.line(
                self.subscreen,
                "black",
                (x * self.grid_cell_size, 0),
                (
                    x * self.grid_cell_size,
                    self.grid_cell_size * (self.grid_dimensions[1] - 1),
                ),
            )
        for y in range(self.grid_dimensions[1]):
            pygame.draw.line(
                self.subscreen,
                "black",
                (0, y * self.grid_cell_size),
                (
                    self.grid_cell_size * (self.grid_dimensions[0] - 1),
                    y * self.grid_cell_size,
                ),
            )

    def draw_tiles(self) -> None:
        self.level.draw(self.subscreen)

    def handle_place(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.current_tile_type = tiles.WallTile
        elif keys[pygame.K_2]:
            self.current_tile_type = tiles.LavaTile
        elif keys[pygame.K_3]:
            self.current_tile_type = tiles.StartPos

        mouse_buttons = pygame.mouse.get_pressed()
        lmb = mouse_buttons[0]
        rmb = mouse_buttons[2]
        if not (lmb or rmb):
            return

        mouse_pos = pygame.mouse.get_pos()

        mouse_pos_in_window = pygame.Vector2(
            mouse_pos[0] * self.subscreen.width / self.screen.width,
            mouse_pos[1] * self.subscreen.height / self.screen.height,
        )
        cell_x = mouse_pos_in_window.x // self.grid_cell_size
        cell_y = mouse_pos_in_window.y // self.grid_cell_size
        actual_x = cell_x * self.grid_cell_size
        actual_y = cell_y * self.grid_cell_size

        tile = tiles.create_tile(
            self.current_tile_type, actual_x, actual_y, self.grid_cell_size
        )
        if lmb:
            match self.mode:
                case EditorMode.PLACE:
                    self.level.add(tile)
                case EditorMode.DELETE:
                    for existing_tile in self.level:
                        if existing_tile.pos == pygame.Vector2(
                            actual_x, actual_y
                        ):
                            self.level.remove(existing_tile)

    def loop(self) -> None:
        self.dt = self.clock.tick_busy_loop(self.settings.max_fps) / 1000

        self.scene(self.dt)

        pygame.transform.scale(
            self.subscreen, self.settings.resolution, self.screen
        )
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    while game.running:
        game.loop()
    pygame.quit()
