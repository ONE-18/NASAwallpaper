import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from PIL import Image
from io import BytesIO
from os import path, mkdir, getcwdb
import ctypes


def change_wallpaper():
    if not path.exists("wallpapers"):
        mkdir("wallpapers")
    
    imagen = get_img()
    
    resolucion = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

    if True:
        # Calcular la relación de aspecto de la pantalla y la imagen
        relacion_aspecto_pantalla = resolucion[0] / resolucion[1]
        relacion_aspecto_imagen = imagen.width / imagen.height
        
        # Ajustar la imagen para que se ajuste a la pantalla sin deformarla
        if relacion_aspecto_pantalla < relacion_aspecto_imagen:
            nueva_altura = int(imagen.height * resolucion[0] / imagen.width)
            imagen = imagen.resize((resolucion[0], nueva_altura), Image.Resampling.LANCZOS)
        else:
            nueva_ancho = int(imagen.width * resolucion[1] / imagen.height)
            imagen = imagen.resize((nueva_ancho, resolucion[1]), Image.Resampling.LANCZOS)
        
        # imagen.show()
        
        # Guardar la imagen redimensionada temporalmente
        ruta_temporal = 'wallpaper_actual.bmp'
        imagen.save(ruta_temporal, 'BMP')
    
    else:
        # Calcular las coordenadas para centrar la imagen
        x = (resolucion[0] - imagen.width) // 2
        y = (resolucion[1] - imagen.height) // 2
        
        # Crear una imagen en blanco del tamaño de la pantalla
        fondo = Image.new('RGB', resolucion, (0, 0, 0))
        
        # Pegar la imagen en el centro del fondo
        fondo.paste(imagen, (x, y))
        
        fondo.show()
        
        # Guardar la imagen redimensionada temporalmente
        ruta_temporal = 'wallpaper_actual.bmp'
        fondo.save(ruta_temporal, 'BMP')
    
    # Establecer la imagen como fondo de pantalla
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path.join(path.dirname(path.abspath(__file__)), ruta_temporal), 3)
    # ctypes.windll.user32.SystemParametersInfoW(20, 0, "C:\\Users\\juang\\Desktop\\NASAwallpaper\\temp_wallpaper.bmp", 3)


def get_img():
    url = 'https://apod.nasa.gov/apod/astropix.html'
    
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        etiqueta_img = soup.find('img')
        
        url_img = etiqueta_img['src']
        
        img_desc = requests.get(urljoin(url, url_img))
        
        img = Image.open(BytesIO(img_desc.content))
        
        # img.show()
        img.save(f"wallpapers\\{datetime.now().strftime('%d_%m_%Y')}.png", "PNG")
        
        return img

if __name__ == "__main__":
    change_wallpaper()