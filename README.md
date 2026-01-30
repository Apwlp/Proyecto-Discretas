# Proyecto: Equivalencia entre Álgebra Relacional y SQL

Este proyecto web busca demostrar de manera interactiva cómo las operaciones del álgebra relacional (Selección, Proyección, Unión, etc.) se traducen a consultas SQL funcionales.

---

## Tecnologías Utilizadas
* ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python 3.12**
* ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) **Flask** (Micro-framework para el backend)
* ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white) **SQLite3** (Motor de base de datos)

---

## Guía de Instalación y Ejecución

Sigue estos pasos para desplegar el proyecto localmente:

### 1. Preparar el entorno
Es importante de asegurarse de que no haya una base de datos previa para evitar conflictos de esquemas. Si existe el archivo `database.db`, elimínalo manualmente o usa la terminal:

```bash
# En Windows (CMD/PowerShell)
del database.db

# En Bash (Git Bash/Linux/macOS)
rm -f database.db

# Inicializar la Base de Datos
python init_db.py

# Iniciar el servidor local
python app.py

```
