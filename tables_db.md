## Таблицы для базы данных к сайту IVL-Documents-Managament (IVL-DM)
**_Информация из источника: https://habr.com/ru/articles/754400/_**

#### База данных приложения (dbIVLDM)

**_Создать базу dbIVLDM_**
```
#python
import sqlite3

# Создаем подключение к базе данных (файл my_database.db будет создан)
connection = sqlite3.connect('dbIVLDM.db')

'''
connection.close()
```

#### Таблица пользователей tb_users

**_Поля и индексы в таблице_**
```
'''
cursor = connection.cursor()

# Создаем таблицу tbUsers
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id          INTEGER PRIMARY KEY,
access      TEXT NOT NULL,
username    TEXT NOT NULL,
position    TEST NOT NULL,
email       TEXT NOT NULL,
github      TEXT,
tel         TEXT NOT NULL, 
age         INTEGER      
)
''')

# Создаем индекс для столбца "email"
cursor.execute('CREATE INDEX idx_email ON tbUsers (email)')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
```

**_Вставка новых данных в таблицу_**
```
...
...

# Добавляем нового пользователя
cursor.execute('INSERT INTO Users (access,username,position,email,github,tel,age)
                       VALUES (?, ?, ?, ?, ?, ?, ?)',
                              ('user',
                               'Marks Karl',
                               'developer',
                               'marks.karl@ekatra.io',
                               'github.com/KarlMarks',
                               '+380 66 980 5577')
              )

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
```

**_Выполнение запросов_**
<br>Например - всю таблицу dbUsers

```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем всех пользователей
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()

# Выводим результаты
for user in users:
  print(user)

# Закрываем соединение
connection.close()
```

#### Примеры других операторов
<br>Примеры операторов SELECT, FROM, WHERE

**_Оператор SELECT позволяет выбрать определенные столбцы из таблицы:_**
```
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем имена и возраст пользователей старше 25 лет
cursor.execute('SELECT username, age 
                FROM Users
                WHERE age > ?', (25,)
              )
results = cursor.fetchall()

for row in results:
  print(row)

connection.close()
```

**_Примеры операторов GROUP BY и HAVING_**
<br>Оператор GROUP BY используется для группировки данных по определенным столбцам.
<br>Оператор HAVING применяется к агрегатным функциям, чтобы фильтровать результаты групп.
```
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Получаем средний возраст пользователей для каждого возраста
cursor.execute('SELECT age, AVG(age) FROM Users GROUP BY age')
results = cursor.fetchall()

for row in results:
  print(row)
  
# Фильтруем группы по среднему возрасту больше 30
cursor.execute('SELECT age, AVG(age) FROM Users GROUP BY age HAVING AVG(age) > ?', (30,))
filtered_results = cursor.fetchall()
for row in filtered_results:
  print(row)

connection.close()
```

**_Примеры оператора ORDER BY_**
<br>Оператор ORDER BY используется для сортировки результатов по указанным столбцам:
```
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем и сортируем пользователей по возрасту по убыванию
cursor.execute('SELECT username, age FROM Users ORDER BY age DESC')
results = cursor.fetchall()

for row in results:
  print(row)

connection.close()
```

#-------------------------------------------------------------------------------------

**_Примеры комбинирования операторов_**
<br>Можно комбинировать операторы для выполнения более сложных запросов.
<br>Например, выберем пользователей, у которых средний возраст в группе больше 30:
```
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем и сортируем пользователей по возрасту по убыванию
cursor.execute('''
SELECT username, age, AVG(age)
FROM Users
GROUP BY age
HAVING AVG(age) > ?
ORDER BY age DESC
''', (30,))
results = cursor.fetchall()

for row in results:
  print(row)

connection.close()
```

#### Использование агрегатных функций: COUNT, SUM, AVG, MIN, MAX
<br>Агрегатные функции позволяют вычислять значения по группам данных или над всей таблицей.
<br>Давайте рассмотрим каждую из агрегатных функций на примерах.

**_COUNT - подсчет количества записей_**
<br>Функция COUNT используется для подсчета количества записей в столбце или таблице.
```
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Подсчет общего числа пользователей
cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()[0]

print('Общее количество пользователей:', total_users)
connection.close()
```

**_SUM - суммирование числовых значений_**
<br>Функция SUM вычисляет сумму числовых значений в столбце.
```
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Вычисление суммы возрастов пользователей
cursor.execute('SELECT SUM(age) FROM Users')
total_age = cursor.fetchone()[0]

print('Общая сумма возрастов пользователей:', total_age)
connection.close()
```

**_AVG - вычисление среднего значения_**
<br>Функция AVG вычисляет среднее значение числовых данных в столбце.
```
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Вычисление среднего возраста пользователей
cursor.execute('SELECT AVG(age) FROM Users')
average_age = cursor.fetchone()[0]

print('Средний возраст пользователей:', average_age)
connection.close()
```

**_MIN - нахождение минимального значения_**
<br>Функция MIN находит минимальное значение в столбце.
```
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Нахождение минимального возраста
cursor.execute('SELECT MIN(age) FROM Users')
min_age = cursor.fetchone()[0]

print('Минимальный возраст среди пользователей:', min_age)
connection.close()
```

**_MAX - нахождение максимального значения_**
<br>Функция MAX находит максимальное значение в столбце.
```
import sqlite3
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Нахождение максимального возраста
cursor.execute('SELECT MAX(age) FROM Users')
max_age = cursor.fetchone()[0]

print('Максимальный возраст среди пользователей:', max_age)
connection.close()
```

#### Примеры сложных запросов с объединением таблиц и подзапросами
<br>Для выполнения сложных запросов можно использовать объединение таблиц и подзапросы.

**_Например, давайте найдем пользователей с наибольшим возрастом:_**
```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Находим пользователей с наибольшим возрастом
cursor.execute('''
SELECT username, age
FROM Users
WHERE age = (SELECT MAX(age) FROM Users)
''')
oldest_users = cursor.fetchall()

# Выводим результаты
for user in oldest_users:
  print(user)
  
# Закрываем соединение
connection.close()
```

**_Получение результатов запроса в виде списка кортежей_**
<br>Результаты запросов обычно возвращаются в виде списка кортежей.
<br>Каждый кортеж представляет собой строку данных.

**_Давайте выведем результаты запроса на выборку всех пользователей:_**
```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем всех пользователей
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()

# Выводим результаты
for user in users:
  print(user)
  
# Закрываем соединение
connection.close()
```

#### Использование методов fetchone(), fetchmany() и fetchall() для получения данных
<br>Кроме того, вы можете использовать методы:
* fetchone(),
* fetchmany() и
* fetchall()
<br>для получения данных по одной строке,нескольким строкам или всем строкам соответственно.
```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем первого пользователя
cursor.execute('SELECT * FROM Users')
first_user = cursor.fetchone()
print(first_user)

# Выбираем первых 5 пользователей
cursor.execute('SELECT * FROM Users')
first_five_users = cursor.fetchmany(5)
print(first_five_users)

# Выбираем всех пользователей
cursor.execute('SELECT * FROM Users')
all_users = cursor.fetchall()
print(all_users)

# Закрываем соединение
connection.close()
```

#### Преобразование результатов в более удобные структуры данных (списки, словари)
<br>Для удобства обработки данных, вы можете преобразовать результаты запросов
<br>в более удобные структуры данных, такие как списки или словари.

**_Давайте преобразуем результаты запроса на выборку всех пользователей в список словарей:_**
```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем всех пользователей
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()

# Преобразуем результаты в список словарей
users_list = []
for user in users:
  user_dict = {
    'id': user[0],
    'username': user[1],
    'email': user[2],
    'age': user[3]
  }
users_list.append(user_dict)

# Выводим результаты
for user in users_list:
  print(user)

# Закрываем соединение
connection.close()
```

#### Обработка NULL-значений
<br>NULL - это специальное значение, обозначающее отсутствие данных.
<br>При обработке NULL-значений, вы можете использовать операторы IS NULL и IS NOT NULL.

**_Например, давайте выберем пользователей с неизвестным возрастом:_**
```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем пользователей с неизвестным возрастом
cursor.execute('SELECT * FROM Users WHERE age IS NULL')
unknown_age_users = cursor.fetchall()

# Выводим результаты
for user in unknown_age_users:
  print(user)

# Закрываем соединение
connection.close()
```

#### Транзакции и управление данными
<br>Транзакции - это группы операций, выполняемых как единое целое.
<br>Они обеспечивают надежность и целостность данных, гарантируя,
<br>что либо все операции будут выполнены успешно,
<br>либо ни одна из них не будет применена.

**_Использование операторов BEGIN, COMMIT и ROLLBACK_**
<br>Операторы BEGIN, COMMIT и ROLLBACK позволяют управлять транзакциями в SQLite.
<br>Оператор BEGIN начинает транзакцию, COMMIT подтверждает изменения, а ROLLBACK отменяет транзакцию.
```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

try:
    # Начинаем транзакцию
    cursor.execute('BEGIN')

    # Выполняем операции
    cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', ('user1', 'user1@example.com'))
    cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', ('user2', 'user2@example.com'))

    # Подтверждаем изменения
    cursor.execute('COMMIT')

except:
    # Отменяем транзакцию в случае ошибки
    cursor.execute('ROLLBACK')

# Закрываем соединение
connection.close()
```

**_Автоматическое управление транзакциями с помощью контекстных менеджеров_**
<br>Python предоставляет контекстные менеджеры, которые автоматически управляют транзакциями.
<br>Это обеспечивает более безопасное и читаемое управление данными. Давайте рассмотрим пример:
```
import sqlite3

# Устанавливаем соединение с базой данных
with sqlite3.connect('my_database.db') as connection:
    cursor = connection.cursor()

    try:
        # Начинаем транзакцию автоматически
        with connection:
            # Выполняем операции
            cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', ('user3', 'user3@example.com'))
            cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', ('user4', 'user4@example.com'))

    except:
        # Ошибки будут приводить к автоматическому откату транзакции
        pass
```

#### Роли ACID (Atomicity, Consistency, Isolation, Durability) в транзакционных операциях
<br>Транзакционные операции следуют принципам ACID:
* Atomicity (Атомарность): Транзакция либо выполняется полностью, либо не выполняется совсем.
* Consistency (Согласованность): Транзакция переводит базу данных из одного согласованного состояния в другое.
* Isolation (Изолированность): Транзакции выполняются независимо друг от друга, как если бы они выполнялись последовательно.
* Durability (Долговечность): После завершения транзакции изменения сохраняются даже при сбое системы.

#### Продвинутые концепции
<br>Использование подготовленных (prepared) запросов для повышения производительности

<br>Подготовленные запросы позволяют многократно выполнять SQL-запросы с разными параметрами,
```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем подготовленный запрос
query = 'SELECT * FROM Users WHERE age > ?'
cursor.execute(query, (25,))
users = cursor.fetchall()

# Выводим результаты
for user in users:
  print(user)
  
# Закрываем соединение
connection.close()
```

**_Работа с представлениями (views) для упрощения сложных запросов_**
<br>Представления позволяют создавать виртуальные таблицы,
<br>которые являются результатом выполнения SQL-запроса.
<br>Это упрощает выполнение сложных запросов.
<br>Давайте создадим представление для выбора активных пользователей:
```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем представление для активных пользователей
cursor.execute('CREATE VIEW ActiveUsers AS SELECT * FROM Users WHERE is_active = 1')

# Выбираем активных пользователей
cursor.execute('SELECT * FROM ActiveUsers')
active_users = cursor.fetchall()

# Выводим результаты
for user in active_users:
  print(user)
  
# Закрываем соединение
connection.close()
```

**_Создание триггеров для автоматизации операций при изменении данных_**
<br>Триггеры - это специальные хранимые процедуры, которые автоматически вызываются при изменении данных в таблице.
<br>Давайте создадим триггер для автоматического обновления времени создания пользователя:
```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Создаем триггер для обновления времени создания при вставке новой записи
cursor.execute('''
CREATE TRIGGER IF NOT EXISTS update_created_at
AFTER INSERT ON Users
BEGIN
UPDATE Users SET created_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
```

**_Работа с индексами для оптимизации запросов_**
<br>Индексы позволяют ускорить выполнение запросов к базе данных.
<br>Давайте создадим индекс для ускорения поиска пользователей по имени:
```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем индекс для столбца "username"
cursor.execute('CREATE INDEX idx_username ON Users (username)')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
```

#### Примеры использования
<br>Создание простого приложения для управления задачами с использованием SQLite и Python
```
Давайте рассмотрим пример создания простого приложения для управления задачами
с использованием базы данных SQLite и языка программирования Python.
В приложении мы будем хранить список задач с их статусами.
```
```
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('tasks.db')
cursor = connection.cursor()

# Создаем таблицу Tasks
cursor.execute('''
CREATE TABLE IF NOT EXISTS Tasks (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
status TEXT DEFAULT 'Not Started'
)
''')

# Функция для добавления новой задачи
def add_task(title):
  cursor.execute('INSERT INTO Tasks (title) VALUES (?)', (title,))
  connection.commit()
  
# Функция для обновления статуса задачи
def update_task_status(task_id, status):
  cursor.execute('UPDATE Tasks SET status = ? WHERE id = ?', (status, task_id))
  connection.commit()
  
# Функция для вывода списка задач
def list_tasks():
  cursor.execute('SELECT * FROM Tasks')
  tasks = cursor.fetchall()
  for task in tasks:
    print(task)
    
# Добавляем задачи
add_task('Подготовить презентацию')
add_task('Закончить отчет')
add_task('Подготовить ужин')

# Обновляем статус задачи
update_task_status(2, 'In Progress')

# Выводим список задач
list_tasks()

# Закрываем соединение
connection.close()
```

#### Заключение
```
В этом туториале мы рассмотрели основы работы с базой данных SQLite в языке программирования Python.
Вы узнали, как создавать и управлять таблицами, выполнять запросы, использовать транзакции
и применять продвинутые концепции для оптимизации и упрощения работы с данными.
SQLite предоставляет мощные инструменты для управления данными внутри ваших приложений,
делая их более эффективными и надежными.
```
