import socket
import os
import sys
from concurrent.futures import ThreadPoolExecutor

# Ajustamos el path para poder importar desde la carpeta 'comun'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from comun.protocolos import recibir_mensaje, enviar_mensaje
from conexion_db import inicializar_db, guardar_tarea

HOST = '127.0.0.1'
PUERTO = 65432
MAX_WORKERS = 4  # Tamaño de nuestro Pool de Hilos (Workers)
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "storage")

# Asegura que existan las carpetas simuladas
os.makedirs(STORAGE_DIR, exist_ok=True)

def worker_atender_tarea(conn, addr):
    """Esta función es ejecutada por un hilo del Pool para procesar la petición."""
    print(f"[Pool de Hilos] Hilo asignado para atender a la conexión {addr}")
    
    try:
        peticion = recibir_mensaje(conn)
        if peticion and peticion.get("accion") == "crear_tarea":
            titulo = peticion.get("titulo")
            descripcion = peticion.get("descripcion")
            archivo_nombre = peticion.get("archivo_nombre")
            archivo_contenido = peticion.get("archivo_contenido")
            
            # 1. Simula e interactua con la Cola de Mensajes (RabbitMQ)
            print("[RabbitMQ] Mensaje de sincronización publicado en la cola de workers.")
            
            # 2. Si viene un archivo, se guarda simulando AWS S3
            if archivo_nombre and archivo_contenido:
                print(f"[AWS S3] Subiendo archivo '{archivo_nombre}' al bucket de objetos...")
                ruta_s3 = os.path.join(STORAGE_DIR, archivo_nombre)
                with open(ruta_s3, "w", encoding="utf-8") as f:
                    f.write(archivo_contenido)
                print("[AWS S3] Archivo almacenado de forma distribuida.")

            # 3. Guardar datos estructurados en SQLite (Simulando PostgreSQL)
            guardar_tarea(titulo, descripcion, archivo_nombre)
            
            # Responder al cliente
            respuesta = {"status": "OK", "mensaje": f"Tarea '{titulo}' registrada con éxito en el sistema distribuido."}
            enviar_mensaje(conn, respuesta)
        else:
            enviar_mensaje(conn, {"status": "ERROR", "mensaje": "Acción no válida o datos corruptos."})
            
    except Exception as e:
        print(f"❌ Error procesando petición de {addr}: {e}")
    finally:
        conn.close()
        print(f"Conexión con {addr} cerrada. Hilo liberado al Pool.")

def iniciar_servidor():
    inicializar_db()
    
    # Configuramos el servidor Socket nativo
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PUERTO))
    server_socket.listen()
    
    # Inicializamos el Pool de Hilos distribuido (Workers)
    pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    print(f"Servidor Worker escuchando en {HOST}:{PUERTO}")
    print(f"Pool de hilos activo configurado con {MAX_WORKERS} workers independientes.")
    
    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"\nNueva conexión entrante desde el Balanceador de Carga simulado: {addr}")
            # Delegamos la tarea al Pool de hilos inmediatamente
            pool.submit(worker_atender_tarea, conn, addr)
    except KeyboardInterrupt:
        print("\nApagando el servidor distribuido de forma ordenada...")
    finally:
        server_socket.close()
        pool.shutdown()

if __name__ == "__main__":
    iniciar_servidor()
    