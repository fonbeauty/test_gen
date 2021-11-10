from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from datetime import datetime

from webapp.tests import test_execute
from webapp.send_requests import standart_tests
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
        paths = get_paths(request)
        if paths:
            try:
                print('--- START ---')
                for endpoint in paths:
                    print('Endpoint ', endpoint)
                    path_method = []
                    for method in paths[endpoint]:
                        path_method.append(str(method).upper())
                print('Methods ', path_method)
                endpoints[endpoint] = path_method
                print(f'Endpoints with methods {endpoints}')
                standart_tests(endpoints, app.config['METHOD_LIST'], base_url)
                # save_swagger(data)
                print('--- END ---')
                return {}
            except Exception as e:
                print(f'Exception \n {e}')
                print('--- END ---')
                return {}
        else:
            print('Ошибка при обработке запроса')
    return app


def get_paths(request):
    try:
        if request.headers['Content-Type'] == 'application/json':
            data_json = request.json
            print('application/json ', data_json)
            return data_json.get('paths')
        elif request.headers['Content-Type'] == 'text/plain':
            data_yaml = yaml.load(request.data, Loader=yaml.SafeLoader)
            print('text/plain', data_yaml)
            return data_yaml.get("paths")
        else:
            print('Получен не обрабатывемый Content-Type')
            return False
    except Exception as e:
        print(f'Received not valid data type. \n Exception {e}')
        return False


def save_swagger(swagger, title='stub', author='stub'):
    swagger = Swagger(swagger=swagger, title=title, author=author, edit_date=datetime.now(), create_date=datetime.now())
    db.session.add(swagger)
    db.session.commit()
