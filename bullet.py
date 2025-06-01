from game import Entity
from objloader import Object
from OpenGL.GL import *

class Bullet(Entity):
    def __init__(self, game, pos, direction, speed=10.0, max_distance=20.0):
        self.object = Object("./assets/coin.obj", "./assets/texture.png", flip_texture=False)
        super().__init__(game, "bullet", self.object)
        self.speed = speed
        self.direction = direction
        self.forward_offset = 1.0
        self.position = pos + direction * self.forward_offset
        self.distance_traveled = 0.0
        self.max_distance = max_distance

    def update(self, delta_time: float):
        self.position += self.direction * self.speed * delta_time
        self.distance_traveled += self.speed * delta_time
        if self.distance_traveled > self.max_distance:
            self.game.remove_entity(self)