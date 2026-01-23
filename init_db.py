import sqlite3
import os

# Eliminar la base de datos existente si existe
if os.path.exists('database.db'):
    os.remove('database.db')

connection = sqlite3.connect('database.db')

with open('schema.sql', encoding='utf-8') as f:
    connection.executescript(f.read())

print("Base de datos creada e inicializada con éxito.")
connection.commit()
connection.close()