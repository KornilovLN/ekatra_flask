#!/bin/bash

IMAGENAME="my-flask-img:latest"
CONTAINERNAME="my-flask-cont"

# Имя тома для данных
VOLUMENAME="ekatra_flask_data"

# Путь для данных на хосте (заказчик должен изменить этот путь)
DATAPATH="/путь/к/папке/для/данных"

# Порт на хосте и Порт в контейнере    
PORTHOST=8089
PORTDOCK=80

# Остановка существующего контейнера
docker stop $CONTAINERNAME

# Пауза, чтобы контейнер успел остановиться
sleep 2

# Создание тома для данных
docker volume create $VOLUMENAME

# Запуск контейнера
docker run  --rm \
            --name $CONTAINERNAME \
            -p $PORTHOST:$PORTDOCK \
            -v $VOLUMENAME:/data \
            $IMAGENAME

