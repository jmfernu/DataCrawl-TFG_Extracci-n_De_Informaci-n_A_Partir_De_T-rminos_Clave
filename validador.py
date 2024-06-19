from urllib.parse import  urlparse
import urllib
def es_url_valida(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ["http", "https"] and parsed_url.netloc != ""

def permitido_por_robots(url, user_agent='*'):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(base_url)
    rp.read()
    return rp.can_fetch(user_agent, url)