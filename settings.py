import pygame
from pygame.typing import IntPoint

pygame.init()


class Settings:
    def __init__(
        self,
        resolution: IntPoint = (0, 0),
        fullscreen: bool = True,
        monitor: int = 0,
        vsync: bool = False,
        max_fps: int = 0,
    ) -> None:
        self._monitor = monitor
        self._fullscreen = fullscreen
        self._vsync = vsync

        self._max_fps: int
        self.max_fps = max_fps

        self._resolution: IntPoint
        self.resolution = resolution

        self.screen: pygame.Surface
        self._update_display_mode()

    @property
    def monitor(self) -> int:
        """Which connected display to use. Zero indexed"""
        return self._monitor

    @monitor.setter
    def monitor(self, monitor: int) -> None:
        if monitor > (pygame.display.get_num_displays() - 1):
            raise IndexError("Invalid monitor number")

        self._monitor = monitor
        self._update_display_mode()

    @property
    def fullscreen(self) -> bool:
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value: bool) -> None:
        self._fullscreen = value
        self._update_display_mode()

    @property
    def resolution(self) -> IntPoint:
        return self.screen.get_size()

    @resolution.setter
    def resolution(self, dimensions: IntPoint) -> None:
        """The window resolution. Setting to (0, 0) will use native monitor resolution"""
        self._resolution = dimensions
        self._update_display_mode()

    @property
    def vsync(self) -> bool:
        return self._vsync

    @vsync.setter
    def vsync(self, value: bool) -> None:
        self._vsync = value
        self._update_display_mode()

    @property
    def max_fps(self) -> int:
        """Current fps limit. 0 means uncapped."""
        return self._max_fps

    @max_fps.setter
    def max_fps(self, value: int) -> None:
        self._max_fps = value

    def _update_display_mode(self) -> None:
        """Update the pygame.display mode"""
        display_flags = 0
        if self._fullscreen:
            display_flags |= pygame.FULLSCREEN

        self.screen = pygame.display.set_mode(
            self._resolution, display_flags, display=self._monitor
        )


if __name__ == "__main__":
    settings = Settings()
