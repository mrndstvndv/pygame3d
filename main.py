# import os
# os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

import os

from objloader import Object
from game import GameContext, Entity
from lighting import Light, LightManager

if os.environ.get("XDG_SESSION_TYPE") == "wayland":
    os.environ["SDL_VIDEODRIVER"] = "wayland"


import pygame
from pygame.locals import *
from OpenGL.GL import *
from pyglm import glm
from shaders import create_shader_program
from bullet import Bullet


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
    wall = Entity(game, "wall", Object("./assets/wall.obj", "./assets/wall.png"))

    # Get uniform locations
    model_loc = glGetUniformLocation(shader_program, "model")
    view_loc = glGetUniformLocation(shader_program, "view")
    proj_loc = glGetUniformLocation(shader_program, "projection")
    view_pos_loc = glGetUniformLocation(shader_program, "viewPos")

    # Initialize lighting system
    light_manager = LightManager(shader_program)

    # Add multiple light sources
    # Static light sources
    light_manager.add_light(
        Light(position=(5.0, 5.0, 5.0), color=(1.0, 1.0, 1.0), intensity=2.0)
    )  # Main overhead light
    light_manager.add_light(
        Light(position=(-3.0, 2.0, 3.0), color=(1.0, 0.8, 0.6), intensity=1.5)
    )  # Warm side light
    light_manager.add_light(
        Light(position=(0.0, -1.0, -5.0), color=(0.6, 0.8, 1.0), intensity=1.0)
    )  # Cool ground light

    # Dynamic light that will follow the camera (like a flashlight)
    flashlight_index = len(light_manager.lights)
    light_manager.add_light(
        Light(position=(0.0, 0.0, 0.0), color=(1.0, 1.0, 0.8), intensity=3.0)
    )

    print("=== Multiple Light Sources Demo ===")
    print("Controls:")
    print("WASD - Move camera")
    print("Arrow Keys - Look around")
    print("SPACE - Fire bullet")
    print("1 - Toggle overhead light")
    print("2 - Toggle side light")
    print("3 - Toggle ground light")
    print("4 - Toggle flashlight")
    print("C - Cycle flashlight color")
    print("ESC - Quit")
    print("=====================================\n")

    # Create transformation matrices
    projection = glm.perspective(glm.radians(45.0), 800.0 / 600.0, 0.1, 100.0)

    # Camera position and orientation
    camera_pos = glm.vec3(0.0, 0.0, 5.0)
    camera_front = glm.vec3(0.0, 0.0, -1.0)  # Direction camera is looking
    camera_up = glm.vec3(0.0, 1.0, 0.0)
    camera_right = glm.normalize(glm.cross(camera_front, camera_up))

    # Camera speed and controls
    camera_speed = 10
    yaw = -90.0  # Initial yaw (facing -Z direction)
    pitch = 0.0

    rotation = 0.0
    clock = pygame.time.Clock()

    grid = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ]

    # Main loop
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        # print(camera_pos)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera_pos += camera_speed * camera_front * dt
        if keys[pygame.K_s]:
            camera_pos -= camera_speed * camera_front * dt
        if keys[pygame.K_a]:
            camera_pos -= camera_right * camera_speed * dt
        if keys[pygame.K_d]:
            camera_pos += camera_right * camera_speed * dt
        if keys[pygame.K_LEFT]:
            yaw -= camera_speed * 10 * dt
        if keys[pygame.K_RIGHT]:
            yaw += camera_speed * 10 * dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    print("Bullet fired!")
                    game.entities.append(
                        Bullet(game, pos=glm.vec3(camera_pos), direction=direction)
                    )

                # Light controls
                if event.key == pygame.K_1:
                    # Toggle overhead light intensity
                    if light_manager.lights[0].intensity > 0:
                        light_manager.update_light_intensity(0, 0.0)
                        print("Overhead light OFF")
                    else:
                        light_manager.update_light_intensity(0, 2.0)
                        print("Overhead light ON")

                if event.key == pygame.K_2:
                    # Toggle side light intensity
                    if light_manager.lights[1].intensity > 0:
                        light_manager.update_light_intensity(1, 0.0)
                        print("Side light OFF")
                    else:
                        light_manager.update_light_intensity(1, 1.5)
                        print("Side light ON")

                if event.key == pygame.K_3:
                    # Toggle ground light intensity
                    if light_manager.lights[2].intensity > 0:
                        light_manager.update_light_intensity(2, 0.0)
                        print("Ground light OFF")
                    else:
                        light_manager.update_light_intensity(2, 1.0)
                        print("Ground light ON")

                if event.key == pygame.K_4:
                    # Toggle flashlight intensity
                    if light_manager.lights[flashlight_index].intensity > 0:
                        light_manager.update_light_intensity(flashlight_index, 0.0)
                        print("Flashlight OFF")
                    else:
                        light_manager.update_light_intensity(flashlight_index, 3.0)
                        print("Flashlight ON")

                if event.key == pygame.K_c:
                    # Cycle flashlight color
                    current_color = light_manager.lights[flashlight_index].color
                    if current_color.x > 0.9:  # Currently white/warm
                        light_manager.update_light_color(
                            flashlight_index, (1.0, 0.3, 0.3)
                        )  # Red
                        print("Flashlight: RED")
                    elif (
                        current_color.x > 0.9 and current_color.z < 0.5
                    ):  # Currently red
                        light_manager.update_light_color(
                            flashlight_index, (0.3, 1.0, 0.3)
                        )  # Green
                        print("Flashlight: GREEN")
                    elif current_color.y > 0.9:  # Currently green
                        light_manager.update_light_color(
                            flashlight_index, (0.3, 0.3, 1.0)
                        )  # Blue
                        print("Flashlight: BLUE")
                    else:  # Currently blue or other
                        light_manager.update_light_color(
                            flashlight_index, (1.0, 1.0, 0.8)
                        )  # White/warm
                        print("Flashlight: WHITE")

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

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.2, 0.3, 0.3, 1.0)

        # Use shader program
        glUseProgram(shader_program)

        # Update flashlight position to follow camera
        light_manager.update_light_position(flashlight_index, camera_pos)

        # Update rotation for the model
        # rotation += 0.01 * dt * 60
        model = glm.rotate(glm.mat4(1.0), rotation, glm.vec3(0, 1, 0))

        # Set uniforms
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))

        # Upload lighting data to shader
        light_manager.upload_to_shader()
        glUniform3f(view_pos_loc, camera_pos.x, camera_pos.y, camera_pos.z)

        bench.draw()

        wall_count = 3
        # for i in range(wall_count):
        #     wall.position = glm.vec3((i * 1.6), 0, 0)
        #     wall.draw()
        #
        # for i in range(wall_count):
        #     model = glm.rotate(glm.mat4(1.0), 80.0, glm.vec3(0, 1, 0))
        #     glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))
        #     wall.position = glm.vec3((i * 1.6), 0, 0)
        # wall.draw()

        for entity in game.entities:
            entity.update(dt)
            entity.draw()

        # Replace grid loop to draw both horizontal and vertical walls at corners
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    pos = glm.vec3(j * 1.6, 0, i * 1.6)
                    # horizontal wall if neighbor left/right or at top/bottom row
                    if (j > 0 and row[j-1] == 1) or (j < len(row)-1 and row[j+1] == 1) or i == 0 or i == len(grid)-1:
                        wall.position = pos
                        wall.rotation = 0.0
                        wall.draw()
                    # vertical wall if neighbor above/below or at left/right column
                    if (i > 0 and grid[i-1][j] == 1) or (i < len(grid)-1 and grid[i+1][j] == 1) or j == 0 or j == len(row)-1:
                        wall.position = pos
                        wall.rotation = 90.0
                        wall.draw()

        # Swap buffers
        pygame.display.flip()

    # Cleanup
    glDeleteProgram(shader_program)
    pygame.quit()


if __name__ == "__main__":
    main()
