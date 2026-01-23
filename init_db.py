import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql', encoding='utf-8') as f:
    connection.executescript(f.read())

print("Base de datos creada e inicializada con éxito.")
connection.commit()
connection.close()