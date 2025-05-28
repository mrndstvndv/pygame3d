import glm
from OpenGL.GL import *
from dataclasses import dataclass
from objloader import Object


@dataclass
class GameContext:
    shader_program: any

    def __post_init__(self):
        # Get uniform locations once during initialization
        self.pos_loc = glGetUniformLocation(self.shader_program, "pos")


class Entity:
    def __init__(
        self,
        game: GameContext,
        name: str,
        obj: Object,
    ):
        self.name = name
        self.game = game
        self.obj: Object = obj
        self.position = glm.vec3(0.0, 0.0, 0.0)

    def update(self, delta_time: float):
        pass

    def draw(self):
        glUniform3f(self.game.pos_loc, self.position.x, self.position.y, self.position.z)
        self.obj.draw()
