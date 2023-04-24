### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Smitona/api_final_yatube.git
```
```
cd yatube_api
```

Создать и активировать вирутальное окружение с версией python 3.9:
```
py -3.9 venv venv
```

```
. venv/Scripts/activate
```

Установить необходимы зависимости из файла requirements.txt:
```
pyhton install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```
Запустить сервер:

```
python manage.py runserver
```


### В проекте создан API. Доступ к нему есть только у ~~всех~~ аутентифицированных пользователей.
