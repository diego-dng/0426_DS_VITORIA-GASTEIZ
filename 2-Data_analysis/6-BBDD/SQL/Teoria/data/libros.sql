-- Tabla de autores
CREATE TABLE Autor (
  id_autor INT PRIMARY KEY,
  nombre VARCHAR(100),
  nacionalidad VARCHAR(50)
);

-- Tabla de libros
CREATE TABLE Libro (
  id_libro INT PRIMARY KEY,
  titulo VARCHAR(150),
  id_autor INT,
  FOREIGN KEY (id_autor) REFERENCES Autor(id_autor)
);

-- Tabla de usuarios
CREATE TABLE Usuario (
  id_usuario INT PRIMARY KEY,
  nombre VARCHAR(100),
  email VARCHAR(100)
);

-- Tabla de préstamos
CREATE TABLE Prestamo (
  id_prestamo INT PRIMARY KEY,
  id_libro INT,
  id_usuario INT,
  fecha_prestamo DATE,
  FOREIGN KEY (id_libro) REFERENCES Libro(id_libro),
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- Autores
INSERT INTO Autor VALUES (1, 'Gabriel García Márquez', 'Colombiana');
INSERT INTO Autor VALUES (2, 'J.K. Rowling', 'Británica');

-- Libros
INSERT INTO Libro VALUES (1, 'Cien Años de Soledad', 1);
INSERT INTO Libro VALUES (2, 'El Amor en los Tiempos del Cólera', 1);
INSERT INTO Libro VALUES (3, 'Harry Potter y la Piedra Filosofal', 2);

-- Usuarios
INSERT INTO Usuario VALUES (1, 'Ana Pérez', 'ana@email.com');
INSERT INTO Usuario VALUES (2, 'Juan Gómez', 'juan@email.com');

-- Préstamos
INSERT INTO Prestamo VALUES (1, 1, 1, '2024-05-01');
INSERT INTO Prestamo VALUES (2, 3, 2, '2024-05-03');