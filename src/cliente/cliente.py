import socket
import sys
import os

# Ajustar el path para poder importar desde la carpeta 'comun'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from comun.protocolos import enviar_mensaje, recibir_mensaje

HOST = '127.0.0.1'
PUERTO = 65432

def enviar_nueva_tarea(titulo, descripcion, nombre_archivo=None, contenido_archivo=None):
    """Se conecta al servidor por socket para enviar una tarea."""
    print(f"Conectando al sistema distribuido en {HOST}:{PUERTO}...")
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PUERTO))
        
        # Estructuramos la petición en un formato JSON amigable
        tarea_payload = {
            "accion": "crear_tarea",
            "titulo": titulo,
            "descripcion": descripcion,
            "archivo_nombre": nombre_archivo,
            "archivo_contenido": contenido_archivo
        }
        
        print("Enviando datos de la tarea...")
        enviar_mensaje(client_socket, tarea_payload)
        
        print("Esperando respuesta del clúster de servidores...")
        respuesta = recibir_mensaje(client_socket)
        
        if respuesta:
            print(f"\n[Respuesta Servidor]: {respuesta.get('mensaje')}")
            print(f"[Estado]: {respuesta.get('status')}")
        else:
            print("❌ No se recibió respuesta del servidor.")
            
    except ConnectionRefusedError:
        print("❌ Error: No se pudo conectar al servidor. Asegúrate de que servidor.py esté corriendo.")
    finally:
        client_socket.close()
        print("Conexión finalizada.")

if __name__ == "__main__":
    print("=== CLIENTE DE GESTIÓN DE TAREAS DISTRIBUIDAS ===")
    # Ejemplo de envío de tarea con un archivo adjunto para simular S3
    enviar_nueva_tarea(
        titulo="Corregir examen de Informática",
        descripcion="Revisar los scripts distribuidos subidos por los alumnos.",
        nombre_archivo="notas_parcial.txt",
        contenido_archivo="Lista de alumnos: Facundo Rodriguez - Aprobado."
    )
