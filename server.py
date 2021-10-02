from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    with open('resources/swagger_example.json', 'r', encoding='utf-8') as f:
        filetext = f.read()
# todo обработка исключений чтения файла, затем вынести в функцию

    return render_template('index.html', filetext=filetext)


if __name__ == '__main__':
    app.run(debug=True)
