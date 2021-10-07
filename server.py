from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    with open('resources/swagger_example.json', 'r', encoding='utf-8') as f:
        # todo обработка исключений чтения файла, затем вынести в функцию
        filetext = f.read()
    return render_template('index.html', filetext=filetext)


@app.route('/swagger', methods=['POST'])
def receive_swagger():
    # todo добавить обработку исключений
    data = request.json
    print("HELLO ", data)
    return {}


if __name__ == '__main__':
    app.run(debug=True)
