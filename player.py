import pygame
from pygame.locals import *
from math import exp


def expDecay(decay: float, dt: float) -> float:
    return exp(-decay * dt)


class Player:
    def __init__(self):
        self.movement = pygame.Vector2()
        self.vel = pygame.Vector2()
        self.max_vel = 1000
        self.gravity = pygame.Vector2(0, 1)
        self.gravity_strength = 3000
        self.friction = 4
        self.image = pygame.Surface((60, 60))
        self.image.fill("dodgerblue4")
        self.rect = self.image.get_frect(topleft=(240, 120))

    def update(self, dt: float):
        keys = pygame.key.get_pressed()

        up = keys[K_UP] or keys[K_w]
        down = keys[K_DOWN] or keys[K_s]
        left = keys[K_LEFT] or keys[K_a]
        right = keys[K_RIGHT] or keys[K_d]

        if up:
            self.gravity.update(0, -1)
        elif down:
            self.gravity.update(0, 1)
        elif left:
            self.gravity.update(-1, 0)
        elif right:
            self.gravity.update(1, 0)

        if self.gravity.x != 0:
            self.vel.y *= expDecay(self.friction, dt)
        if self.gravity.y != 0:
            self.vel.x *= expDecay(self.friction, dt)

        self.vel += self.gravity * self.gravity_strength * dt
        # cap speed
        if self.vel.length() > self.max_vel:
            self.vel.scale_to_length(self.max_vel)

        self.movement.update(self.vel * dt)

    def move(self):
        self.rect.x += self.movement.x
        self.rect.y += self.movement.y

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def collide(self, group: pygame.sprite.Group):
        for sprite in group:
            # collide x
            if sprite.rect.colliderect(self.rect.x + self.movement.x, self.rect.y, self.rect.width, self.rect.height):
                if self.movement.x > 0:
                    self.movement.x = sprite.rect.left - self.rect.right
                elif self.movement.x < 0:
                    self.movement.x = sprite.rect.right - self.rect.left
                self.vel.x = 0
            # collide y
            if sprite.rect.colliderect(self.rect.x, self.rect.y + self.movement.y, self.rect.width, self.rect.height):
                if self.movement.y < 0:
                    self.movement.y = sprite.rect.bottom - self.rect.top
                elif self.movement.y > 0:
                    self.movement.y = sprite.rect.top - self.rect.bottom
                self.vel.y = 0
