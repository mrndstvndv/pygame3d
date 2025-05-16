# import os
# os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL import shaders
from objects import create_button, create_square, create_pokeball
import numpy as np
from pyglm import glm

# Shader source code
VERTEX_SHADER = """
#version 330
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
out vec3 fragColor;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    fragColor = color;
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330
in vec3 fragColor;
out vec4 outColor;

void main() {
    outColor = vec4(fragColor, 1.0);
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    
    # Check compilation status
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        print(f"Shader compilation error: {error}")
        glDeleteShader(shader)
        return None
    return shader

def create_shader_program(vertex_shader_source, fragment_shader_source):
    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)
    
    if not vertex_shader or not fragment_shader:
        return None
    
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    
    # Check linking status
    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        print(f"Shader program linking error: {error}")
        glDeleteProgram(program)
        return None
    
    # Clean up individual shaders
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    return program

def init_pygame_opengl():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    
    # Create a window with OpenGL context
    width, height = 800, 600
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL with Shaders")

def main():
    init_pygame_opengl()
    
    # Create and use shader program
    shader_program = create_shader_program(VERTEX_SHADER, FRAGMENT_SHADER)
    if not shader_program:
        print("Failed to create shader program")
        return

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)

    # Create pokeball VAO
    pokeball_vao = create_pokeball()
    button_vao = create_button()

    # Get uniform locations
    model_loc = glGetUniformLocation(shader_program, "model")
    view_loc = glGetUniformLocation(shader_program, "view")
    proj_loc = glGetUniformLocation(shader_program, "projection")

    # Create transformation matrices
    projection = glm.perspective(glm.radians(45.0), 800.0 / 600.0, 0.1, 100.0)
    
    # Camera position and orientation
    camera_pos = glm.vec3(0.0, 0.0, 5.0)
    camera_target = glm.vec3(0.0, 0.0, 0.0)
    camera_up = glm.vec3(0.0, 1.0, 0.0)
    view = glm.lookAt(camera_pos, camera_target, camera_up)

    rotation = 0.0
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.2, 0.3, 0.3, 1.0)
        
        # Use shader program
        glUseProgram(shader_program)

        # Update rotation
        rotation += 0.01
        model = glm.rotate(glm.mat4(1.0), rotation, glm.vec3(0, 1, 0))

        # Set uniforms
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))

        # Draw the pokeball
        glBindVertexArray(pokeball_vao)
        glDrawArrays(GL_TRIANGLES, 0, 72)  # 72 vertices for 24 triangles (12 faces total)
        glBindVertexArray(0)

        # Draw the button
        glBindVertexArray(button_vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)  # 36 vertices for 12 triangles (6 faces)
        glBindVertexArray(0)
        
        # Swap buffers
        pygame.display.flip()
    
    # Cleanup
    glDeleteProgram(shader_program)
    pygame.quit()

if __name__ == "__main__":
    main()
