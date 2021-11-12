from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from datetime import datetime

from webapp.tests import test_execute
from webapp.send_requests import execute_standart_tests
from webapp.forms import LoginForm
from webapp.model import db, Swagger, User
import yaml


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('index'))

        flash('Неправильные имя или пароль пользователя')
        return redirect(url_for('login'))

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ'
        else:
            return 'Ты не админ'

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
        base_url = request.args.get('adress', 'http://127.0.0.1:5000')
        print(f"Адрес для запроса {base_url}")
        swagger_dict = get_swagger_dict(request)
        security_dict = get_security(swagger_dict)
        print(f'Значение секции security_schemes  {security_dict}')
        if swagger_dict:
            paths_dict = swagger_dict.get('paths', False)
            if paths_dict:
                try:
                    print('--- START ---')
                    for endpoint in paths_dict:
                        print('Endpoint ', endpoint)
                        path_method = []
                        for method in paths_dict[endpoint]:
                            path_method.append(str(method).upper())
                    # print('Methods ', path_method)
                    endpoints[endpoint] = path_method
                    print(f'Endpoints with methods {endpoints}')
                    execute_standart_tests(endpoints, app.config['METHOD_LIST'], base_url, security_dict)
                    print('--- END ---')
                    return {}
                except Exception as e:
                    print(f'Exception \n {e}')
                    print('--- END ---')
                    return {}
            else:
                print('Ошибка - не найдена секция paths в спецификации')
        else:
            print('Ошибка при обработке спецификации')

    return app


def get_swagger_dict(request):
    try:
        if request.headers['Content-Type'] == 'application/json':
            data_json = request.json
            print('application/json', data_json)
            return data_json
        elif request.headers['Content-Type'] == 'text/plain':
            data_yaml = yaml.load(request.data, Loader=yaml.SafeLoader)
            print('text/plain', data_yaml)
            return data_yaml
        else:
            print('Получен не обрабатывемый Content-Type')
            return False
    except Exception as e:
        print(f'Received not valid data type. \n Exception {e}')
        return False


def get_security(swagger):
    security = swagger.get('components', False).get('securitySchemes', False)
    return security


def save_swagger(swagger, title='stub', author='stub'):
    swagger = Swagger(swagger=swagger, title=title, author=author, edit_date=datetime.now(), create_date=datetime.now())
    db.session.add(swagger)
    db.session.commit()
