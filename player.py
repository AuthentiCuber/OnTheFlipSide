from enum import Enum, auto
from math import exp
from typing import cast

import pygame

import tiles
import Vector2


def expDecay(decay: float, dt: float) -> float:
    return exp(-decay * dt)


class Collision(Enum):
    DAMAGE = auto()
    NORMAL = auto()
    FINISH = auto()
    NONE = auto()


class Player:
    def __init__(self) -> None:
        self.movement = Vector2.ZERO()
        self.vel = Vector2.ZERO()
        self.max_vel = 1000
        self.gravity = Vector2.DOWN()
        self.gravity_strength = 3000
        self.friction = 6
        self.image = pygame.Surface((60, 60))
        self.image.fill("dodgerblue4")
        self.rect = self.image.get_frect()

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        up = keys[pygame.K_UP] or keys[pygame.K_w]
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        if up:
            self.gravity = Vector2.UP()
        elif down:
            self.gravity = Vector2.DOWN()
        elif left:
            self.gravity = Vector2.LEFT()
        elif right:
            self.gravity = Vector2.RIGHT()

        if self.gravity.x != 0:
            self.vel.y *= expDecay(self.friction, dt)
        if self.gravity.y != 0:
            self.vel.x *= expDecay(self.friction, dt)

        self.vel += self.gravity * self.gravity_strength * dt
        # cap speed
        self.vel.clamp_magnitude_ip(self.max_vel)

        self.movement = self.vel * dt

    def move(self) -> None:
        self.rect.x += self.movement.x
        self.rect.y += self.movement.y

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def collide(self, tile: tiles.Tile) -> Collision:
        # because pygame.sprite.Sprite.rect is Optional for some reason
        tile.rect = cast(pygame.FRect, tile.rect)

        collision = Collision.NONE

        # collide x
        if tile.rect.colliderect(
            self.rect.x + self.movement.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
        ):
            if self.movement.x > 0:
                self.movement.x = tile.rect.left - self.rect.right
            elif self.movement.x < 0:
                self.movement.x = tile.rect.right - self.rect.left
            self.vel.x = 0

            collision = Collision.NORMAL

        # collide y
        if tile.rect.colliderect(
            self.rect.x,
            self.rect.y + self.movement.y,
            self.rect.width,
            self.rect.height,
        ):
            if self.movement.y < 0:
                self.movement.y = tile.rect.bottom - self.rect.top
            elif self.movement.y > 0:
                self.movement.y = tile.rect.top - self.rect.bottom
            self.vel.y = 0
            collision = Collision.NORMAL

        if collision is not Collision.NONE and tile.does_damage:
            collision = Collision.DAMAGE

        if isinstance(tile, tiles.FinishTile):
            collision = Collision.FINISH

        return collision
