import urllib.robotparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin , urlparse
from validador import es_url_valida
from extraerinformacion import extraer_informacion_articulos
# Función para rastrear una URL específica
def rastrear_url(url):
    # Descargar la página web
    headers = {
        "User-Agent": "Jaime"  # Cambia esto por el User-Agent que desees usar
    }

    # Descargar la página web con el User-Agent especificado
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"No se pudo acceder a {url}, código de estado: {response.status_code}")
        return

    # Analizar el contenido HTML para luego sacar los links
    soup = BeautifulSoup(response.content, "html.parser")
    enlaces = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        # Construir la URL absoluta
        absolute_url = urljoin(url, href)
        # Verificar si la URL está permitida según las reglas del robots.txt
        
        print("Visitando:", absolute_url)
        enlaces.append(absolute_url)
        

    return enlaces

# URL del sitio web a rastrear
sitio_web = input("Introduce la URL del sitio web a rastrear: ")

#Validación de url introducida
if es_url_valida(sitio_web):
# Comenzar el rastreo desde la página de inicio del sitio web
    enlaces = rastrear_url(sitio_web)
    # Preguntar al usuario si desea extraer información(Esto más adelante se incorporará en la interfaz gráfica)
    extraer_info = input("¿Deseas extraer información de los artículos indexados? (sí/no): ").strip().lower()
    if extraer_info == 'sí' or extraer_info == 'si':
        for enlace in enlaces:
            articulos = extraer_informacion_articulos(enlace)
            for articulo in articulos:
                print(f"Título: {articulo['titulo']}")
                print(f"URL: {articulo['url']}")
                print(f"Resumen: {articulo['resumen']}\n")
    else:
        print("No se extraerá información de los artículos.")
else:
    print("La URL introducida no es válida")