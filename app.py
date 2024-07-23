from flask import Flask, render_template, request, redirect, url_for
import json
import signal
import sys

app = Flask(__name__)

@app.context_processor
def utility_processor():
    def repeat_nbsp(count):
        return '&nbsp' * count
    return dict(repeat_nbsp=repeat_nbsp)

# Функция сохранения документов в файл при остановке сервера
def save_documents(documents):
    with open('documents.json', 'w') as f:
        json.dump(documents, f)

# Загружает документы из файла при запуске сервера
def load_documents():
    try:
        with open('documents.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Инициализация документов
documents = load_documents()

# Страница с индексом документов
@app.route('/')
def index():
    return render_template('index.html', documents=documents, repeat_count=5)

# Страница с документом по ID
@app.route('/document/<id>')
def document(id):
    doc = documents.get(id)
    return render_template('document.html', document=doc)

# Страница редактирования документа по ID
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        documents[id] = {"title": title, "content": content}
        save_documents(documents)
        return redirect(url_for('index'))
    doc = documents.get(id)
    return render_template('edit.html', document=doc)

# Страница добавления документа
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_id = str(len(documents) + 1)
        title = request.form['title']
        content = request.form['content']
        documents[new_id] = {"title": title, "content": content}
        save_documents(documents)
        return redirect(url_for('index'))
    return render_template('edit.html', document={"title": "", "content": ""})

# Страница удаления документа по ID
@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    if id in documents:
        del documents[id]
        save_documents(documents)
    return redirect(url_for('index'))

# Функция для обработки сигналов остановки
def handle_shutdown(signal, frame):
    save_documents(documents)
    sys.exit(0)

signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

@app.teardown_appcontext
def save_documents_before_termination(exception=None):
    save_documents(documents)

if __name__ == '__main__':
    app.run(debug=True)

