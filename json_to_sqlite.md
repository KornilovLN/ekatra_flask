## Миграция приложения от применения json к sqlite базе данных

### Заменить JSON-файлы на базу данных в приложении на Flask, варианты:

1. PostgreSQL

    Преимущества: Сложные SQL-запросы, транзакции, индексы. Подходит для структурированных данных.
    Минусы: сложнее настроить и администрировать, чем json.

2. SQLite

    Преимущества: Простая настройка, файл в качестве базы данных, что похоже на JSON.
    Минусы: Ограничена функциональность при больших объемах данных и сложных запросах.

3. MySQL

    Преимущества: Хорошо известна и широко используется, мощная поддержка запросов и индексов.
    Минусы: Требует больше ресурсов и настройки по сравнению с SQLite.

4. MongoDB

    Преимущества: Документно-ориентированная NoSQL база, для хранения неструктур. данных (JSON-объектов).
    Минусы: Нет поддержки SQL-запросов, менее строгие транзакции.

5. Redis

    Преимущества: Очень быстрая, отлично подходит для кэша, очередей и временных данных.
    Минусы: Ограниченная поддержка структурированных данных, не подходит для сложных реляционных задач.

### Пример перехода на SQLite:

Для перехода на SQLite нужно будет:

* Создать базу данных.
* Написать функции для работы с ней вместо работы с JSON.
* Изменить маршруты Flask, чтобы они взаимодействовали с базой данных.

**_Пример кода:_**

<br>python
```
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Создаем соединение с базой данных
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    documents = conn.execute('SELECT * FROM documents').fetchall()
    conn.close()
    return render_template('index.html', documents=documents)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO documents (title, description, content) VALUES (?, ?, ?)',
                         (title, description, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('add.html')

# Функции для редактирования, удаления и просмотра документов аналогичны

if __name__ == '__main__':
    app.run(debug=True)
```

**_Для создания базы данных:_**

<br>python
```
import sqlite3

connection = sqlite3.connect('database.db')

with connection:
    connection.execute(
        '''CREATE TABLE documents (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               description TEXT,
               content TEXT NOT NULL
           );'''
    )
```

#### Этот пример показывает,

<br>как перейти с JSON-файлов на использование базы данных SQLite,
<br>сохранив общую логику работы приложения.
<br>Можно адаптировать его под любую другую базу данных,
<br>заменив соответствующие функции работы с SQLite на соответствующие функции для работы с выбранной СУБД.
