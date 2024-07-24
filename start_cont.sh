#!/bin/bash

IMAGENAME="my-flask-img"
CONTAINERNAME="my-flask-cont"
VOLUMENAME="ekatra_flask_data"
VOLUMEPATH="/home/leon/work/docker/ekatra_flask/"
APPPATH="/app"
DATAPATH="/data"
PORTHOST=8089
PORTDOCK=80

# Если был запущен, то надо остановить перед перегрузкой 
docker stop $CONTAINERNAME

sleep 2

# Создаем том для контекста, создаваемого приложением
docker volume create $VOLUMENAME


# После останова самоуничтожится
docker run  --rm \
            --name $CONTAINERNAME \
            -p $PORTHOST:$PORTDOCK \
            -v $VOLUMEPATH:$APPPATH \
            -v $VOLUMENAME:$DATAPATH \
            $IMAGENAME
