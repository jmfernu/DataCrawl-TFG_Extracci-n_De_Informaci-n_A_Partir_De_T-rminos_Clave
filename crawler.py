
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin 
from validador import  permitido_por_robots, es_url_valida
import time


# Variable global para controlar la cancelación del rastreo
cancelar_rastreo = False
# Función para rastrear una URL específica con límite de profundidad y cantidad de enlaces
def rastrear_url(url, palabra_clave, max_profundidad=2, max_enlaces=100, actualizar_feedback=None):
    global cancelar_rastreo
    cancelar_rastreo = False

    enlaces_a_visitar = [(url, 0)]
    enlaces_visitados = set()
    enlaces_resultantes = set()

    while enlaces_a_visitar and len(enlaces_resultantes) < max_enlaces:
        if cancelar_rastreo:
            print("Rastreo cancelado por el usuario.")
            if actualizar_feedback:
                actualizar_feedback("Rastreo cancelado por el usuario.")
            break

        current_url, profundidad = enlaces_a_visitar.pop(0)
        mensaje = f"Visitando: {current_url} (Profundidad: {profundidad})"
        print(mensaje)
        if actualizar_feedback:
            actualizar_feedback(mensaje)

        if current_url in enlaces_visitados or profundidad > max_profundidad:
            continue

        enlaces_visitados.add(current_url)

        # Verificar si la URL está permitida según las reglas del robots.txt
        if not permitido_por_robots(current_url, user_agent="Jaime"):
            mensaje = f"El acceso a {current_url} está prohibido por robots.txt"
            print(mensaje)
            if actualizar_feedback:
                actualizar_feedback(mensaje)
            continue

        # Descarga las páginas con el User-Agent especificado
        headers = {
            "User-Agent": "Juanma"  
        }
        try:
            response = requests.get(current_url, headers=headers)
            if response.status_code != 200:
                mensaje = f"No se pudo acceder a {current_url}, código de estado: {response.status_code}"
                print(mensaje)
                if actualizar_feedback:
                    actualizar_feedback(mensaje)
                continue
        except requests.RequestException as e:
            mensaje = f"Error al acceder a {current_url}: {e}"
            print(mensaje)
            if actualizar_feedback:
                actualizar_feedback(mensaje)
            continue

        # Analiza el contenido HTML de la url para luego sacar los links a las siguientes
        soup = BeautifulSoup(response.content, "html.parser")

        # Buscar la palabra clave en el contenido de la página
        if palabra_clave.lower() in soup.get_text().lower() and current_url not in enlaces_resultantes:
            enlaces_resultantes.add(current_url)

        # Procesar los enlaces encontrados en la página
        for link in soup.find_all("a", href=True):
            if len(enlaces_resultantes) >= max_enlaces:
                break

            href = link["href"]
            absolute_url = urljoin(current_url, href)
            if (es_url_valida(absolute_url) and absolute_url not in enlaces_visitados and
                (palabra_clave.lower() in href.lower() or palabra_clave.lower() in link.get_text(strip=True).lower())):
                enlaces_a_visitar.append((absolute_url, profundidad + 1))
                

        # Retardo entre solicitudes
        time.sleep(1)

    return list(enlaces_resultantes)

def cancelar_rastreo():
    global cancelar_rastreo
    cancelar_rastreo = True