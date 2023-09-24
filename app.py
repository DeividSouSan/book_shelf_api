import json
from os import getcwd
from os.path import isfile
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

current_directory = getcwd()
db_file_path = f"{current_directory}/mock/db.json"

if isfile(db_file_path):
    print('Arquivo existe')
else:
    print('Arquivo não existe.')

    with open("mock/db.json", "w") as db:
        db.write('{}')
        print('Arquivo criado.')


@app.route("/")
def index():
    return 'API funcionando corretamente'


@app.route("/books", methods=['GET'])
def all_books():
    with open('mock/db.json', 'r') as db:
        data = db.read()
        data_json = json.loads(data)

    response = jsonify(data_json)
    return response


@app.route("/books/<id>", methods=['GET'])
def get_book(id: int = 0):
    with open('mock/db.json', 'r') as db:
        data = db.read()
        books_dict: dict = json.loads(data)

    try:
        current_book = books_dict[id]
    except:
        return jsonify("erro: Não existe livro com o ID forncecido."), 400

    response = jsonify(current_book)
    return response


@app.route('/books', methods=['POST'])
def insert_book():
    # Captura todos os dados do DB e transforma em um Dict
    with open("mock/db.json", "r") as db:
        db_data = db.read()
        books_data: dict = json.loads(db_data)

    if db_data == "{}":
        new_book_data: dict = request.get_json()
        next_id = 1
        books_data[next_id] = new_book_data
    else:
        # Pega o JSON do livro inserido e adiciona ao DB Dict
        new_book_data: dict = request.get_json()
        next_id = int(list(books_data.keys())[-1]) + 1
        books_info_array = list(books_data.values())

        for book_info in books_info_array:
            if new_book_data['title'] == book_info['title']:
                return jsonify("error: Já existe um livro com esse nome!"), 400
            else:
                books_data[next_id] = new_book_data

    # Abre o DB e adiciona o novo Dict convertido em JSON
    with open("mock/db.json", "w") as db:
        data_str = json.dumps(books_data)
        db.write(data_str)

    response = jsonify(new_book_data)
    return response


@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    with open("mock/db.json", "r") as db:
        db_data = db.read()
        books_data: dict = json.loads(db_data)

    try:
        removed_book = books_data[id]
        del books_data[id]
    except:
        return jsonify("erro: ID passado não pertence a nenhum livro."), 400

    with open("mock/db.json", "w") as db:
        data_str = json.dumps(books_data)
        db.write(data_str)

    response = jsonify(removed_book)
    return response


@app.route('/books', methods=['PUT'])
def update_index():
    with open('mock/db.json', "r") as db:
        db_data = db.read()
        books_data: dict = json.loads(db_data)

    new_books_data = dict()
    id = 1

    for book in books_data.values():
        new_books_data[id] = book
        id += 1

    with open('mock/db.json', "w") as db:
        new_books_data_str = json.dumps(new_books_data)
        db.write(new_books_data_str)

    response = jsonify(new_books_data)
    return response


if __name__ == '__main__':
    app.run(debug=True)
