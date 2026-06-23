from flask import request, Flask, jsonify
import sqlite3
import os
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True

def fun_sumar(num_1, num_2):
    total = num_1 + num_2
    return total

@app.route("/", methods = ["GET"])
def main():
    return "API de libros"

# 1.Ruta para obtener todos los libros
@app.route("/libros", methods = ["GET"])
def libros():
    con = sqlite3.connect("books.db")
    cursor = con.cursor()
    query = "SELECT * FROM books"
    result = cursor.execute(query).fetchall()
    con.close()

    return jsonify(result)


# 2.Ruta para obtener un libro concreto mediante su nombre de autor como parámetro en la llamada
@app.route("/buscar_libros", methods = ["GET"])
def buscar_libros():
    # http://127.0.0.1:5000/buscar_libros?nombre_autor=Paolo
    con = sqlite3.connect("books.db")
    autor = request.args["nombre_autor"]
    cursor = con.cursor()
    query = f"SELECT * FROM books WHERE author LIKE '%{autor}%'"
    result = cursor.execute(query).fetchall()
    con.close()

    return jsonify(result)

@app.route("/buscar_libros_2/<string:autor>", methods = ["GET"])
def buscar_libros_2(autor):
    # http://127.0.0.1:5000/buscar_libros_2/Paolo
    con = sqlite3.connect("books.db")
    cursor = con.cursor()
    query = f"SELECT * FROM books WHERE author LIKE '%{autor}%'"
    result = cursor.execute(query).fetchall()
    con.close()

    return jsonify(result)

@app.route("/buscar_libros_3", methods = ["GET"])
def buscar_libros_3():
    # http://127.0.0.1:5000/buscar_libros_3
    # JSON EJEMPLO:
    """
        {
        "autor":"Ann",
        }
    """
    data = request.get_json()
    autor = data.get("autor")

    con = sqlite3.connect("books.db")
    cursor = con.cursor()
    query = f"SELECT * FROM books WHERE author LIKE '%{autor}%'"
    result = cursor.execute(query).fetchall()
    con.close()

    return jsonify(result)

# 3. Ruta para añadir un libro.

@app.route("/nuevo_libro", methods = ["POST"])
def nuevo_libro():
    # http://127.0.0.1:5000/nuevo_libro?id=44&published=1994&author=Saramago&title=El doble&first_sentence=En un lugar de la Mancha...
    id = request.args["id"]
    published = request.args["published"]
    author = request.args["author"]
    title = request.args["title"]
    first_sentence = request.args["first_sentence"]
    try:
        con = sqlite3.connect("books.db")
        cursor = con.cursor()
        query = f"INSERT INTO books(id, published, author, title, first_sentence) VALUES ({id},{published},'{author}','{title}','{first_sentence}')"
        # query = f"INSERT INTO books(id, published, author, title, first_sentence) VALUES (12, 2005, 'Orwell', 1984, 'En un lugar de la Mancha...')"
        print(query)
        result = cursor.execute(query).fetchall()
        con.commit()
        con.close()
        return jsonify({"resultado":"Libro insertado correctamente"}) 


    except sqlite3.IntegrityError:
        return jsonify({"error": "Tenemos un error"}), 400
    
@app.route("/nuevo_libro_json", methods = ["POST"])
def nuevo_libro_json():
    # http://127.0.0.1:5000/nuevo_libro?id=44&published=1994&author=Saramago&title=El doble&first_sentence=En un lugar de la Mancha...
    
    """
        {
        "id": 400,
        "published":2025,
        "author": "Diego",
        "title": "La ciencia de datos",
        "first_sentence": "Python"
        }    
    """
    data = request.get_json()
    
    id = data.get("id")
    published = data.get("published")
    author = data.get("author")
    title = data.get("title")
    first_sentence = data.get("first_sentence")

    try:
        con = sqlite3.connect("books.db")
        cursor = con.cursor()
        query = f"INSERT INTO books(id, published, author, title, first_sentence) VALUES ({id},{published},'{author}','{title}','{first_sentence}')"
        # query = f"INSERT INTO books(id, published, author, title, first_sentence) VALUES (12, 2005, 'Orwell', 1984, 'En un lugar de la Mancha...')"
        print(query)
        result = cursor.execute(query).fetchall()
        con.commit()
        con.close()
        return jsonify({"resultado":"Libro insertado correctamente"}) 


    except sqlite3.IntegrityError:
        return jsonify({"error": "Tenemos un error"}), 400


    

app.run()

