from pygame.locals import *
from OpenGL.GL import *
import numpy as np
import ctypes
import pygame


class Object:
    def __init__(self, object: str, texture: str, flip_texture=True):
        self.vertices = []
        self.indices = []
        self.face_shape = None
        self.vao = None
        self.flip = flip_texture
        self.index_count = 0
        self.texture_id = None

        if object:
            self.load_obj(object)

        if texture:
            self.texture_id = self.load_texture(texture)

    def load_texture(self, filename):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        self.texture_id = texture

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # Load image data
        image = pygame.image.load(filename)
        if self.flip:
            image = pygame.transform.flip(
                image, False, True
            )  # Flip vertically, not horizontally
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
        _normals = []
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
                elif line.startswith("vn "):
                    parts = line.strip().split()
                    _normals.append(tuple(map(float, parts[1:4])))
                elif line.startswith("f "):
                    parts = line.strip().split()[1:]

                    if len(parts) == 3:
                        # Triangle - process normally
                        self.face_shape = GL_TRIANGLES
                        face_indices = []
                        for part in parts:
                            vals = part.split("/")
                            v_idx = int(vals[0]) - 1
                            vt_idx = int(vals[1]) - 1 if len(vals) > 1 and vals[1] else 0
                            vn_idx = int(vals[2]) - 1 if len(vals) > 2 and vals[2] else 0

                            key = (v_idx, vt_idx)
                            if key not in unique_verts:
                                unique_verts[key] = len(self.vertices) // 8
                                pos = _positions[v_idx]
                                tex = (
                                    _texcoords[vt_idx]
                                    if vt_idx < len(_texcoords)
                                    else (0.0, 0.0)
                                )
                                normal = _normals[vn_idx]  # Placeholder for normals
                                self.vertices.extend(pos + tex + normal)
                            face_indices.append(unique_verts[key])

                        # Store triangle indices
                        self.indices.extend(face_indices)

                    elif len(parts) == 4:
                        # Quad - convert to two triangles
                        self.face_shape = GL_QUADS
                        quad_indices = []
                        for part in parts:
                            vals = part.split("/")
                            v_idx = int(vals[0]) - 1
                            vt_idx = int(vals[1]) - 1 if len(vals) > 1 and vals[1] else 0
                            vn_idx = int(vals[2]) - 1 if len(vals) > 2 and vals[2] else 0

                            key = (v_idx, vt_idx)
                            if key not in unique_verts:
                                unique_verts[key] = len(self.vertices) // 8
                                pos = _positions[v_idx]
                                tex = (
                                    _texcoords[vt_idx]
                                    if vt_idx < len(_texcoords)
                                    else (0.0, 0.0)
                                )
                                normal = _normals[vn_idx]  # Placeholder for normals
                                self.vertices.extend(pos + tex + normal)
                            quad_indices.append(unique_verts[key])

                        # Convert quad to two triangles (0,1,2) and (0,2,3)
                        self.indices.extend([quad_indices[0], quad_indices[1], quad_indices[2]])
                        self.indices.extend([quad_indices[0], quad_indices[2], quad_indices[3]])

                    else:
                        raise ValueError("Unsupported face format")

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

        stride = 8 * ctypes.sizeof(ctypes.c_float)

        # Position attribute
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        # Texture attribute
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(
            1,
            2,
            GL_FLOAT,
            GL_FALSE,
            stride,
            ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)),
        )

        # Normals attribute
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(
            2,
            3,
            GL_FLOAT,
            GL_FALSE,
            stride,
            ctypes.c_void_p(5 * ctypes.sizeof(ctypes.c_float)),
        )

        glBindVertexArray(0)

        self.vao = vao

    def draw(self, texture_id=None):
        if self.texture_id is not None:
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        if texture_id is not None:
            glBindTexture(GL_TEXTURE_2D, texture_id)
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.index_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        if texture_id is not None:
            glBindTexture(GL_TEXTURE_2D, 0)
