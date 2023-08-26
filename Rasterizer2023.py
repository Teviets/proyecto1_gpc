from gl import Renderer
import shaders

# El tama�o del FrameBuffer
width = 972
height = 660

# Se crea el renderizador
rend = Renderer(width, height)

rend.glBackgroundTexture("textures/fondo.bmp")
rend.glClearBackground()



# Le damos los shaders que se utilizar�s
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.borderlands_toon_shader

# Cargamos los modelos que rederizaremos
rend.glLoadModel(filename = "obj/ardilla.obj",
                 textureName = "textures/ardilla_txr.bmp",
                 translate = (240, 150, -100),
                 rotate = (-90, 0, 45),
                 scale = (1.5,1.5,1.5))
rend.glRender()

rend.fragmentShader = shaders.hologram
rend.glLoadModel(filename = "obj/oso.obj",
                    textureName = "textures/oso_txr.bmp",
                    translate = (120, 190, -100),
                    rotate = (-90, 3, 15),
                    scale = (2.5,2,2))
rend.glRender()

rend.fragmentShader = shaders.phong_shader
rend.glLoadModel(filename = "obj/mapache.obj",
                    textureName = "textures/mapache_txr.bmp",
                    translate = (490, 30, 0),
                    rotate = (-75, 0, -10),
                    scale = (3.5,3.5,3.5))

rend.glRender()

rend.fragmentShader = shaders.flat_shader_with_dark_edges
rend.glLoadModel(filename = "obj/ave.obj",
                    textureName = "textures/ave_txr.bmp",
                    translate = (500, 280, 0),
                    rotate = (45, -50, 35),
                    scale = (1.5,1.5,1.5))


rend.glRender()



# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("proyecto.bmp")