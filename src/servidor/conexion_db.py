import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "tareas_distribuidas.db")

def inicializar_db():
    """Crea la tabla de tareas si no existe."""
    print("[PostgreSQL] Verificando tablas en la base de datos distribuida...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            archivo_adjunto TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_tarea(titulo, descripcion, archivo_nombre=None):
    """Inserta una nueva tarea simulando persistencia en PostgreSQL."""
    print(f"[PostgreSQL] Insertando tarea: '{titulo}'...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tareas (titulo, descripcion, archivo_adjunto) VALUES (?, ?, ?)",
        (titulo, descripcion, archivo_nombre)
    )
    conn.commit()
    conn.close()
    print("[PostgreSQL] Transacción confirmada exitosamente.")
    