from fakeNumpy import timeMatrix
import fakeNumpy as fnp
import math


def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    vpMatrix = kwargs["viewMatrix"]

    # Convertir el vértice a una matriz columna 4x1 agregando un valor de 1
    vt = [[vertex[0]], [vertex[1]], [vertex[2]], [1]]
    # Realizar la multiplicación de la matriz del modelo con el vértice
    vt = timeMatrix(vpMatrix, timeMatrix(projectionMatrix, timeMatrix(viewMatrix, timeMatrix(modelMatrix, vt))))
    # Convertir la matriz resultado de nuevo a un vértice (lista)
    vt = [vt[0][0],vt[1][0],vt[2][0]]
    return vt

#normal texture shader
def normal(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    if texture is not None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)
    return color

# border shader
def border(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    if texture is not None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)

    # Calculate the intensity of the color (brightness)
    intensity = (color[0] + color[1] + color[2]) / 3.0

    # Calculate new color components based on brightness
    new_red = color[0] * intensity
    new_green = color[1] * intensity
    new_blue = color[2] * intensity

    # Return the new color
    return (new_red, new_green, new_blue)

#toonshader basic
def toonshader(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    if texture is not None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)

    # Calculate the intensity of the color (brightness)
    intensity = (color[0] + color[1] + color[2]) / 3.0

    # Define the toon shading levels (adjust as needed)
    levels = 4

    # Calculate the new color value based on toon shading levels
    if intensity > 0.9:
        color = (1, 0, 1)  # High intensity, use white color for cuerpo
    elif intensity > 0.7:
        color = (1, 0.2, 0.8)  # Medium-high intensity, use white color for cuerpo
    elif intensity > 0.5:
        color = (0.3, 0.4, 0.6)  # Medium intensity, use orange color for camisa
    elif intensity > 0.3:
        color = (0.2, 0.6, 0.3)
    else:
        color = (0.1, 0.8, 0.2)

    return color

# Gray Scale Shader
def grayScaleShader(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    if texture is not None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)

    # Calculate the intensity of the color (brightness)
    intensity = (color[0] + color[1] + color[2]) / 3.0

    # Calculate new color components based on brightness
    new_red = intensity
    new_green = intensity
    new_blue = intensity

    # Return the new color
    return (new_red, new_green, new_blue)


# Invert Color Shader
def invertColorTextureEnhancedShader(**kwargs):
    texCoords = kwargs.get("texCoords")
    texture = kwargs.get("texture")

    if texture is not None:
        # Get the color directly from the texture
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)

    # Calculate the intensity of the color (brightness)
    intensity = (color[0] + color[1] + color[2]) / 3.0

    # Calculate new color components based on brightness
    new_red = 1.0 - color[0]
    new_green = 1.0 - color[1]
    new_blue = 1.0 - color[2]

    # Apply a strength factor based on intensity for more controlled inversion
    strength = 0.5  # You can adjust this value for desired effect
    inverted_color = (
        new_red * strength + color[0] * (1 - strength),
        new_green * strength + color[1] * (1 - strength),
        new_blue * strength + color[2] * (1 - strength)
    )

    # Return the new color
    return inverted_color


#Shader de Dibujo a Mano:
def pencil(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    if texture is not None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)

    # Calculate the intensity of the color (brightness)
    intensity = (color[0] + color[1] + color[2]) / 3.0

    # Calculate new color components based on brightness
    new_red = intensity
    new_green = intensity
    new_blue = intensity

    # Return the new color
    return (new_red, new_green, new_blue)


def hologram(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    if texture is not None:
        original_color = texture.getColor(texCoords[0], texCoords[1])
    else:
        original_color = (1, 1, 1)

    # Calculate a sinusoidal wave based on time and texture coordinates
    frequency = 10.0  # Frequency of the wave
    amplitude = 0.1   # Amplitude of the wave
    time = kwargs.get("time", 0.0)  # You need to pass the current time as a keyword argument
    offset = math.sin(frequency * time + texCoords[0] * 10.0) * amplitude

    # Calculate displaced texture coordinates
    displaced_tex_coord = (texCoords[0], texCoords[1] + offset)

    if texture is not None:
        displaced_color = texture.getColor(displaced_tex_coord[0], displaced_tex_coord[1])
    else:
        displaced_color = (1, 1, 1)
    if displaced_color is None:
        displaced_color = (1, 1, 1)
        
    # Apply color blending with more control using a parameter
    hologram_blending_factor = 0.5
    hologram_color = (
        (1 - hologram_blending_factor) * original_color[0] + hologram_blending_factor * displaced_color[0],
        (1 - hologram_blending_factor) * original_color[1] + hologram_blending_factor * displaced_color[1],
        (1 - hologram_blending_factor) * original_color[2] + hologram_blending_factor * displaced_color[2]
    )

    return hologram_color

def saturate_color(color, factor):
    # Aumentar la saturación de cada canal de color por el factor especificado
    saturated_color = (
        min(1, color[0] + factor * 3),
        min(1, color[1] + factor * 3),
        min(1, color[2] + factor * 3)
    )
    return saturated_color

def borderlands_toon_shader(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    if texture is not None:
        # Obtener el color directamente de la textura
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)

    # Calcular la distancia desde el centro de la textura
    center_x = 0.5
    center_y = 0.5
    distance_to_center = ((texCoords[0] - center_x) ** 2 + (texCoords[1] - center_y) ** 2) ** 0.5

    # Calcular la intensidad del color (brillo)
    intensity = (color[0] + color[1] + color[2]) / 3.0

    # Definir los niveles de sombreado toon con colores más saturados
    if intensity > 0.9:
        shading_color = saturate_color((1, 0.5, 0.5), 0.2)  # Rojo más saturado
    elif intensity > 0.7:
        shading_color = saturate_color((1, 0.7, 0.5), 0.2)  # Naranja más saturado
    elif intensity > 0.5:
        shading_color = saturate_color((0.5, 1, 0.5), 0.2)  # Verde más saturado
    elif intensity > 0.3:
        shading_color = saturate_color((0.5, 0.7, 1), 0.2)  # Azul más saturado
    else:
        shading_color = saturate_color((1, 1, 0.5), 0.2)  # Amarillo más saturado

    # Si el fragmento está en los bordes del modelo, ajustar el color hacia el centro
    border_threshold = 0.15  # Ajusta este valor para controlar la intensidad de los bordes negros
    border_softness = 0.2  # Ajusta este valor para controlar el suavizado de los bordes
    if intensity < border_threshold:
        # Calcular el factor de suavizado basado en la distancia al centro
        softness_factor = 1 - min(1, (distance_to_center / border_softness))
        return (0, 0, 0, softness_factor)  # Devolver también el factor de suavizado
    else:
        # Aclarar el color utilizando la intensidad
        aclarado = (color[0] + intensity * (1 - color[0]),
                    color[1] + intensity * (1 - color[1]),
                    color[2] + intensity * (1 - color[2]))
        # Mezclar el color aclarado con el color de sombreado más saturado
        final_color = (aclarado[0] * shading_color[0],
                       aclarado[1] * shading_color[1],
                       aclarado[2] * shading_color[2])
        return final_color

def phong_shader(**kwargs):
    texCoords = kwargs["texCoords"]
    normal = kwargs["normal"]
    light_direction = kwargs["lightDirection"]
    texture = kwargs["texture"]

    if texture is not None:
        base_color = texture.getColor(texCoords[0], texCoords[1])
    else:
        base_color = (1, 1, 1)

    ambient_color = (0.2, 0.2, 0.2)
    diffuse_color = (0.8, 0.8, 0.8)
    specular_color = (1, 1, 1)

    # Normalizar los vectores de dirección y normal
    light_direction = fnp.normalize(light_direction)
    normal = fnp.normalize(normal)

    # Cálculo del término de luz difusa
    diffuse_intensity = max(0, fnp.dot_product(normal, light_direction))

    # Cálculo del término de luz especular
    view_direction = (0, 0, -1)
    halfway_vector = fnp.normalize((
        light_direction[0] + view_direction[0],
        light_direction[1] + view_direction[1],
        light_direction[2] + view_direction[2]
    ))
    specular_intensity = max(0, fnp.dot_product(normal, halfway_vector))
    specular_intensity = math.pow(specular_intensity, 16)
    specular_intensity = min(specular_intensity, 1.0)  # Limitar a 1.0

    # Combinación de los términos de luz con el color base
    shaded_color = (
        min(base_color[0] * (ambient_color[0] + diffuse_color[0] * diffuse_intensity) +
            specular_color[0] * specular_intensity, 1.0),  # Limitar a 1.0

        min(base_color[1] * (ambient_color[1] + diffuse_color[1] * diffuse_intensity) +
            specular_color[1] * specular_intensity, 1.0),  # Limitar a 1.0

        min(base_color[2] * (ambient_color[2] + diffuse_color[2] * diffuse_intensity) +
            specular_color[2] * specular_intensity, 1.0)  # Limitar a 1.0
    )

    return shaded_color

def radioactive_shader(**kwargs):
    texCoords = kwargs["texCoords"]
    normal = kwargs["normal"]
    light_direction = kwargs["lightDirection"]
    texture = kwargs["texture"]

    if texture is not None:
        base_color = texture.getColor(texCoords[0], texCoords[1])
    else:
        base_color = (1, 1, 1)

    ambient_color = (0.2, 0.2, 0.2)  # Color de luz ambiente
    diffuse_color = (0.8, 0.8, 0.8)  # Color de luz difusa
    specular_color = (1, 1, 1)       # Color de luz especular

    # Cálculo del término de luz difusa
    diffuse_intensity = max(0, normal[0] * light_direction[0] +
                                 normal[1] * light_direction[1] +
                                 normal[2] * light_direction[2])

    # Cálculo del término de luz especular
    view_direction = (0, 0, -1)  # Dirección de la vista (hacia la cámara)
    halfway_vector = (
        light_direction[0] + view_direction[0],
        light_direction[1] + view_direction[1],
        light_direction[2] + view_direction[2]
    )
    specular_intensity = max(0, normal[0] * halfway_vector[0] +
                                  normal[1] * halfway_vector[1] +
                                  normal[2] * halfway_vector[2])
    specular_intensity = math.pow(specular_intensity, 16)  # Ajustar el brillo

    # Aplicar el efecto de radiactividad (añadir tono verdoso y brillo)
    shaded_color = (
        base_color[0] * (ambient_color[0] + diffuse_color[0] * diffuse_intensity) +
        specular_color[0] * specular_intensity,
        
        min(base_color[1] * (ambient_color[1] + diffuse_color[1] * diffuse_intensity) +
            specular_color[1] * specular_intensity + 0.3, 1.0),  # Limitar a 1.0
        
        base_color[2] * (ambient_color[2] + diffuse_color[2] * diffuse_intensity) +
        specular_color[2] * specular_intensity
    )
    
    # Aplicar un ligero efecto de saturación para aumentar la vivacidad
    saturated_color = (
        min(shaded_color[0] * 1.2, 1.0),  # Aumentar el valor rojo
        min(shaded_color[1] * 1.1, 1.0),  # Aumentar el valor verde
        shaded_color[2]  # Mantener el valor azul
    )
    
    # Normalizar los valores del color para que estén en el rango de 0 a 1
    max_color_value = max(saturated_color)
    if max_color_value > 1.0:
        final_color = [c / max_color_value for c in saturated_color]
    else:
        final_color = saturated_color

    return final_color

def diamond_shader(**kwargs):
    texCoords = kwargs["texCoords"]
    normal = kwargs["normal"]
    light_direction = kwargs["lightDirection"]
    
    texture = kwargs["texture"]

    view_direction = (0, 0, -1)  # Dirección de la vista (hacia la cámara)

    if texture is not None:
        base_color = texture.getColor(texCoords[0], texCoords[1])
    else:
        base_color = (0.8, 0.8, 0.8)  # Color base si no hay textura

    # Calcular la intensidad del brillo basado en la dirección de la luz y la normal
    specular_intensity = max(0, normal[0] * light_direction[0] +
                                  normal[1] * light_direction[1] +
                                  normal[2] * light_direction[2])
    specular_intensity = math.pow(specular_intensity, 32)  # Ajustar el brillo

    # Ajustar los colores hacia tonos celestes y añadir brillos hacia la cámara
    celestized_color = (
        min(base_color[0] + 0.2, 1.0),   # Incrementar el componente rojo
        min(base_color[1] + 0.3, 1.0),   # Incrementar el componente verde
        min(base_color[2] + 0.5, 1.0)    # Incrementar el componente azul
    )

    # Añadir brillos hacia la cámara (especular)
    specular_color = (0.8, 0.8, 0.8)  # Color de brillo especular
    specular_intensity_camera = max(0, normal[0] * view_direction[0] +
                                        normal[1] * view_direction[1] +
                                        normal[2] * view_direction[2])
    specular_intensity_camera = math.pow(specular_intensity_camera, 16)  # Ajustar el brillo de la cámara

    final_color = (
        min(celestized_color[0] + specular_color[0] * specular_intensity + specular_color[0] * specular_intensity_camera, 1.0),
        min(celestized_color[1] + specular_color[1] * specular_intensity + specular_color[1] * specular_intensity_camera, 1.0),
        min(celestized_color[2] + specular_color[2] * specular_intensity + specular_color[2] * specular_intensity_camera, 1.0)
    )
    
    return final_color
    


def custom_shader(**kwargs):
    texCoords = kwargs["texCoords"]
    normal = kwargs["normal"]
    light_direction = kwargs["lightDirection"]
    texture = kwargs["texture"]

    if texture is not None:
        base_color = texture.getColor(texCoords[0], texCoords[1])
    else:
        base_color = (1, 1, 1)

    # Cálculo del término de luz difusa y especular (Phong)
    ambient_color = (0.2, 0.2, 0.2)
    diffuse_color = (0.8, 0.8, 0.8)
    specular_color = (1, 1, 1)

    light_direction = fnp.normalize(light_direction)
    normal = fnp.normalize(normal)

    diffuse_intensity = max(0, fnp.dot_product(normal, light_direction))

    view_direction = (0, 0, -1)
    halfway_vector = fnp.normalize((
        light_direction[0] + view_direction[0],
        light_direction[1] + view_direction[1],
        light_direction[2] + view_direction[2]
    ))
    specular_intensity = max(0, fnp.dot_product(normal, halfway_vector))
    specular_intensity = math.pow(specular_intensity, 16)
    specular_intensity = min(specular_intensity, 1.0)

    phong_shaded_color = (
        min(base_color[0] * (ambient_color[0] + diffuse_color[0] * diffuse_intensity) +
            specular_color[0] * specular_intensity, 1.0),

        min(base_color[1] * (ambient_color[1] + diffuse_color[1] * diffuse_intensity) +
            specular_color[1] * specular_intensity, 1.0),

        min(base_color[2] * (ambient_color[2] + diffuse_color[2] * diffuse_intensity) +
            specular_color[2] * specular_intensity, 1.0)
    )

    # Efecto de radiactividad
    radioactive_ambient_color = (0.2, 0.2, 0.2)
    radioactive_diffuse_color = (0.8, 0.8, 0.8)
    radioactive_specular_color = (1, 1, 1)

    radioactive_diffuse_intensity = max(0, normal[0] * light_direction[0] +
                                        normal[1] * light_direction[1] +
                                        normal[2] * light_direction[2])

    radioactive_view_direction = (0, 0, -1)
    radioactive_halfway_vector = (
        light_direction[0] + radioactive_view_direction[0],
        light_direction[1] + radioactive_view_direction[1],
        light_direction[2] + radioactive_view_direction[2]
    )
    radioactive_specular_intensity = max(0, normal[0] * radioactive_halfway_vector[0] +
                                         normal[1] * radioactive_halfway_vector[1] +
                                         normal[2] * radioactive_halfway_vector[2])
    radioactive_specular_intensity = math.pow(radioactive_specular_intensity, 16)

    radioactive_shaded_color = (
        phong_shaded_color[0] * (radioactive_ambient_color[0] + radioactive_diffuse_color[0] * radioactive_diffuse_intensity) +
        radioactive_specular_color[0] * radioactive_specular_intensity,

        phong_shaded_color[1] * (radioactive_ambient_color[1] + radioactive_diffuse_color[1] * radioactive_diffuse_intensity) +
        radioactive_specular_color[1] * radioactive_specular_intensity + 0.3,

        phong_shaded_color[2] * (radioactive_ambient_color[2] + radioactive_diffuse_color[2] * radioactive_diffuse_intensity) +
        radioactive_specular_color[2] * radioactive_specular_intensity
    )

    # Efecto de saturación
    saturated_color = (
        min(radioactive_shaded_color[0] * 1.2, 1.0),
        min(radioactive_shaded_color[1] * 1.1, 1.0),
        radioactive_shaded_color[2]
    )

    # Normalizar los valores del color
    max_color_value = max(saturated_color)
    if max_color_value > 1.0:
        final_color = [c / max_color_value for c in saturated_color]
    else:
        final_color = saturated_color

    return final_color

def flat_shader_with_dark_edges(**kwargs):
    texCoords = kwargs["texCoords"]
    normal = kwargs["normal"]
    light_direction = kwargs["lightDirection"]
    texture = kwargs["texture"]

    if texture is not None:
        base_color = texture.getColor(texCoords[0], texCoords[1])
    else:
        base_color = (1, 1, 1)

    # Calcular la intensidad de la luz difusa
    diffuse_intensity = max(0, fnp.dot_product(normal, light_direction))

    # Calcular los bordes oscuros (usando el producto punto entre la normal y la luz)
    edge_intensity = max(0, -fnp.dot_product(normal, light_direction))

    # Ajustar la intensidad de los bordes oscuros
    edge_intensity = edge_intensity * 0.7  # Puedes ajustar este valor según tus preferencias

    # Combinar el color base con la intensidad de la luz difusa
    shaded_color = (
        base_color[0] * diffuse_intensity,
        base_color[1] * diffuse_intensity,
        base_color[2] * diffuse_intensity
    )

    # Agregar los bordes oscuros al color resultante, pero limitar a 1.0
    final_color = (
        min(shaded_color[0] + edge_intensity, 1.0),
        min(shaded_color[1] + edge_intensity, 1.0),
        min(shaded_color[2] + edge_intensity, 1.0)
    )

    return final_color
