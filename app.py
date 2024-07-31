from flask import Flask, render_template, request, redirect, url_for
from flask import flash
import json
import signal
import sys

# Список категорий для ссылок на различные запоминаемые сайты
categories = ["ext_links", "info_links", "handscraft", "tutorials", "other"]

#=== Приложение Flask с поддержкой шаблонов ===================================
app = Flask(__name__)
#==============================================================================

#------------------------------------------------------------------------------

with open('key_secret.txt', 'r') as file:
    '''
    Функция, отвечающая за получение секретного ключа из файла key_secret.txt    
    '''
    secret_key = file.read().strip()

app.secret_key = secret_key

@app.context_processor
def utility_processor():
    '''
    Функция, отвечающая за обработку данных в шаблонах.
    В шаблонах можно использовать функцию repeat_nbsp(count), которая
    возвращает строку из count повторов символа &nbsp;.
    '''
    def repeat_nbsp(count):
        return '&nbsp' * count
    return dict(repeat_nbsp=repeat_nbsp)

def save_documents(documents):
    '''
    Функция сохранения документов в файл documents.json при остановке сервера
    '''
    with open('documents.json', 'w') as f:
        json.dump(documents, f)

def load_documents():
    '''
    Функция загрузки документов из файла documents.json при запуске сервера
    '''
    try:
        with open('documents.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Инициализация документов
documents = load_documents()

#------------------------------------------------------------------------------

@app.route('/')
def index():
    '''
    Это переход по ссылке http://127.0.0.1:8089/ в браузере.
    В шаблон передается список документов и количество повторов символа &nbsp;.
    '''
    return render_template('index.html', documents=documents, repeat_count=5)

@app.route('/start')
def start():
    '''
    Это переход по ссылке http://127.0.0.1:8089/start в браузере.
    В шаблон передается список ссылок на разделы сайта.
    '''
    return render_template('start.html')

@app.route('/sidebar')
def sidebar():
    '''
    Функция, отвечающая за отображение сайдбара с ссылками на разделы сайта.
    В шаблон передается список ссылок на разделы сайта в виде кнопок.
    '''
    return render_template('sidebar.html')

@app.route('/external_links')
def external_links():
    '''
    Функция, отвечающая за отображение ссылок на статической странице различных внешних сайтов.
    '''
    return render_template('external_links.html')

@app.route('/links_info')
def links_info():
    '''
    Функция, отвечающая за отображение ссылок на статической странице различных информационных сайтов.
    '''
    return render_template('links_info.html')

@app.route('/handcrafts')
def handcrafts():
    '''
    Функция, отвечающая за отображение ссылок на статической странице различных сайтов по теме iot.
    '''
    return render_template('handcrafts.html')

@app.route('/tutor')
def tutor():
    '''
    Функция, отвечающая за отображение ссылок на статической странице различных сайтов по теме tutorials.
    '''
    return render_template('tutor.html')

#------------------------------------------------------------------------

@app.route('/document/<id>')
def document(id):
    '''
    Функция, отвечающая за отображение документа по ID.
    '''
    doc = documents.get(id)
    return render_template('document.html', document=doc)

# Страница редактирования документа по ID
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    '''
    Функция, отвечающая за отображение страницы редактирования документа по ID.
    Если использован метод POST, то в шаблоне передается форма с полями для редактирования.
     Тут можно изменить текст документа по всем  его полям.
     И потом сохранить изменения функцией save_documents().
     И потом перейти на страницу документа по ID.
    Если - метод GET, то в шаблоне передается документ по ID.
    '''
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        documents[id] = {"title": title, "description": description, "content": content}
        save_documents(documents)
        return redirect(url_for('index'))
    doc = documents.get(id)
    return render_template('edit.html', document=doc)


@app.route('/add', methods=['GET', 'POST'])
def add():
    '''
    Функция, отвечающая за отображение страницы добавления документа.
    Если использован метод POST, то в шаблоне передается форма с полями для добавления.
    Иначе - в шаблон идет пустая форма для заполнения данными.
    '''
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
    '''
    Функция, отвечающая за удаление документа по ID.
    При успешном удалении документа по ID, перенаправляем пользователя на страницу документов.
    '''
    if id in documents:
        del documents[id]
        save_documents(documents)
    return redirect(url_for('index'))

#------------------------------------------------------------------------------

#=== Работа со ссылками на сайты (сохр., редакт., удаление, показ) ============

def get_links_from_database():
    '''
    Вычитываем ссылки из файла links.json в переменную links
    '''
    try:
        with open('links.json', 'r') as file:
            links = json.load(file)
        return links
    except FileNotFoundError:
        return []
    
def save_link_to_database(new_link):
    '''
    Сохраняем новую ссылку в БД (файл links.json)
    '''
    links = get_links_from_database()    
    links.append(new_link)
    with open('links.json', 'w') as file:
        json.dump(links, file, indent=2)

def update_link_in_database(index, updated_link):
    '''
    Обновляем ссылку в БД (файл links.json) после изменения данных
    '''
    links = get_links_from_database()
    links[index] = updated_link
    with open('links.json', 'w') as file:
        json.dump(links, file, indent=2)        

def delete_link_from_database(index):
    '''
    Удаляем ссылку из БД (файл links.json)
    '''
    links = get_links_from_database()
    del links[index]
    with open('links.json', 'w') as file:
        json.dump(links, file, indent=2)        

@app.route('/links')
def links():
    '''
    Функция, отвечающая за отображение страницы с ссылками.
    Зачитали все ссылки из БД и разделели по категориям.
    В цикле перебираем все ссылки и добавляем их в соответствующие категории.
    В локальный словарь добавили индекс к каждой ссылке.
    Отдаем этот словарь (по категориям) в шаблон.
    '''
    all_links = get_links_from_database()
    links_by_category = {}
    
    for index, link in enumerate(all_links):
        category = link['fld_cat']
        if category not in links_by_category:
            links_by_category[category] = []
        # Добавляем индекс к каждой ссылке
        link['index'] = index  
        links_by_category[category].append(link)
    
    return render_template('links.html', links_by_category=links_by_category)


@app.route('/add_link', methods=['GET', 'POST'])
def add_link():
    '''
    Функция, отвечающая за добавление новой ссылки.
    Сначала запрашиваем запрос на получение данных из формы.
    Сохраняем полученные данные в словаре.
    Затем добавляем новую ссылку в БД.
    Отдаем пользователю сообщение об успешном добавлении ссылки.
    Отдаем пользователю страницу с индексом ссылок.
    '''
    if request.method == 'POST':
        new_link = {
            'fld_cat': request.form['fld_cat'],
            'fld_url': request.form['fld_url'],
            'fld_dsc': request.form['fld_dsc'],
            'fld_krz': request.form['fld_krz']
        }
        save_link_to_database(new_link)
        return redirect(url_for('links'))
    return render_template('add_link.html', categories=categories)

@app.route('/edit_link/<int:index>', methods=['GET', 'POST'])
def edit_link(index):
    '''
    Функция, отвечающая за редактирование ссылки.
    Сначала запрашиваем запрос на получение данных из формы.
    Сохраняем полученные данные в словаре.
    Затем обновляем ссылку в БД.
    Отдаем пользователю сообщение об успешном обновлении ссылки.
    Отдаем пользователю страницу с индексом ссылок.
    '''
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

@app.route('/delete_link/<int:index>')
def delete_link(index):
    '''
    Функция, отвечающая за удаление ссылки по индексу.
    Удаляем ссылку из БД.
    Отдаем пользователю сообщение об успешном удалении ссылки.
    '''
    delete_link_from_database(index)
    return redirect(url_for('links'))

#==============================================================================


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

