from pygame.locals import *
from OpenGL.GL import *
import numpy as np
import ctypes
import pygame


class Object:
    def __init__(self):
        self.vertices = []
        self.indices = []
        self.face_shape = None
        self.vao = None
        self.index_count = 0

    def load_texture(self, filename):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # Load image data
        image = pygame.image.load(filename)
        image = pygame.transform.flip(image, False, True)  # Flip vertically, not horizontally
        image_data = pygame.image.tostring(image, "RGBA", True)
        width, height = image.get_size()

        # Upload texture data
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            image_data,
        )
        glGenerateMipmap(GL_TEXTURE_2D)

        return texture

    def load_obj(self, filename):
        _positions = []
        _texcoords = []
        unique_verts = {}
        self.vertices = []
        self.indices = []

        with open(filename, "r") as file:
            for line in file:
                if line.startswith("v "):
                    parts = line.strip().split()
                    _positions.append(tuple(map(float, parts[1:4])))
                elif line.startswith("vt "):
                    parts = line.strip().split()
                    _texcoords.append(tuple(map(float, parts[1:3])))
                elif line.startswith("f "):
                    parts = line.strip().split()[1:]

                    if len(parts) == 3:
                        self.face_shape = GL_TRIANGLES
                    elif len(parts) == 4:
                        self.face_shape = GL_QUADS
                    else:
                        raise ValueError("Unsupported face format")

                    face_indices = []
                    for part in parts:
                        vals = part.split("/")
                        v_idx = int(vals[0]) - 1
                        vt_idx = int(vals[1]) - 1 if len(vals) > 1 and vals[1] else 0

                        key = (v_idx, vt_idx)
                        if key not in unique_verts:
                            unique_verts[key] = len(self.vertices) // 5
                            pos = _positions[v_idx]
                            tex = (
                                _texcoords[vt_idx]
                                if vt_idx < len(_texcoords)
                                else (0.0, 0.0)
                            )
                            self.vertices.extend(pos + tex)
                        face_indices.append(unique_verts[key])

                    # Store indices directly
                    self.indices.extend(face_indices)

        print("Vertices:", self.vertices)
        print("Indices:", self.indices)
        self._create_buffers()

    def _create_buffers(self):
        vertices = np.array(self.vertices, dtype=np.float32)
        indices = np.array(self.indices, dtype=np.uint32)
        self.index_count = len(indices)

        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        ebo = glGenBuffers(1)

        glBindVertexArray(vao)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        stride = 5 * ctypes.sizeof(ctypes.c_float)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(
            1,
            2,
            GL_FLOAT,
            GL_FALSE,
            stride,
            ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)),
        )

        glBindVertexArray(0)

        self.vao = vao

    def draw(self, texture_id=None):
        if texture_id is not None:
            glBindTexture(GL_TEXTURE_2D, texture_id)
        glBindVertexArray(self.vao)
        glDrawElements(self.face_shape, self.index_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        if texture_id is not None:
            glBindTexture(GL_TEXTURE_2D, 0)
