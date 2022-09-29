# Система оценки мнений
Система мнений

Установка Docker Ubuntu
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04





# Установка базы данных PostgreSQL через Docker

Загрузка образа postgresql из репозитория 
> docker pull postgres




Запуск контейнера с бд
> docker run --name multiverse -p 5477:5432 -e POSTGRES_DB=c137 -e POSTGRES_USER=rick -e POSTGRES_PASSWORD=plumbus -d postgres

> docker run --name multiverse --ip 172.17.0.4 --restart=always -p 5477:5432 -e POSTGRES_DB=c137 -e POSTGRES_USER=rick -e POSTGRES_PASSWORD=plumbus -d multiverse_with_scritpts
*(больше параметров, не совсем свежийmultiverse)



Данные:
host "172.17.0.4" (проверить через docker inspect multiverse | grep IPAddress )

port "5432"

maintenance database "c137"

username "rick"

password "plumbus"






# Установка pgAdmin 4 Web (если нужно)
Загрузка образа pgAdmin из репозитория 
> docker pull dpage/pgadmin4




Запуск контейнера с бд
> docker run --name pg_dashboard -p 5488:80 -e PGADMIN_DEFAULT_EMAIL=rick@sanchez.com -e PGADMIN_DEFAULT_PASSWORD=pickleriick -d dpage/pgadmin4

Here you can log into the pgAdmin4 using the above "email" and "password":
- "rick@sanchez.com"
- "pickleriick"







# Установка библиотек
### 0. Весь контейнер
(сюда напиши команды для установки питона и пипа)
> apt install nano
>
> apt-get update
>
> apt-get -y install nano (нано нужно, без него никуда)

команды для правильного запуска скриптов, с сохранением логов

> python3 parsing.py > parsing_logs/log.log 2> parsing_logs/error.log &
> 
> python3 toxic.py > toxic_logs/log.log 2> toxic_logs/error.log &


### 1. toxic.py

> pip install pandas 

> pip install transformers[torch]

### 2. parcing.py

> pip install vk_api
> 
> pip install psycopg2 (если не сработало, то pip install psycopg2-binary)

# Парсинг данных групg VK:
* Риа
* ТАСС
* Регнум
### 3. В контейнере с веб приложением выполнить программу
> import nltk
> 
> nltk.download('stopwords')
