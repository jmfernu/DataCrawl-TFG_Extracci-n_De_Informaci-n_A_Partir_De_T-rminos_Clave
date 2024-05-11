import urllib.robotparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Función para descargar y analizar el archivo robots.txt
def verificar_permiso_robots(url):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url + "/robots.txt")
    rp.read()
    return rp

# Función para rastrear una URL específica
def rastrear_url(url):
    # Descargar la página web
    response = requests.get(url)
    if response.status_code != 200:
        return

    # Analizar el contenido HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Procesar los enlaces encontrados en la página
    for link in soup.find_all("a", href=True):
        href = link["href"]
        # Construir la URL absoluta
        absolute_url = urljoin(url, href)
        # Verificar si la URL está permitida según las reglas del robots.txt
        if rp.can_fetch("*", absolute_url):
            print("Visitando:", absolute_url)
            # Aquí puedes agregar lógica adicional para procesar la URL
            # Por ejemplo, almacenar el contenido, seguir recorriendo enlaces, etc.

# URL del sitio web a rastrear
sitio_web = "https://www.ejemplo.com"
# Verificar permisos del robots.txt
rp = verificar_permiso_robots(sitio_web)
# Comenzar el rastreo desde la página de inicio del sitio web
pagina_inicio = sitio_web
rastrear_url(pagina_inicio)