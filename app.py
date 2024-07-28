from flask import Flask, render_template, request, redirect, url_for
from flask import flash
import json
import signal
import sys

categories = ["ext_links", "info_links", "handscraft", "tutorials", "other"]

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

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/sidebar')
def sidebar():
    return render_template('sidebar.html')

@app.route('/external_links')
def external_links():
    return render_template('external_links.html')

@app.route('/links_info')
def links_info():
    return render_template('links_info.html')

@app.route('/handcrafts')
def handcrafts():
    return render_template('handcrafts.html')

@app.route('/tutor')
def tutor():
    return render_template('tutor.html')

#------------------------------------------------------------------------------

def get_links_from_database():
    try:
        with open('links.json', 'r') as file:
            links = json.load(file)
        return links
    except FileNotFoundError:
        return []
    
def save_link_to_database(new_link):
    links = get_links_from_database()    
    links.append(new_link)
    with open('links.json', 'w') as file:
        json.dump(links, file, indent=2)
"""
def update_link_in_database(updated_link):
    links = get_links_from_database()
    for i, link in enumerate(links):
        if link['id'] == updated_link['id']:
            links[i] = updated_link
            break
    with open('links.json', 'w') as file:
        json.dump(links, file, indent=2)
"""
def update_link_in_database(index, updated_link):
    links = get_links_from_database()
    links[index] = updated_link
    with open('links.json', 'w') as file:
        json.dump(links, file, indent=2)        

"""
def delete_link_from_database(id):
    links = get_links_from_database()
    links = [link for link in links if link['id'] != id]
    with open('links.json', 'w') as file:
        json.dump(links, file, indent=2)
"""
def delete_link_from_database(index):
    links = get_links_from_database()
    del links[index]
    with open('links.json', 'w') as file:
        json.dump(links, file, indent=2)        

@app.route('/links')
def links():
    # Получение списка ссылок из базы данных
    links = get_links_from_database()
    return render_template('links.html', links=links)

@app.route('/add_link', methods=['GET', 'POST'])
def add_link():
    if request.method == 'POST':
        # Обработка данных формы
        new_link = {
            'fld_cat': request.form['fld_cat'],
            'fld_url': request.form['fld_url'],
            'fld_dsc': request.form['fld_dsc'],
            'fld_krz': request.form['fld_krz']
        }
        # Сохранение новой ссылки в базу данных
        save_link_to_database(new_link)
        return redirect(url_for('links'))
    return render_template('add_link.html', categories=categories)

"""
@app.route('/edit_link/<int:id>', methods=['GET', 'POST'])
def edit_link(id):
    # Получение ссылки из базы данных по id
    link = next((link for link in get_links_from_database() if link['id'] == id), None)
    if request.method == 'POST':
        # Обновление данных ссылки
        link['fld_cat'] = request.form['fld_cat']
        link['fld_url'] = request.form['fld_url']
        link['fld_dsc'] = request.form['fld_dsc']
        link['fld_krz'] = request.form['fld_krz']
        # Сохранение обновленной ссылки в базу данных
        update_link_in_database(link)
        return redirect(url_for('links'))
    return render_template('edit_link.html', link=link, categories=categories)
"""
@app.route('/edit_link/<int:index>', methods=['GET', 'POST'])
def edit_link(index):
    links = get_links_from_database()
    link = links[index]
    if request.method == 'POST':
        link['fld_cat'] = request.form['fld_cat']
        link['fld_url'] = request.form['fld_url']
        link['fld_dsc'] = request.form['fld_dsc']
        link['fld_krz'] = request.form['fld_krz']
        update_link_in_database(index, link)
        return redirect(url_for('links'))
    return render_template('edit_link.html', link=link, categories=categories, index=index)

"""
@app.route('/delete_link/<int:id>')
def delete_link(id):
    # Удаление ссылки из базы данных
    delete_link_from_database(id)
    return redirect(url_for('links'))
"""

@app.route('/delete_link/<int:index>')
def delete_link(index):
    delete_link_from_database(index)
    return redirect(url_for('links'))

#------------------------------------------------------------------------

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
        description = request.form['description']
        content = request.form['content']
        documents[id] = {"title": title, "description": description, "content": content}
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
        description = request.form['description']

        if not title.strip():
            return render_template('add.html', error="Title cannot be empty", document={"title": title, "content": content})

        new_id = str(max(map(int, documents.keys())) + 1) if documents else "1"

        documents[new_id] = {"title": title, "description": description, "content": content}
        save_documents(documents)

        flash('Document added successfully', 'success')
        return redirect(url_for('index'))
    
    # эта строка сработает при GET запросе
    # Это происходит, когда пользователь просто открывает страницу добавления документа,
    # но еще не отправил форму.
    # Эта строка отображает пустую форму, готовую к заполнению новыми данными.
    # Это правильное поведение для инициализации страницы добавления нового документа.
    return render_template('add.html', document={"title": "", "description": "", "content": ""})

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

