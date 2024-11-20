import pygame
from settings import Settings
import tiles


class Game:
    def __init__(self) -> None:
        self.settings = Settings(max_fps=240)
        self.screen = self.settings.screen
        self.clock = pygame.Clock()
        self.dt = 0
        self.running = True

        self.grid_cell_size = 70
        self.grid_dimensions = (16, 9)

        self.level: dict[tuple[float, float], tiles.Tile] = {}
        self.current_tile_type = 0

    def scene(self, dt: float) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                return

        self.screen.fill((10, 200, 80))
        self.draw_grid()
        self.handle_place()
        self.draw_tiles()

    def draw_grid(self) -> None:
        for x in range(self.grid_dimensions[0]):
            pygame.draw.line(self.screen, "black", (x*self.grid_cell_size, 0),
                             (x*self.grid_cell_size, self.grid_cell_size * (self.grid_dimensions[1] - 1)))
        for y in range(self.grid_dimensions[1]):
            pygame.draw.line(self.screen, "black", (0, y*self.grid_cell_size),
                             (self.grid_cell_size * (self.grid_dimensions[0] - 1), y*self.grid_cell_size))

    def draw_tiles(self) -> None:
        for tile in self.level.values():
            tile.draw(self.screen)

    def handle_place(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.current_tile_type = 0
        elif keys[pygame.K_2]:
            self.current_tile_type = 1

        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        lmb = mouse_buttons[0]
        rmb = mouse_buttons[2]
        if not (lmb or rmb):
            return
        cell_x = mouse_pos[0] // self.grid_cell_size
        cell_y = mouse_pos[1] // self.grid_cell_size
        actual_x = cell_x * self.grid_cell_size
        actual_y = cell_y * self.grid_cell_size
        if lmb:
            self.level[(actual_x, actual_y)] = tiles.tiles[self.current_tile_type](
                actual_x, actual_y, self.grid_cell_size)
        elif rmb:
            if (actual_x, actual_y) in self.level.keys():
                del self.level[(actual_x, actual_y)]

    def loop(self) -> None:
        self.dt = self.clock.tick_busy_loop(self.settings.max_fps) / 1000

        self.scene(self.dt)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    while game.running:
        game.loop()
    pygame.quit()
