"""pygame compatible vector2 conveniences"""

from pygame import Vector2


def ZERO() -> Vector2:
    return Vector2()


def UP() -> Vector2:
    return Vector2(0, -1)


def DOWN() -> Vector2:
    return Vector2(0, 1)


def LEFT() -> Vector2:
    return Vector2(-1, 0)


def RIGHT() -> Vector2:
    return Vector2(1, 0)
