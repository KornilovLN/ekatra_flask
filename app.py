from flask import Flask, render_template, request, redirect, url_for
from flask import flash
import json
import signal
import sys

app = Flask(__name__)

# Получить секретный ключ для дальнейшей работы приложения
with open('key_secret.txt', 'r') as file:
    secret_key = file.read().strip()

app.secret_key = secret_key

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
        title = request.form['title']
        content = request.form['content']

        if not title.strip():
            return render_template('add.html', error="Title cannot be empty", document={"title": title, "content": content})

        new_id = str(max(map(int, documents.keys())) + 1) if documents else "1"

        documents[new_id] = {"title": title, "content": content}
        save_documents(documents)

        flash('Document added successfully', 'success')
        return redirect(url_for('index'))
    
    # эта строка сработает при GET запросе
    # Это происходит, когда пользователь просто открывает страницу добавления документа,
    # но еще не отправил форму.
    # Эта строка отображает пустую форму, готовую к заполнению новыми данными.
    # Это правильное поведение для инициализации страницы добавления нового документа.
    return render_template('add.html', document={"title": "", "content": ""})

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

