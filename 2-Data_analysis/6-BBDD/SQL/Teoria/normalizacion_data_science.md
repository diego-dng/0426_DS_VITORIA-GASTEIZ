# Guía Completa de Normalización de Bases de Datos
## Conceptos y Fases para Data Scientists

Aunque la normalización es un concepto tradicional de la ingeniería de bases de datos relacionales (SQL), entenderlo es **fundamental** por tres razones clave:
1. **Calidad del Dato:** Evita inconsistencias y anomalías que arruinarían cualquier modelo de Machine Learning.
2. **Eficiencia en Consultas:** Optimiza el almacenamiento y acelera los `JOIN` y agregaciones en bases de datos de producción.
3. **Diseño de Features:** Entender cómo se relacionan los datos en su origen te permite realizar un mejor *Feature Engineering*.

---

## 1. ¿Qué es la Normalización?

La **normalización** es el proceso de organizar los datos de una base de datos relacional para lograr dos objetivos principales:
* **Minimizar la redundancia:** Evitar que el mismo dato esté duplicado en múltiples lugares.
* **Maximizar la integridad:** Asegurar que las dependencias de los datos tengan sentido lógico (evitando problemas al insertar, actualizar o eliminar registros).

El proceso consiste en descomponer tablas grandes y complejas en tablas más pequeñas y conectarlas mediante **Claves Foráneas (Foreign Keys)**.

### Las 3 Anomalías que queremos evitar:
* **Anomalía de Inserción:** No poder añadir información porque falta otra parte de los datos.
* **Anomalía de Actualización:** Cambiar un dato en un registro pero olvidar cambiarlo en su copia de otra fila, generando datos contradictorios.
* **Anomalía de Eliminación:** Borrar un registro y perder accidentalmente información crucial que no queríamos borrar.

---

## 2. El Estado Inicial: Tabla No Normalizada (0FN)

Imaginemos que extraemos un reporte crudo de las ventas de un bootcamp de un archivo de Excel o una base de datos mal diseñada:

| ID_Alumno | Nombre_Alumno | Telefono | Curso | Id_Profesor | Nombre_Profesor | Tutorias_Agendadas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 101 | Ana Gómez | 555-1234 | Data Science, Python | P201 | Carlos Pérez | 2026-05-20, 2026-05-22 |
| 102 | Luis Martínez | 555-5678 | Data Science | P201 | Carlos Pérez | 2026-05-21 |
| 103 | María López | 555-9012 | Web Dev | P202 | Laura Ruiz | NULL |

*Problemas visibles:*
* Celdas con múltiples valores (ej. Ana cursa "Data Science, Python" y tiene dos tutorías).
* Redundancia (El nombre "Carlos Pérez" se repite innecesariamente).

---

## 3. Las Fases de la Normalización (Formas Normales)

Para normalizar, aplicamos una serie de reglas llamadas **Formas Normales (FN)**. Cada fase es acumulativa (para estar en 2FN, primero debes cumplir la 1FN).

### 1ª Forma Normal (1FN): Atomicidad y Claves
**Reglas:**
1. Los datos de cada columna deben ser **atómicos** (un solo valor indivisible por celda).
2. No debe haber grupos ni listas repetidas.
3. Se debe definir una **Clave Primaria (Primary Key)** única.

**Transformación a 1FN:**
Rompemos las listas en filas independientes y elegimos una clave primaria compuesta (`ID_Alumno` + `Curso` + `Tutoria`).

| ID_Alumno (PK) | Curso (PK) | Tutoria (PK) | Nombre_Alumno | Telefono | Id_Profesor | Nombre_Profesor |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 101 | Data Science | 2026-05-20 | Ana Gómez | 555-1234 | P201 | Carlos Pérez |
| 101 | Data Science | 2026-05-22 | Ana Gómez | 555-1234 | P201 | Carlos Pérez |
| 101 | Python | NULL | Ana Gómez | 555-1234 | NULL | NULL |
| 102 | Data Science | 2026-05-21 | Luis Martínez | 555-5678 | P201 | Carlos Pérez |
| 103 | Web Dev | NULL | María López | 555-9012 | P202 | Laura Ruiz |

*¿Qué logramos?* Todo es atómico.
*¿Cuál es el problema?* ¡La redundancia empeoró muchísimo! El nombre de Ana y el del profesor Carlos se repiten muchas veces.

---

### 2ª Forma Normal (2FN): Dependencia Funcional Completa
**Reglas:**
1. Cumplir con la **1FN**.
2. **Eliminar dependencias parciales:** Todos los atributos que no forman parte de la clave primaria deben depender de *toda* la clave primaria, no solo de una parte de ella.

*Análisis:* En nuestra tabla 1FN, la Clave Primaria es compuesta (`ID_Alumno`, `Curso`, `Tutoria`). 
* El `Nombre_Alumno` solo depende de `ID_Alumno`, no le importa el `Curso` ni la `Tutoria`. Esto es una dependencia parcial.

**Transformación a 2FN:**
Separamos las entidades en sus propias tablas independientes.

#### Tabla: Alumnos
| ID_Alumno (PK) | Nombre_Alumno | Telefono |
| :--- | :--- | :--- |
| 101 | Ana Gómez | 555-1234 |
| 102 | Luis Martínez | 555-5678 |
| 103 | María López | 555-9012 |

#### Tabla: Cursos_Profesores
| Curso (PK) | Id_Profesor | Nombre_Profesor |
| :--- | :--- | :--- |
| Data Science | P201 | Carlos Pérez |
| Python | NULL | NULL |
| Web Dev | P202 | Laura Ruiz |

#### Tabla: Alumnos_Cursos_Tutorias (Tabla Puente / Hechos)
| ID_Alumno (FK) | Curso (FK) | Tutoria |
| :--- | :--- | :--- |
| 101 | Data Science | 2026-05-20 |
| 101 | Data Science | 2026-05-22 |
| 101 | Python | NULL |
| 102 | Data Science | 2026-05-21 |
| 103 | Web Dev | NULL |

---

### 3ª Forma Normal (3FN): Eliminar Dependencias Transitivas
**Reglas:**
1. Cumplir con la **2FN**.
2. **Eliminar dependencias transitivas:** Ningún atributo no primario debe depender de otro atributo no primario. Todo debe depender *únicamente* de la clave primaria (Como decía el famoso lema de bases de datos: *"The key, the whole key, and nothing but the key"*).

*Análisis:* Observemos la tabla `Cursos_Profesores`. La PK es `Curso`.
* `Id_Profesor` depende de `Curso` (Bien).
* `Nombre_Profesor` depende de `Id_Profesor` (¡Dependencia Transitiva!). Si el ID del profesor cambia, cambia el nombre, pero ninguno es la clave de la tabla.

**Transformación a 3FN:**
Separamos los profesores a su propia entidad.

#### Tabla: Alumnos (Se queda igual)
| ID_Alumno (PK) | Nombre_Alumno | Telefono |
| :--- | :--- | :--- |

#### Tabla: Profesores
| Id_Profesor (PK) | Nombre_Profesor |
| :--- | :--- |
| P201 | Carlos Pérez |
| P202 | Laura Ruiz |

#### Tabla: Cursos
| Curso (PK) | Id_Profesor (FK) |
| :--- | :--- |
| Data Science | P201 |
| Python | NULL |
| Web Dev | P202 |

#### Tabla: Alumnos_Cursos_Tutorias (Se queda igual)

---

## 4. Resumen Visual de Conceptos

* **0FN:** Todo mezclado en una gran sábana de datos.
* **1FN:** Datos limpios y atómicos, pero con filas duplicadas.
* **2FN:** Separamos por conceptos grandes (Alumnos por un lado, Cursos por el otro).
* **3FN:** Eliminamos dependencias indirectas (Separamos Profesores de los Cursos).

---

## 5. El Dilema del Data Scientist: ¿Normalizar o Desnormalizar?

Aunque para una base de datos transaccional (OLTP) la **3FN** es el estándar de oro, en Data Science y Big Data nos encontramos muy seguido con la **Desnormalización**:

| Criterio | Normalización (3FN) | Desnormalización (Data Warehouses / OLAP) |
| :--- | :--- | :--- |
| **Uso Principal** | Aplicaciones en vivo, e-commerce, apps. | Analítica, Dashboards, Machine Learning. |
| **Ventaja** | Cero redundancia, inserciones ultra rápidas. | Consultas (`SELECT`) hiper veloces, sin `JOINs` complejos. |
| **Desventaja** | Requiere múltiples `JOINs` para analizar. | Duplicidad de datos, mayor gasto de almacenamiento. |

