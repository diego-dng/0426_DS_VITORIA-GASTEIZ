import pandas as pd
from flask import request, Flask, jsonify
import sqlite3
import os

# PROBAR IMPORTANDO EL ARCHIVO "BOOKS.DB" EN "https://sqliteonline.com/"

def conexion():
    conexion = sqlite3.connect("data/books.db")
    cursor = conexion.cursor()

    return conexion, cursor

# 0.Ruta para obtener todos los libros


# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente


# 2.Ruta para obtener los libros de un autor


# 3.Ruta para añadir un libro


