#---------------------------------------------------------------------
# образ Docker с тегом my-image, содержащий базовый python:3.12-slim
# Nginx, Git и Midnight Commander.
# Файлы приложения Flask в директории app/
#---------------------------------------------------------------------
# docker build -t my-flask-img .            #--- сборка my-flask-img
# docker run -p 8086:80 my-flask-img        #--- запустить контейнер#
# docker run --rm --name my-flask-cont -p 8086:80 -v /home/leon/work/docker/ekatra_flask/:/app my-flask-img
#---------------------------------------------------------------------
# Используем базовый образ Python 3.12
FROM python:3.12-slim

# Обновляем список пакетов и устанавливаем необходимые пакеты
RUN apt-get update && \
    apt-get install -y nginx docker.io git mc && \
    rm -rf /var/lib/apt/lists/*

# Копируем файл requirements.txt
COPY requirements.txt /app/requirements.txt

# Обновляем pip, setuptools и wheel
RUN pip install --upgrade pip setuptools wheel

# Устанавливаем зависимости Python через pip
RUN pip install -r /app/requirements.txt

# Копируем файлы приложения в контейнер
# Если заглушить, то будут использоваться из подключенного тома 
# какой надо будет указать в скрипте запуска контейнера
# Например так: -v ekatra_flask_data:/data
# COPY . /app/  

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем конфигурационный файл Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Открываем порт для Nginx
EXPOSE 80

# Запускаем Nginx и Flask приложение при старте контейнера
CMD ["sh", "-c", "nginx && gunicorn -b 0.0.0.0:5000 app:app"]


