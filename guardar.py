import json
# Guardado de los resultados en un archivo JSON
def guardar_resultados(resultados, archivo='resultados.json'):
    print(f"Guardando {len(resultados)} artículos en {archivo}")
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)