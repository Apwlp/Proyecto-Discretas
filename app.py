import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row # Esto convierte las filas en objetos similares a diccionarios
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    # ---------------------------------------------------------
    # PASO 1: TRAER LOS DATOS CRUDOS A LA MEMORIA RAM (Python)
    # ---------------------------------------------------------
    # En lugar de pedirle a SQL que procese, traemos las tablas enteras.
    
    # Convertimos a lista de diccionarios reales para manipularlos en Python
    estudiantes = [dict(row) for row in conn.execute("SELECT * FROM Estudiantes").fetchall()]
    materias    = [dict(row) for row in conn.execute("SELECT * FROM Materias").fetchall()]
    profesores  = [dict(row) for row in conn.execute("SELECT * FROM Profesores").fetchall()]
    inscripciones = [dict(row) for row in conn.execute("SELECT * FROM Inscripciones").fetchall()]
    
    conn.close() # Cerramos la conexión. A partir de aquí, todo es Python puro.

    # ---------------------------------------------------------
    # PASO 2: APLICAR ÁLGEBRA RELACIONAL CON ALGORITMOS PYTHON
    # ---------------------------------------------------------
    
    # 1. SELECCIÓN (σ): Filtrar filas
    # Algoritmo: List Comprehension con condicional (if)
    resultado_seleccion = [e for e in estudiantes if e['carrera'] == 'Computación']

    # 2. PROYECCIÓN (π): Recortar columnas
    # Algoritmo: Crear nuevos diccionarios solo con las llaves deseadas
    resultado_proyeccion = [{'nombre': e['nombre'], 'apellido': e['apellido']} for e in estudiantes]

    # 3. UNIÓN (∪): Sumar conjuntos sin duplicados
    # Algoritmo: Usar 'set' de Python para eliminar duplicados automáticamente
    nombres_est = {e['nombre'] for e in estudiantes} # Set de nombres estudiantes
    nombres_prof = {p['nombre'] for p in profesores} # Set de nombres profesores
    conjunto_union = nombres_est | nombres_prof      # Operador | es Unión en Python
    # Formateamos para la tabla HTML
    resultado_union = [{'nombre': nombre} for nombre in conjunto_union]

    # 4. DIFERENCIA (-): Elementos en A pero no en B
    # Algoritmo: Filtrar listas y restar sets
    ids_en_discretas = {i['id_estudiante'] for i in inscripciones if i['codigo_materia'] == 'MAT001'}
    ids_en_calculo   = {i['id_estudiante'] for i in inscripciones if i['codigo_materia'] == 'MAT002'}
    conjunto_diferencia = ids_en_discretas - ids_en_calculo # Operador - es Diferencia en Python
    # Formateamos
    resultado_diferencia = [{'id_estudiante': id_est} for id_est in conjunto_diferencia]

    # 5. PRODUCTO CARTESIANO (×): Combinar todos con todos
    # Algoritmo: Bucles anidados (Nested Loops)
    resultado_cartesiano = []
    for est in estudiantes:
        for mat in materias:
            # Combinamos atributos de ambos
            fila_combinada = {'nombre': est['nombre'], 'nombre_materia': mat['nombre_materia']}
            resultado_cartesiano.append(fila_combinada)
    # Recortamos a 8 para que no sea gigante en pantalla
    resultado_cartesiano = resultado_cartesiano[:8]


    # ---------------------------------------------------------
    # PASO 3: PREPARAR LA ESTRUCTURA PARA LA VISTA (HTML)
    # ---------------------------------------------------------
    demostraciones = [
        {
            "titulo": "1. Selección (σ) - Lógica Python",
            "formula": r"\sigma_{Carrera='Computación'}(Estudiantes)",
            "codigo_visible": "resultado = [e for e in estudiantes if e['carrera'] == 'Computación']",
            "descripcion": "Usamos una 'List Comprehension' con un 'if' para filtrar los datos en memoria.",
            "columnas_mostrar": ["id_estudiante", "nombre", "apellido", "carrera"],
            "datos": resultado_seleccion,
            "estado": "Procesado en Python"
        },
        {
            "titulo": "2. Proyección (π) - Lógica Python",
            "formula": r"\pi_{Nombre, Apellido}(Estudiantes)",
            "codigo_visible": "resultado = [{'nombre': e['nombre'], 'apellido': e['apellido']} for e in estudiantes]",
            "descripcion": "Construimos una nueva lista de diccionarios extrayendo solo las llaves deseadas.",
            "columnas_mostrar": ["nombre", "apellido"],
            "datos": resultado_proyeccion,
            "estado": "Procesado en Python"
        },
        {
            "titulo": "3. Unión (∪) - Lógica Python",
            "formula": r"\pi_{Nombre}(Estudiantes) \cup \pi_{Nombre}(Profesores)",
            "codigo_visible": "union = set(nombres_estudiantes) | set(nombres_profesores)",
            "descripcion": "Usamos la estructura de datos 'set' (conjunto) y el operador pipe (|) para unir y eliminar duplicados.",
            "columnas_mostrar": ["nombre"],
            "datos": resultado_union,
            "estado": "Procesado en Python"
        },
        {
            "titulo": "4. Diferencia (-) - Lógica Python",
            "formula": r"Estudiantes_{Discretas} - Estudiantes_{Cálculo}",
            "codigo_visible": "diferencia = ids_discretas - ids_calculo",
            "descripcion": "Creamos dos conjuntos de IDs y usamos el operador resta (-) nativo de Python.",
            "columnas_mostrar": ["id_estudiante"],
            "datos": resultado_diferencia,
            "estado": "Procesado en Python"
        },
        {
            "titulo": "5. Producto Cartesiano (×) - Lógica Python",
            "formula": r"Estudiantes \times Materias",
            "codigo_visible": "for e in estudiantes:\n    for m in materias:\n        lista.append(...)",
            "descripcion": "Implementamos dos bucles 'for' anidados para combinar cada estudiante con cada materia.",
            "columnas_mostrar": ["nombre", "nombre_materia"],
            "datos": resultado_cartesiano,
            "estado": "Procesado en Python"
        }
    ]

    # --- DATOS CRUDOS PARA EL VISOR DEL FINAL ---
    tablas_crudas = {
        'Estudiantes': {'columnas': list(estudiantes[0].keys()) if estudiantes else [], 'datos': estudiantes},
        'Materias': {'columnas': list(materias[0].keys()) if materias else [], 'datos': materias},
        'Profesores': {'columnas': list(profesores[0].keys()) if profesores else [], 'datos': profesores},
        'Inscripciones': {'columnas': list(inscripciones[0].keys()) if inscripciones else [], 'datos': inscripciones}
    }

    return render_template('index.html', demostraciones=demostraciones, tablas_db=tablas_crudas)

if __name__ == '__main__':
    app.run(debug=True)