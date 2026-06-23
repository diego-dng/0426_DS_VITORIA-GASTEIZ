from flask import Flask, jsonify, request
from datos_dummy import books


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods = ['GET'])
def inicio():
    return "Inicio de la API de libros"

# http://127.0.0.1:5000/

# 1.Ruta para obtener todos los libros

@app.route('/books', methods = ['GET'])
def libros():
    return jsonify(books)

# http://127.0.0.1:5000/books

# 2.Ruta para obtener un libro concreto mediante su id como parámetro en la llamada
@app.route('/book_id', methods = ['GET'])
def book_id():
    #return request.args["id"]
    id = int(request.args["id"])
    for i in books:
        if i["id"] == id:
            result = i
            print(result)
            return result

# http://127.0.0.1:5000/book_id?id=0

# 3.Ruta para obtener un libro concreto mediante su título como parámetro en la llamada de otra forma
@app.route('/books_nombre_0/<string:title>', methods = ['GET'])
def books_nombre_0(title):
    for i in books:
        if i['title'] == title:
            result = i
            return result

# http://127.0.0.1:5000/books_nombre_3/A Fire Upon the Deep

@app.route('/books_nombre_3', methods = ['GET'])
def books_nombre_1():
    title = request.args["title"]
    for i in books:
        if i['title'] == title:
            result = i
            return result
#  http://127.0.0.1:5000/books_nombre_3?title=A Fire Upon the Deep       


# 4.Ruta para obtener un libro concreto mediante su titulo dentro del cuerpo de la llamada  
@app.route('/books_nombre_2', methods=["GET"])
def books_nombre_2():
    title = request.get_json().get('title', None)
    for i in books:
        if i["title"] == title:
            result = i
            return result
"""
{
    "title" : "A Fire Upon the Deep"
}
"""

# 5.Ruta para añadir un libro mediante un json en la llamada
@app.route("/add_book_0", methods = ['POST'])
def add_book():
    data = request.get_json()
    books.append(data)
    return books
"""
    {'id': 3,
     'title': '1984',
     'author': 'Orwell',
     'first_sentence': 'En un lugar de la Mancha.',
     'published': '2024'}
"""

# 6.Ruta para añadir un libro mediante parámetros
@app.route("/add_book_1", methods = ['POST'])
def add_book_1():
    book = {}
    book['id'] = int(request.args['id'])
    book['title'] = request.args['title']
    book['author'] = request.args['author']
    book['first_sentence'] = request.args['first_sentence']
    book['published'] = request.args['published']

    books.append(book)

    return books
# http://127.0.0.1:5000/add_book_1?id=4&title=harry potter&author=la mujer racista&first_sentence=harry eres mago&published=1984

@app.route("/modi_book", methods = ['PUT'])
def modi_book():
    id = int(request.args['id'])
    print("fsdfasdfdsasvdavdsavsdv", id)
    title = request.args.get('title', None)
    author = request.args.get('author', None)

    for i in books:
        if i["id"] == id:
            if title:
                i['title'] = title
            if author:
                i['author'] = author
    return books
# http://127.0.0.1:5000/modi_book?id=0&title=Romeo y Julieta&author=Antonio Lobato

# 8.Ruta para eliminar un libro

@app.route("/delete_book", methods = ['DELETE'])
def delete_book():
    id = int(request.args['id'])
    for i in books:
        if i['id'] == id:


            books.remove(i)

    return books
# http://127.0.0.1:5000/delete_book?id=0

app.run()

