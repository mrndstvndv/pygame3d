import glm
from OpenGL.GL import *
from dataclasses import dataclass, field
from objloader import Object


@dataclass
class GameContext:
    shader_program: any
    entities: list["Entity"] = field(default_factory=list)

    def remove_entity(self, entity: "Entity"):
        self.entities.remove(entity)

    def __post_init__(self):
        # Get uniform locations once during initialization
        self.pos_loc = glGetUniformLocation(self.shader_program, "pos")
        self.model_loc = glGetUniformLocation(self.shader_program, "model")

class Entity:
    def __init__(
        self,
        game: GameContext,
        name: str,
        obj: Object,
    ):
        self.name = name
        self.game = game
        self.rotation = 0.0
        self.obj: Object = obj
        self.position = glm.vec3(0.0, 0.0, 0.0)

    def update(self, delta_time: float):
        pass

    def draw(self):
        wall_model = glm.mat4(1.0)

        wall_model = glm.translate(
            wall_model, glm.vec3(self.position.x, self.position.y, self.position.z)
        )

        wall_model = glm.rotate(
            wall_model, glm.radians(self.rotation), glm.vec3(0, 1, 0)
        )

        # Set the model matrix uniform for this specific wall
        glUniformMatrix4fv(
            self.game.model_loc, 1, GL_FALSE, glm.value_ptr(wall_model)
        )

        self.obj.draw()