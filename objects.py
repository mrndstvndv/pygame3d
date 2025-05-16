from pygame.locals import *
from OpenGL.GL import *
import numpy as np

def create_square():
    # Vertex data for a square (two triangles)
    vertices = np.array([
        # First triangle
        -0.5,  0.5, 0.0,  # Top left
        -0.5, -0.5, 0.0,  # Bottom left
         0.5,  0.5, 0.0,  # Top right
        # Second triangle
         0.5,  0.5, 0.0,  # Top right
        -0.5, -0.5, 0.0,  # Bottom left
         0.5, -0.5, 0.0   # Bottom right
    ], dtype=np.float32)

    # Create VAO and VBO
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    # Bind VAO and VBO
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Set vertex attributes
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    # Unbind VAO and VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao

def create_pokeball():
    # Vertex data for a complete cube (all six faces)
    vertices = np.array([
        # Top half (white)
        # Front face (z positive)
        -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  # Top left
        -0.5,  0.0,  0.5,  1.0, 1.0, 1.0,  # Bottom left
         0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  # Top right
         0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  # Top right
        -0.5,  0.0,  0.5,  1.0, 1.0, 1.0,  # Bottom left
         0.5,  0.0,  0.5,  1.0, 1.0, 1.0,  # Bottom right

        # Back face (z negative)
        -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  # Top left
         0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  # Top right
        -0.5,  0.0, -0.5,  1.0, 1.0, 1.0,  # Bottom left
         0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  # Top right
         0.5,  0.0, -0.5,  1.0, 1.0, 1.0,  # Bottom right
        -0.5,  0.0, -0.5,  1.0, 1.0, 1.0,  # Bottom left

        # Right face (x positive)
         0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  # Top front
         0.5,  0.0,  0.5,  1.0, 1.0, 1.0,  # Bottom front
         0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  # Top back
         0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  # Top back
         0.5,  0.0,  0.5,  1.0, 1.0, 1.0,  # Bottom front
         0.5,  0.0, -0.5,  1.0, 1.0, 1.0,  # Bottom back

        # Left face (x negative)
        -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  # Top front
        -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  # Top back
        -0.5,  0.0,  0.5,  1.0, 1.0, 1.0,  # Bottom front
        -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  # Top back
        -0.5,  0.0, -0.5,  1.0, 1.0, 1.0,  # Bottom back
        -0.5,  0.0,  0.5,  1.0, 1.0, 1.0,  # Bottom front

        # Bottom half (red)
        # Front face
        -0.5,  0.0,  0.5,  1.0, 0.0, 0.0,  # Top left
        -0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  # Bottom left
         0.5,  0.0,  0.5,  1.0, 0.0, 0.0,  # Top right
         0.5,  0.0,  0.5,  1.0, 0.0, 0.0,  # Top right
        -0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  # Bottom left
         0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  # Bottom right

        # Back face
        -0.5,  0.0, -0.5,  1.0, 0.0, 0.0,  # Top left
         0.5,  0.0, -0.5,  1.0, 0.0, 0.0,  # Top right
        -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  # Bottom left
         0.5,  0.0, -0.5,  1.0, 0.0, 0.0,  # Top right
         0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  # Bottom right
        -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  # Bottom left

        # Right face
         0.5,  0.0,  0.5,  1.0, 0.0, 0.0,  # Top front
         0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  # Bottom front
         0.5,  0.0, -0.5,  1.0, 0.0, 0.0,  # Top back
         0.5,  0.0, -0.5,  1.0, 0.0, 0.0,  # Top back
         0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  # Bottom front
         0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  # Bottom back

        # Left face
        -0.5,  0.0,  0.5,  1.0, 0.0, 0.0,  # Top front
        -0.5,  0.0, -0.5,  1.0, 0.0, 0.0,  # Top back
        -0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  # Bottom front
        -0.5,  0.0, -0.5,  1.0, 0.0, 0.0,  # Top back
        -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  # Bottom back
        -0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  # Bottom front
    ], dtype=np.float32)

    # Create VAO and VBO
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    # Bind VAO and VBO
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Position attribute
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

    # Color attribute
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    # Unbind VAO and VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao

def create_button():
    # Vertex data for a black square that protrudes from the front face
    vertices = np.array([
        # Front face (protruding part)
        -0.15,  0.15,  0.51,  0.0, 0.0, 0.0,  # Top left
        -0.15, -0.15,  0.51,  0.0, 0.0, 0.0,  # Bottom left
         0.15,  0.15,  0.51,  0.0, 0.0, 0.0,  # Top right
         0.15,  0.15,  0.51,  0.0, 0.0, 0.0,  # Top right
        -0.15, -0.15,  0.51,  0.0, 0.0, 0.0,  # Bottom left
         0.15, -0.15,  0.51,  0.0, 0.0, 0.0,  # Bottom right

        # Back face (inside the cube)
        -0.15,  0.15,  0.3,   0.0, 0.0, 0.0,  # Top left
         0.15,  0.15,  0.3,   0.0, 0.0, 0.0,  # Top right
        -0.15, -0.15,  0.3,   0.0, 0.0, 0.0,  # Bottom left
         0.15,  0.15,  0.3,   0.0, 0.0, 0.0,  # Top right
         0.15, -0.15,  0.3,   0.0, 0.0, 0.0,  # Bottom right
        -0.15, -0.15,  0.3,   0.0, 0.0, 0.0,  # Bottom left

        # Connect front to back
        # Right face
         0.15,  0.15,  0.51,  0.0, 0.0, 0.0,
         0.15, -0.15,  0.51,  0.0, 0.0, 0.0,
         0.15,  0.15,  0.3,   0.0, 0.0, 0.0,
         0.15,  0.15,  0.3,   0.0, 0.0, 0.0,
         0.15, -0.15,  0.51,  0.0, 0.0, 0.0,
         0.15, -0.15,  0.3,   0.0, 0.0, 0.0,

        # Left face
        -0.15,  0.15,  0.51,  0.0, 0.0, 0.0,
        -0.15,  0.15,  0.3,   0.0, 0.0, 0.0,
        -0.15, -0.15,  0.51,  0.0, 0.0, 0.0,
        -0.15,  0.15,  0.3,   0.0, 0.0, 0.0,
        -0.15, -0.15,  0.3,   0.0, 0.0, 0.0,
        -0.15, -0.15,  0.51,  0.0, 0.0, 0.0,

        # Top face
        -0.15,  0.15,  0.51,  0.0, 0.0, 0.0,
         0.15,  0.15,  0.51,  0.0, 0.0, 0.0,
        -0.15,  0.15,  0.3,   0.0, 0.0, 0.0,
         0.15,  0.15,  0.51,  0.0, 0.0, 0.0,
         0.15,  0.15,  0.3,   0.0, 0.0, 0.0,
        -0.15,  0.15,  0.3,   0.0, 0.0, 0.0,

        # Bottom face
        -0.15, -0.15,  0.51,  0.0, 0.0, 0.0,
        -0.15, -0.15,  0.3,   0.0, 0.0, 0.0,
         0.15, -0.15,  0.51,  0.0, 0.0, 0.0,
         0.15, -0.15,  0.51,  0.0, 0.0, 0.0,
        -0.15, -0.15,  0.3,   0.0, 0.0, 0.0,
         0.15, -0.15,  0.3,   0.0, 0.0, 0.0,
    ], dtype=np.float32)

    # Create VAO and VBO
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    # Bind VAO and VBO
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Position attribute
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

    # Color attribute
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    # Unbind VAO and VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao
