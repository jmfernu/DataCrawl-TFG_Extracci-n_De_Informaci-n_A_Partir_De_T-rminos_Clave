import urllib.robotparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Función para rastrear una URL específica
def rastrear_url(url):
    # Descargar la página web
    headers = {
        "User-Agent": "Jaime"  # Cambia esto por el User-Agent que desees usar
    }

    # Descargar la página web con el User-Agent especificado
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return

    # Analizar el contenido HTML para luego sacar los links
    soup = BeautifulSoup(response.content, "html.parser")

    # Procesar los enlaces encontrados en la página
    for link in soup.find_all("a", href=True):
        href = link["href"]
        # Construir la URL absoluta
        absolute_url = urljoin(url, href)
        # Verificar si la URL está permitida según las reglas del robots.txt
        print("Visitando:", absolute_url)
            # Aquí puedes agregar lógica adicional para procesar la URL
            # Por ejemplo, almacenar el contenido, seguir recorriendo enlaces, etc.

# URL del sitio web a rastrear
sitio_web = "https://www.marca.com"
# Comenzar el rastreo desde la página de inicio del sitio web
pagina_inicio = sitio_web
rastrear_url(pagina_inicio)