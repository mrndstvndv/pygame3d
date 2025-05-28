# import os
# os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

import os

from objloader import Object
from game import GameContext, Entity

if os.environ.get("XDG_SESSION_TYPE") == "wayland":
    os.environ["SDL_VIDEODRIVER"] = "wayland"


import pygame
from pygame.locals import *
from OpenGL.GL import *
from pyglm import glm
from shaders import create_shader_program

objects = []


def init_pygame_opengl():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)

    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
    )

    # Create a window with OpenGL context
    width, height = 800, 600
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL with Shaders")

def main():
    init_pygame_opengl()

    # Create and use shader program
    shader_program = create_shader_program()
    if not shader_program:
        print("Failed to create shader program")
        return

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)

    game = GameContext(shader_program)

    bench = Entity(game, "bench", Object("./assets/bench.obj", "./assets/bench.png"))
    bullet = Entity(game, "bullet", Object("./assets/coin.obj", "./assets/texture.png"))
    wall = Entity(game, "wall", Object("./assets/wall.obj", "./assets/wall.png"))


    # Get uniform locations
    model_loc = glGetUniformLocation(shader_program, "model")
    view_loc = glGetUniformLocation(shader_program, "view")
    proj_loc = glGetUniformLocation(shader_program, "projection")
    light_pos_loc = glGetUniformLocation(shader_program, "lightPos")
    light_color_loc = glGetUniformLocation(shader_program, "lightColor")
    view_pos_loc = glGetUniformLocation(shader_program, "viewPos")

    # Set light properties
    light_pos = glm.vec3(2.0, 2.0, 2.0)  # Light position
    light_color = glm.vec3(1.0, 1.0, 1.0)  # White light

    # Create transformation matrices
    projection = glm.perspective(glm.radians(45.0), 800.0 / 600.0, 0.1, 100.0)

    # Camera position and orientation
    camera_pos = glm.vec3(0.0, 0.0, 5.0)
    camera_front = glm.vec3(0.0, 0.0, -1.0)  # Direction camera is looking
    camera_up = glm.vec3(0.0, 1.0, 0.0)
    camera_right = glm.normalize(glm.cross(camera_front, camera_up))

    # Camera speed and controls
    camera_speed = 0.2
    yaw = -90.0  # Initial yaw (facing -Z direction)
    pitch = 0.0

    rotation = 0.0
    clock = pygame.time.Clock()

    # Main loop
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        # print(camera_pos)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera_pos += camera_speed * camera_front
        if keys[pygame.K_s]:
            camera_pos -= camera_speed * camera_front
        if keys[pygame.K_a]:
            yaw -= camera_speed * 10.0
        if keys[pygame.K_d]:
            yaw += camera_speed * 10.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    objects.append((0.0, 1.0, 0.0))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_m:  # Toggle mouse look
                    mouse_look_enabled = not mouse_look_enabled
                    if mouse_look_enabled:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                    else:
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)

        # Limit pitch to avoid camera flipping
        if pitch > 89.0:
            pitch = 89.0
        if pitch < -89.0:
            pitch = -89.0

        # Calculate new front vector
        direction = glm.vec3()
        direction.x = glm.cos(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
        direction.y = glm.sin(glm.radians(pitch))
        direction.z = glm.sin(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
        camera_front = glm.normalize(direction)

        # Update right and up vectors
        camera_right = glm.normalize(glm.cross(camera_front, glm.vec3(0.0, 1.0, 0.0)))
        camera_up = glm.normalize(glm.cross(camera_right, camera_front))

        # Update view matrix
        view = glm.lookAt(camera_pos, camera_pos + camera_front, camera_up)

        print(camera_front, end="\n")

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.2, 0.3, 0.3, 1.0)

        # Use shader program
        glUseProgram(shader_program)

        # Update rotation for the model
        # rotation += 0.01 * dt * 60
        model = glm.rotate(glm.mat4(1.0), rotation, glm.vec3(0, 1, 0))

        # Set uniforms
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))

        # Set lighting uniforms
        glUniform3f(light_pos_loc, light_pos.x, light_pos.y, light_pos.z)
        glUniform3f(light_color_loc, light_color.x, light_color.y, light_color.z)
        glUniform3f(view_pos_loc, camera_pos.x, camera_pos.y, camera_pos.z)

        bench.draw()
        bullet.draw()
        wall.draw()

        # Swap buffers
        pygame.display.flip()

    # Cleanup
    glDeleteProgram(shader_program)
    pygame.quit()


if __name__ == "__main__":
    main()
