from flask import Flask, render_template, request
from datetime import datetime
from webapp.tests import test_execute
from webapp.send_requests import standart_tests
from webapp.forms import LoginForm


from webapp.model import db, Swagger


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/login')
    def login():
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)


    @app.route('/')
    def index():
        with open('./resources/swagger_example.json', 'r', encoding='utf-8') as f:
            # todo обработка исключений чтения файла, затем вынести в функцию
            filetext = f.read()
        return render_template('/index.html', filetext=filetext)

    @app.route('/swagger', methods=['POST'])
    def receive_swagger():
        # todo добавить обработку исключений
        endpoints = {}
        try:
            data = request.json
            print('AAAAAAAAAAAAAA')
            print("HELLO \n", data, "\n TYPE ", type(data))
            print(len(data['paths']))
            print('BBBBBBBBBBBBBB')
            print(data['paths'])
            print('CCCCCCCCCCCCCC')

            for endpoint in data['paths']:
                print('Endpoint ', endpoint)
                pathMethod = []
                for method in data['paths'][endpoint]:
                    pathMethod.append(str(method).upper())
                    print('Methods ', pathMethod)

                    # querys = [] здесь идет перебор по параметрам эндпоинта, пока не реализовно
                    # headers = []
                    # try:
                    #     for parameter in data['paths'][endpoint][method]['parameters']:
                    #         # print('Parameter ', parameter)
                    #         requestElement = parameter['in']
                    #         print(f'Элемент запроса {requestElement}')
                    #         if requestElement == 'query':
                    #             querys.append(requestElement)
                    #         elif requestElement == 'header':
                    #             headers.append(requestElement)
                    #
                    # except(BaseException):
                    #     print(f'Ошибка: у метода {str(method).upper()} нет parameters')
                    # test_execute((app.config['BASE_URL'] + endpoint), method, querys, headers)
                    # print(f'Querys {querys}')
                    # print(f'Headers {headers}')
            endpoints[endpoint] = pathMethod
            print(f'Endpoints with methods {endpoints}')
            standart_tests(endpoints, app.config['METHOD_LIST'], app.config['BASE_URL'])

            # save_swagger(data)
        except Exception:
            print('ALARMA Received not valid data type')
        print('END ------------------')
        return {}

    return app


def save_swagger(swagger, title='stub', author='stub'):
    swagger = Swagger(swagger=swagger, title=title, author=author, edit_date=datetime.now(), create_date=datetime.now())
    db.session.add(swagger)
    db.session.commit()
