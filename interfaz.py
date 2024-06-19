import tkinter as tk
from tkinter import messagebox, filedialog
from validador import es_url_valida
from crawler import rastrear_url,cancelar_rastreo
from extraerinformacion import extraer_informacion_articulos
from guardar import guardar_resultados
import threading
import queue
import time
# Crear una cola para manejar las actualizaciones de feedback
feedback_queue = queue.Queue()

# Función para manejar el clic del botón de rastreo
def manejar_rastreo():
    sitio_web = url_entry.get()
    palabra_clave = palabra_clave_entry.get()
    max_profundidad = profundidad_entry.get()
    max_enlaces = enlaces_entry.get()

    # Validar que max_profundidad y max_enlaces sean enteros
    try:
        max_profundidad = int(max_profundidad) if max_profundidad else 2
    except ValueError:
        messagebox.showerror("Entrada inválida", "La profundidad máxima debe ser un número entero.")
        return

    try:
        max_enlaces = int(max_enlaces) if max_enlaces else 100
    except ValueError:
        messagebox.showerror("Entrada inválida", "El número máximo de enlaces debe ser un número entero.")
        return

    if es_url_valida(sitio_web):
        rastreo_button.config(state=tk.DISABLED)
        cancelar_button.grid(row=0, column=1, padx=10, pady=20)
        feedback_text.config(state=tk.NORMAL)
        feedback_text.delete('1.0', tk.END)  # Limpiar el área de feedback
        feedback_text.config(state=tk.DISABLED)
        
        # Iniciar el rastreo en un hilo separado
        threading.Thread(target=iniciar_rastreo, args=(sitio_web, palabra_clave, max_profundidad, max_enlaces)).start()
    else:
        messagebox.showerror("URL Inválida", "La URL introducida no es válida.")

def iniciar_rastreo(sitio_web, palabra_clave, max_profundidad, max_enlaces):
    global cancelar_rastreo
    cancelar_rastreo = False

    def actualizar_feedback(mensaje):
        feedback_queue.put(mensaje)

    # Comenzar el rastreo desde la página de inicio del sitio web
    enlaces = rastrear_url(url=sitio_web, palabra_clave=palabra_clave, max_profundidad=max_profundidad, max_enlaces=max_enlaces, actualizar_feedback=actualizar_feedback)
    # Verificar si se encontraron enlaces
    if enlaces:
        extraer = messagebox.askyesno("Extracción de Artículos", "¿Deseas extraer información de los sitios indexados?")
        
        if extraer:
            resultados = []
            for enlace in enlaces:
                if cancelar_rastreo:
                    print("Rastreo cancelado por el usuario.")
                    actualizar_feedback("Rastreo cancelado por el usuario.")
                    break
                print(f"Procesando enlace: {enlace}")
                actualizar_feedback(f"Procesando enlace: {enlace}")
                articulos = extraer_informacion_articulos(enlace)
                if articulos:
                    resultados.extend(articulos)
                    print(f"Artículos extraídos: {articulos}")
                    actualizar_feedback(f"Artículos extraídos: {articulos}")

            # Verificar los resultados extraídos
            print(f"Total artículos extraídos: {len(resultados)}")
            actualizar_feedback(f"Total artículos extraídos: {len(resultados)}")
            for articulo in resultados:
                print(f"Artículo: {articulo}")
                actualizar_feedback(f"Artículo: {articulo}")

            guardar = messagebox.askyesno("Guardar Resultados", "¿Deseas guardar la información extraída?")
            if guardar:
                archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], title="Guardar archivo como")
                if archivo:
                    # Guardar los resultados
                    guardar_resultados(resultados, archivo)
                    messagebox.showinfo("Resultados Guardados", f"Información de los artículos guardada en '{archivo}'.")
            else:
                messagebox.showinfo("Proceso Completo", "La información extraída no será guardada.")
        else:
            messagebox.showinfo("Proceso Completo", "No se extraerá información de los artículos indexados.")
    else:
        messagebox.showwarning("Sin Enlaces", "No se encontraron enlaces en la página principal.")
    
    cancelar_button.grid_remove()
    rastreo_button.config(state=tk.NORMAL)

# Función para actualizar el feedback desde la cola
def actualizar_feedback_desde_cola():
    while not feedback_queue.empty():
        mensaje = feedback_queue.get()
        feedback_text.config(state=tk.NORMAL)
        feedback_text.insert(tk.END, mensaje + "\n")
        feedback_text.see(tk.END)  # Desplazar al final
        feedback_text.config(state=tk.DISABLED)
    ventana.after(100, actualizar_feedback_desde_cola)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Web Crawler")

# Establecer el icono de la aplicación
ventana.iconbitmap('spider.ico')  

# Configurar estilo oscuro
ventana.configure(bg='#2E2E2E')
ventana.option_add('*Foreground', 'white')
ventana.option_add('*Background', '#2E2E2E')
ventana.option_add('*Entry.Foreground', 'white')
ventana.option_add('*Entry.Background', '#1C1C1C')
ventana.option_add('*Label.Foreground', 'white')
ventana.option_add('*Label.Background', '#2E2E2E')
ventana.option_add('*Button.Foreground', 'white')
ventana.option_add('*Button.Background', '#1C1C1C')
ventana.option_add('*Text.Foreground', 'white')
ventana.option_add('*Text.Background', '#1C1C1C')

# Fuente y estilo
fuente_titulo = ("Helvetica", 18, "bold")
fuente_labels = ("Helvetica", 12)
fuente_entry = ("Helvetica", 12)
fuente_texto = ("Helvetica", 10)
fuente_boton = ("Helvetica", 12, "bold")

# Título de la aplicación
titulo_label = tk.Label(ventana, text="Web Crawler", font=fuente_titulo, bg='#2E2E2E')
titulo_label.pack(pady=(10, 20))

# Frame para los campos de entrada
frame_campos = tk.Frame(ventana, bg='#2E2E2E')
frame_campos.pack(pady=10)

# Crear y colocar los widgets
tk.Label(frame_campos, text="URL del sitio web:", font=fuente_labels).grid(row=0, column=0, padx=10, pady=10, sticky="e")
url_entry = tk.Entry(frame_campos, width=50, font=fuente_entry)
url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_campos, text="Profundidad máxima (opcional):", font=fuente_labels).grid(row=1, column=0, padx=10, pady=10, sticky="e")
profundidad_entry = tk.Entry(frame_campos, width=10, font=fuente_entry)
profundidad_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

tk.Label(frame_campos, text="Número máximo de enlaces (opcional):", font=fuente_labels).grid(row=2, column=0, padx=10, pady=10, sticky="e")
enlaces_entry = tk.Entry(frame_campos, width=10, font=fuente_entry)
enlaces_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

tk.Label(frame_campos, text="Palabra clave (opcional):", font=fuente_labels).grid(row=3, column=0, padx=10, pady=10, sticky="e")
palabra_clave_entry = tk.Entry(frame_campos, width=20, font=fuente_entry)
palabra_clave_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Frame para los botones
frame_botones = tk.Frame(ventana, bg='#2E2E2E')
frame_botones.pack(pady=10)

rastreo_button = tk.Button(frame_botones, text="Iniciar Rastreo", command=manejar_rastreo, font=fuente_boton)
rastreo_button.grid(row=0, column=0, padx=10, pady=20)

cancelar_button = tk.Button(frame_botones, text="Cancelar Rastreo", command=cancelar_rastreo, font=fuente_boton)
cancelar_button.grid(row=0, column=1, padx=10, pady=20)
cancelar_button.grid_remove()

# Crear un área de texto para mostrar el feedback
feedback_text = tk.Text(ventana, wrap=tk.WORD, state=tk.DISABLED, height=10, width=80, font=fuente_texto)
feedback_text.pack(padx=10, pady=10)

# Iniciar la actualización del feedback desde la cola
ventana.after(100, actualizar_feedback_desde_cola)

# Ejecutar la aplicación
ventana.mainloop()