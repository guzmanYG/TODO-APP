import sqlite3

conexion = sqlite3.connect("tareas.db")
cursor = conexion.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS tarea (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0
)
"""
)

tareas = [
    ("Aprender Flask",False),
    ("Estudiar Bootstrap",True),
    ("Crear API Rest",False),
    ("Leer Documentación SQLite",False),
    ("Conectar Frontend con backend",True),
    ("Añadir Navbar con Bootstrap",False)
]

cursor.executemany("INSERT INTO tarea (title,done) VALUES (?,?)",tareas)

conexion.commit()
conexion.close()

print("Base de datos creada y poblada correctamente..")