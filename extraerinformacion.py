import urllib.robotparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extraer_informacion_articulos(url):
    # Descargar la página web con el User-Agent especificado
    headers = {
        "User-Agent": "Jaime"  # Cambia esto por el User-Agent que desees usar
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"No se pudo acceder a {url}, código de estado: {response.status_code}")
        return []

    # Analizar el contenido HTML
    soup = BeautifulSoup(response.content, "html.parser")

    articulos = []

    # Buscar los artículos en la página principal
    for articulo in soup.find_all("article"):
        titulo_tag = articulo.find("h2")  # Suponiendo que los títulos están en etiquetas h2
        if titulo_tag and titulo_tag.a:
            titulo = titulo_tag.a.get_text(strip=True)
            link = titulo_tag.a["href"]
            # Construir la URL absoluta
            absolute_url = urljoin(url, link)

            resumen_tag = articulo.find("p")
            resumen = resumen_tag.get_text(strip=True) if resumen_tag else "No hay resumen disponible"

                # Agregar la información del artículo a la lista
            articulos.append({
                    "titulo": titulo,
                    "url": absolute_url,
                    "resumen": resumen
                })

    return articulos