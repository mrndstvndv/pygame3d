from pyglm import glm
from OpenGL.GL import *
import numpy as np

class Light:
    def __init__(self, position, color=(1.0, 1.0, 1.0), intensity=1.0):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.intensity = intensity

class LightManager:
    def __init__(self, shader_program, max_lights=8):
        self.shader_program = shader_program
        self.max_lights = max_lights
        self.lights = []
        
        # Get uniform locations
        self.num_lights_loc = glGetUniformLocation(shader_program, "numLights")
        self.light_positions_loc = glGetUniformLocation(shader_program, "lightPositions")
        self.light_colors_loc = glGetUniformLocation(shader_program, "lightColors")
        self.light_intensities_loc = glGetUniformLocation(shader_program, "lightIntensities")
    
    def add_light(self, light):
        if len(self.lights) < self.max_lights:
            self.lights.append(light)
        else:
            print(f"Maximum number of lights ({self.max_lights}) reached")
    
    def remove_light(self, index):
        if 0 <= index < len(self.lights):
            del self.lights[index]
    
    def update_light_position(self, index, position):
        if 0 <= index < len(self.lights):
            self.lights[index].position = glm.vec3(position)
    
    def update_light_color(self, index, color):
        if 0 <= index < len(self.lights):
            self.lights[index].color = glm.vec3(color)
    
    def update_light_intensity(self, index, intensity):
        if 0 <= index < len(self.lights):
            self.lights[index].intensity = intensity
    
    def upload_to_shader(self):
        """Upload all light data to the shader"""
        glUseProgram(self.shader_program)
        
        num_lights = len(self.lights)
        glUniform1i(self.num_lights_loc, num_lights)
        
        if num_lights > 0:
            # Prepare arrays for positions, colors, and intensities
            positions = []
            colors = []
            intensities = []
            
            for light in self.lights:
                positions.extend([light.position.x, light.position.y, light.position.z])
                colors.extend([light.color.x, light.color.y, light.color.z])
                intensities.append(light.intensity)
            
            # Pad arrays to max_lights size if needed
            while len(positions) < self.max_lights * 3:
                positions.extend([0.0, 0.0, 0.0])
            while len(colors) < self.max_lights * 3:
                colors.extend([0.0, 0.0, 0.0])
            while len(intensities) < self.max_lights:
                intensities.append(0.0)
            
            # Upload to shader
            glUniform3fv(self.light_positions_loc, self.max_lights, positions)
            glUniform3fv(self.light_colors_loc, self.max_lights, colors)
            glUniform1fv(self.light_intensities_loc, self.max_lights, intensities)
