import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    # Aquí definimos la "Traducción" de Álgebra a SQL
    demostraciones = [
        {
            "id": "seleccion",
            "titulo": "1. Selección (σ)",
            "formula": r"\sigma_{Carrera='Computación'}(Estudiantes)",
            "sql_query": "SELECT * FROM Estudiantes WHERE carrera = 'Computación';",
            "descripcion": "Filtra las tuplas (filas) que cumplen con un predicado lógico.",
            "columnas_mostrar": ["id_estudiante", "nombre", "apellido", "carrera"]
        },
        {
            "id": "proyeccion",
            "titulo": "2. Proyección (π)",
            "formula": r"\pi_{Nombre, Apellido}(Estudiantes)",
            "sql_query": "SELECT nombre, apellido FROM Estudiantes;",
            "descripcion": "Extrae columnas específicas, reduciendo la dimensión vertical de la relación.",
            "columnas_mostrar": ["nombre", "apellido"]
        },
        {
            "id": "union",
            "titulo": "3. Unión (∪)",
            "formula": r"\pi_{Nombre}(Estudiantes) \cup \pi_{Nombre}(Profesores)",
            "sql_query": "SELECT nombre FROM Estudiantes UNION SELECT nombre FROM Profesores;",
            "descripcion": "Combina conjuntos. Note cómo 'Carlos' aparece solo una vez aunque esté en ambas tablas (propiedad de conjuntos).",
            "columnas_mostrar": ["nombre"]
        },
        {
            "id": "diferencia",
            "titulo": "4. Diferencia (-)",
            "formula": r"Estudiantes_{Discretas} - Estudiantes_{Cálculo}",
            "sql_query": "SELECT id_estudiante FROM Inscripciones WHERE codigo_materia = 'MAT001' EXCEPT SELECT id_estudiante FROM Inscripciones WHERE codigo_materia = 'MAT002';",
            "descripcion": "Muestra IDs de estudiantes en Discretas que NO están en Cálculo. (En SQL estándar se usa EXCEPT o MINUS).",
            "columnas_mostrar": ["id_estudiante"]
        },
        {
            "id": "cartesiano",
            "titulo": "5. Producto Cartesiano (×)",
            "formula": r"Estudiantes \times Materias",
            "sql_query": "SELECT nombre, nombre_materia FROM Estudiantes CROSS JOIN Materias LIMIT 8;",
            "descripcion": "Combina cada estudiante con cada materia. (Limitado a 8 filas para visualización).",
            "columnas_mostrar": ["nombre", "nombre_materia"]
        }
    ]

    # Ejecutar las consultas dinámicamente
    resultados_finales = []
    for demo in demostraciones:
        try:
            cursor = conn.execute(demo['sql_query'])
            datos = cursor.fetchall()
            demo['datos'] = datos
            demo['estado'] = 'ok'
        except Exception as e:
            demo['datos'] = []
            demo['estado'] = f'Error: {e}'
        resultados_finales.append(demo)

    conn.close()
    return render_template('index.html', demostraciones=resultados_finales)

if __name__ == '__main__':
    app.run(debug=True)