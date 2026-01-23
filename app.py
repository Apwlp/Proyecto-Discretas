import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# =========================================================
#  MOTOR DE ÁLGEBRA RELACIONAL (Lógica Pura en Python)
# =========================================================

def seleccionar(tabla, condicion):
    """
    Equivalente a Sigma (σ).
    Uso: seleccionar(Estudiantes, "carrera == 'Computación'")
    """
    resultado = []
    for fila in tabla:
        try:
            # Evaluamos la condición usando los datos de la fila como variables locales
            if eval(condicion, {}, fila):
                resultado.append(fila)
        except Exception:
            pass 
    return resultado

def proyectar(tabla, *columnas):
    """
    Equivalente a Pi (π).
    Uso: proyectar(Estudiantes, 'nombre', 'apellido')
    """
    resultado = []
    for fila in tabla:
        # Creamos un nuevo diccionario solo con las columnas solicitadas
        nueva_fila = {col: fila[col] for col in columnas if col in fila}
        if nueva_fila:
            resultado.append(nueva_fila)
    return resultado

def union(tabla_a, tabla_b):
    """
    Equivalente a Unión (∪).
    Uso: union(TablaA, TablaB)
    """
    # Convertimos filas a tuplas para eliminar duplicados con set()
    set_a = {tuple(fila.values()) for fila in tabla_a}
    set_b = {tuple(fila.values()) for fila in tabla_b}
    
    union_set = set_a | set_b
    
    # Recuperamos las llaves originales para reconstruir los diccionarios
    keys = list(tabla_a[0].keys()) if tabla_a else (list(tabla_b[0].keys()) if tabla_b else [])
    
    return [dict(zip(keys, valores)) for valores in union_set]

def diferencia(tabla_a, tabla_b):
    """
    Equivalente a Diferencia (-).
    Uso: diferencia(TablaA, TablaB)
    """
    res = []
    # Convertimos B a una lista de tuplas para comparar fácilmente
    filas_b = [tuple(f.values()) for f in tabla_b]
    
    for fila_a in tabla_a:
        if tuple(fila_a.values()) not in filas_b:
            res.append(fila_a)
    return res

def producto(tabla_a, tabla_b):
    """
    Equivalente a Producto Cartesiano (×).
    Uso: producto(TablaA, TablaB)
    """
    res = []
    for fila_a in tabla_a:
        for fila_b in tabla_b:
            # Fusionamos ambos diccionarios
            combinacion = {**fila_a, **fila_b} 
            res.append(combinacion)
    return res[:20] # Limitamos a 20 resultados por seguridad

# =========================================================
#  RUTAS DEL SERVIDOR
# =========================================================

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    
    # 1. CARGAR DATOS A MEMORIA RAM
    # Traemos todo de SQLite y lo convertimos a diccionarios de Python
    estudiantes = [dict(row) for row in conn.execute("SELECT * FROM Estudiantes").fetchall()]
    materias    = [dict(row) for row in conn.execute("SELECT * FROM Materias").fetchall()]
    profesores  = [dict(row) for row in conn.execute("SELECT * FROM Profesores").fetchall()]
    inscripciones = [dict(row) for row in conn.execute("SELECT * FROM Inscripciones").fetchall()]
    
    conn.close()

    # 2. INTERPRETE DE COMANDOS DEL USUARIO
    resultado_interactivo = None
    error_interactivo = None
    query_usuario = ""

    if request.method == 'POST':
        query_usuario = request.form.get('algebra_input')
        
        # Contexto donde se ejecutará el código del usuario
        contexto = {
            "Estudiantes": estudiantes, "Materias": materias, 
            "Profesores": profesores, "Inscripciones": inscripciones,
            "seleccionar": seleccionar, "proyectar": proyectar,
            "union": union, "diferencia": diferencia, "producto": producto
        }

        if query_usuario:
            try:
                # Ejecutamos el string como código Python
                resultado_crudo = eval(query_usuario, {"__builtins__": None}, contexto)
                
                if isinstance(resultado_crudo, list):
                    if len(resultado_crudo) > 0:
                        cols = list(resultado_crudo[0].keys())
                        resultado_interactivo = {"columnas": cols, "datos": resultado_crudo}
                    else:
                        resultado_interactivo = {"mensaje": "Conjunto vacío (0 resultados).", "columnas": [], "datos": []}
                else:
                    error_interactivo = "El resultado no es una lista válida."
            except Exception as e:
                error_interactivo = f"Error en la fórmula: {e}"

    # 3. GENERAR DEMOSTRACIONES AUTOMÁTICAS (Para la clase)
    
    # Demo Selección
    d_sel = seleccionar(estudiantes, "carrera == 'Computación'")
    
    # Demo Proyección
    d_pro = proyectar(estudiantes, 'nombre', 'apellido')
    
    # Demo Unión (requiere proyección previa para ser compatible)
    d_uni = union(proyectar(estudiantes, 'nombre'), proyectar(profesores, 'nombre'))
    
    # Demo Diferencia (Simulada con IDs)
    ids_mat1 = [i for i in inscripciones if i['codigo_materia'] == 'MAT001']
    ids_mat2 = [i for i in inscripciones if i['codigo_materia'] == 'MAT002']
    d_dif = diferencia(proyectar(ids_mat1, 'id_estudiante'), proyectar(ids_mat2, 'id_estudiante'))
    
    # Demo Producto
    d_prod = producto(estudiantes, materias)[:5]

    demostraciones = [
        {
            "titulo": "1. Selección (σ)",
            "formula": r"\sigma_{Carrera='Computación'}(Estudiantes)",
            "codigo": "seleccionar(Estudiantes, \"carrera == 'Computación'\")",
            "desc": "Filtra filas que cumplen la condición.",
            "cols": ["id_estudiante", "nombre", "carrera"], "datos": d_sel, "estado": "Ok"
        },
        {
            "titulo": "2. Proyección (π)",
            "formula": r"\pi_{Nombre, Apellido}(Estudiantes)",
            "codigo": "proyectar(Estudiantes, 'nombre', 'apellido')",
            "desc": "Selecciona columnas específicas.",
            "cols": ["nombre", "apellido"], "datos": d_pro, "estado": "Ok"
        },
        {
            "titulo": "3. Unión (∪)",
            "formula": r"\pi_{Nombre}(Est) \cup \pi_{Nombre}(Prof)",
            "codigo": "union(proy_estudiantes, proy_profesores)",
            "desc": "Une conjuntos eliminando duplicados.",
            "cols": ["nombre"], "datos": d_uni, "estado": "Ok"
        },
        {
            "titulo": "4. Diferencia (-)",
            "formula": r"Inscritos_{Discretas} - Inscritos_{Cálculo}",
            "codigo": "diferencia(ids_discretas, ids_calculo)",
            "desc": "Elementos del primer conjunto que no están en el segundo.",
            "cols": ["id_estudiante"], "datos": d_dif, "estado": "Ok"
        },
        {
            "titulo": "5. Producto Cartesiano (×)",
            "formula": r"Estudiantes \times Materias",
            "codigo": "producto(Estudiantes, Materias)",
            "desc": "Combina todas las filas de A con B.",
            "cols": ["nombre", "nombre_materia"], "datos": d_prod, "estado": "Ok"
        }
    ]

    # Datos base para el visor final
    tablas_db = {
        'Estudiantes': {'columnas': list(estudiantes[0].keys()) if estudiantes else [], 'datos': estudiantes},
        'Materias': {'columnas': list(materias[0].keys()) if materias else [], 'datos': materias},
        'Profesores': {'columnas': list(profesores[0].keys()) if profesores else [], 'datos': profesores},
        'Inscripciones': {'columnas': list(inscripciones[0].keys()) if inscripciones else [], 'datos': inscripciones}
    }

    return render_template('index.html', 
                           demostraciones=demostraciones, 
                           tablas_db=tablas_db,
                           resultado_interactivo=resultado_interactivo,
                           error_interactivo=error_interactivo,
                           query_usuario=query_usuario)

if __name__ == '__main__':
    app.run(debug=True)