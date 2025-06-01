from OpenGL.GL import *

VERTEX_SHADER = """
#version 330
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoord;
layout(location = 2) in vec3 normal;
out vec2 TexCoord;
out vec3 Normal;
out vec3 FragPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec3 pos;

void main() {
    vec3 loc = pos + position;
    FragPos = vec3(model * vec4(loc, 1.0));
    Normal = mat3(transpose(inverse(model))) * normal;
    
    gl_Position = projection * view * model * vec4(loc, 1.0);
    TexCoord = texCoord;
}
"""

FRAGMENT_SHADER = """
#version 330

in vec2 TexCoord;
in vec3 Normal;
in vec3 FragPos;
out vec4 FragColor;

uniform sampler2D ourTexture;
uniform vec3 viewPos;

// Multiple lights support
#define MAX_LIGHTS 8
uniform int numLights;
uniform vec3 lightPositions[MAX_LIGHTS];
uniform vec3 lightColors[MAX_LIGHTS];
uniform float lightIntensities[MAX_LIGHTS];

vec3 calculateLight(vec3 lightPos, vec3 lightColor, float intensity, vec3 norm, vec3 viewDir) {
    // Calculate distance for attenuation
    float distance = length(lightPos - FragPos);
    float attenuation = intensity / (1.0 + 0.09 * distance + 0.032 * distance * distance);
    
    // Diffuse 
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor * attenuation;
    
    // Specular
    float specularStrength = 0.5;
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor * attenuation;
    
    return diffuse + specular;
}

void main() {
    // Ambient lighting (global)
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * vec3(1.0, 1.0, 1.0);
    
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);
    
    // Calculate lighting from all light sources
    vec3 result = ambient;
    for(int i = 0; i < numLights && i < MAX_LIGHTS; i++) {
        result += calculateLight(lightPositions[i], lightColors[i], lightIntensities[i], norm, viewDir);
    }
    
    // Apply to texture
    vec4 texColor = texture(ourTexture, TexCoord);
    FragColor = vec4(result * texColor.rgb, texColor.a);
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


def create_shader_program():
    vertex_shader = compile_shader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

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
