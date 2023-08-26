import struct

class Texture(object):
    def __init__(self, filename):
        with open(filename, "rb") as image:
            # Se carga la información de la imagen, asumiendo
            # que tiene un formato BMP de 24 bits.
            image.seek(10)
            headerSize = struct.unpack('=l', image.read(4))[0]

            image.seek(18)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]

            image.seek(headerSize)

            self.pixels = []

            for y in range(self.height):
                pixelRow = []

                for x in range(self.width):
                    b, g, r = struct.unpack('=BBB', image.read(3))
                    pixelRow.append([r / 255, g / 255, b / 255])

                self.pixels.append(pixelRow)

    def getColor(self, u, v):
        # Se regresa el valor del pixel si los valores de las uv
        # están entre 0 y 1.
        if 0 <= u < 1 and 0 <= v < 1:
            return self.pixels[int(v * self.height)][int(u * self.width)]
        else:
            return None
