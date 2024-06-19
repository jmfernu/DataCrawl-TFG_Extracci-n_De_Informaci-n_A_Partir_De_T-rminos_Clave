import urllib.robotparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from validador import permitido_por_robots
def extraer_informacion_articulos(url):
    print(f"Extrayendo información de artículos desde: {url}")
    # Verificar si la URL está permitida según las reglas del robots.txt
    if not permitido_por_robots(url, user_agent="Jaime"):
        print(f"El acceso a {url} está prohibido por robots.txt")
        return []

    # Descargar la página web con el User-Agent especificado
    headers = {
        "User-Agent": "Juanma"  
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"No se pudo acceder a {url}, código de estado: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return []

    # Analiza el contenido HTML
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Imprime el contenido HTML para depuración
    print("Contenido HTML de la página:")
    print(soup.prettify())

    articulos = []

    # Obtener el título del artículo desde la etiqueta <title>
    titulo_tag = soup.find("title")
    if titulo_tag:
        titulo = titulo_tag.get_text(strip=True)
        print(f"Título encontrado: {titulo}")

        # Obtener el resumen del artículo desde las meta etiquetas o el cuerpo del artículo
        resumen = ""
        meta_description = soup.find("meta", attrs={"name": "description"})
        if meta_description:
            resumen = meta_description.get("content", "No hay resumen disponible")
        else:
            p_tag = soup.find("p")
            if p_tag:
                resumen = p_tag.get_text(strip=True)
            else:
                resumen = "No hay resumen disponible"

        articulo_info = {
            "titulo": titulo,
            "url": url,
            "resumen": resumen
        }
        articulos.append(articulo_info)
        print(f"Extraído: {articulo_info}")
    else:
        print(f"No se encontró el título en {url}")

    # Verificación de artículos extraídos
    if not articulos:
        print(f"No se encontraron artículos en {url}")
    else:
        print(f"Se encontraron {len(articulos)} artículos en {url}")

    return articulos