import pandas as pd
from flask import request, Flask, jsonify
import sqlite3
import os

# PROBAR IMPORTANDO EL ARCHIVO "BOOKS.DB" EN "https://sqliteonline.com/"

def conexion():
    conexion = sqlite3.connect("data/books.db")
    cursor = conexion.cursor()

    return conexion, cursor

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods = ["GET"])
def main():
    return "API libros" 

# 0.Ruta para obtener todos los libros
@app.route("/libros", methods = ["GET"])
def libros():
    con, cur = conexion()
    cur.execute("select * from books")
    libros = cur.fetchall()
    con.close()
    #return jsonify({"libro": resp})
    return jsonify(libros)

# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route("/cont_libros", methods = ["GET"])
def cont_libros():
    con, cur = conexion()
    cur.execute("select author, COUNT(*) from books GROUP by author ORDER by count(*) desc")
    resp = cur.fetchall()
    con.close()
    return jsonify(resp)

# 2.Ruta para obtener los libros de un autor

@app.route("/buscar_autor", methods = ["GET"])
def buscar_titulo():
    autor = request.args["autor"]
    con, cur = conexion()
    consulta = f"SELECT * FROM books WHERE author = '{autor}'"
    cur.execute(consulta)
    resp = cur.fetchall()
    con.close()
    return jsonify(resp)

# 3.Ruta para añadir un libro
@app.route("/insert_libro", methods = ["POST"])
def insert():
    #id, published, author, title, first_sentence
    id = request.args["id"]
    published = request.args["fecha"]
    author = request.args["autor"]
    title = request.args["titulo"]
    first_sentence = request.args["frase"]

    con, cur = conexion()
    cur.execute(f"INSERT into books values({id}, {published},'{author}', '{title}', '{first_sentence}')")
    resp = cur.fetchall()
    con.close()
    return jsonify({"resp": True})
#/insert_libro?id=3000&fecha=2030&autor=Andreea&title=La vida del bootcamp&frase=Confia en el proceso


app.run()