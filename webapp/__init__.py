from flask import Flask, render_template, request
from datetime import datetime
import requests

from webapp.model import db, Swagger


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        with open('./resources/swagger_example.json', 'r', encoding='utf-8') as f:
            # todo обработка исключений чтения файла, затем вынести в функцию
            filetext = f.read()
        return render_template('/index.html', filetext=filetext)

    @app.route('/swagger', methods=['POST'])
    def receive_swagger():
        # todo добавить обработку исключений
        try:
            data = request.json
            print('AAAAAAAAAAAAAA')
            # print(data, '\n')
            # print('OLOLO \n', type(data))
            print("HELLO \n", data, "\n TYPE ", type(data))
            print(len(data['paths']))
            print('BBBBBBBBBBBBBB')
            print(data['paths'])
            print('CCCCCCCCCCCCCC')
            # print(data['paths']['/inventory'])
            # print(len(data['paths']['/inventory']))

            for endpoints in data['paths']:
                print('Endpoint ', endpoints)
                for method in data['paths'][endpoints]:
                    print('Method ', method)


            save_swagger(data)
        except Exception:
            print('ALARMA Received not valid data type')
        return {}
    return app


def save_swagger(swagger, title='stub', author='stub'):
    swagger = Swagger(swagger=swagger, title=title, author=author, edit_date=datetime.now(), create_date=datetime.now())
    db.session.add(swagger)
    db.session.commit()
