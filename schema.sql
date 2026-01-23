DROP TABLE IF EXISTS Estudiantes;
DROP TABLE IF EXISTS Materias;
DROP TABLE IF EXISTS Profesores;
DROP TABLE IF EXISTS Inscripciones;

-- Conjuntos Básicos
CREATE TABLE Estudiantes (
    id_estudiante INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    carrera TEXT NOT NULL
);

CREATE TABLE Materias (
    codigo_materia TEXT PRIMARY KEY,
    nombre_materia TEXT NOT NULL,
    creditos INTEGER NOT NULL
);

CREATE TABLE Profesores (
    id_profesor INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    departamento TEXT NOT NULL
);

-- Relación (Inscripciones)
CREATE TABLE Inscripciones (
    id_inscripcion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_estudiante INTEGER,
    codigo_materia TEXT,
    nota_final REAL,
    FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante),
    FOREIGN KEY (codigo_materia) REFERENCES Materias(codigo_materia)
);

-- DATOS DE PRUEBA (Seeds)

-- Estudiantes
INSERT INTO Estudiantes VALUES (1, 'Carlos', 'Salazar', 'Computación');
INSERT INTO Estudiantes VALUES (2, 'David', 'Cheing', 'Computación');
INSERT INTO Estudiantes VALUES (3, 'Gerson', 'López', 'Auditoría');
INSERT INTO Estudiantes VALUES (4, 'Jordi', 'Gaibor', 'Computación');

-- Profesores (Para probar Unión)
INSERT INTO Profesores VALUES (1, 'Cristhian', 'Matemáticas');
INSERT INTO Profesores VALUES (2, 'Carlos', 'Física'); -- Note: 'Carlos' se repite en Estudiantes (para probar Unión)

-- Materias
INSERT INTO Materias VALUES ('MAT001', 'Matemáticas Discretas', 4);
INSERT INTO Materias VALUES ('MAT002', 'Cálculo I', 5);

-- Inscripciones (Para probar Diferencia)
-- Carlos ve ambas
INSERT INTO Inscripciones (id_estudiante, codigo_materia, nota_final) VALUES (1, 'MAT001', 8.5);
INSERT INTO Inscripciones (id_estudiante, codigo_materia, nota_final) VALUES (1, 'MAT002', 7.0);
-- David solo ve Discretas
INSERT INTO Inscripciones (id_estudiante, codigo_materia, nota_final) VALUES (2, 'MAT001', 9.0);