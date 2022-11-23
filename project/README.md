# laba_4_pp

## Створення та налаштування проекту за допомогою poetry

poetry version 1.2.1

python version 3.8.3

flask version 2.2.2

## Завантаження 

Після встановлення poetry і pyenv у нас є можливість запустити проект наступним чином:
```commandline
poetry new project 
cd project
poetry init
```

Створивши пустий проект, далі додаємо залежності, якими будемо користуватись:
```commandline
poetry add flask
poetry add waitress
```
Щоб наше середовище стало активним, то потрібно ввести наступну команду:

```poetry shell```

## Запуск сервера

Щоб подивитись результат нашої програми, нам потрібно заупустити сервер WSGI:

```waitress-serve --host 127.0.0.1 server:laba_4_sol```

За допомогою декоратора ```@app.route("/api/v1/hello-world-15")``` реалізуємо адресу.
Перейшовши на неї, бачимо текст "hello world 15"

http://localhost:5000/api/v1/hello-world-15

## Створення бази даних
Використайте наступне:

```
Install mysqlclient
Install alembic

alembic init  your_name

your_name.ini
fill sqlalchemy.url
sqlalchemy.url = mysql://root:root@localhost:5900/mydb

After writing models, copy this to cmd
alembic revision --autogenerate -m "First migration"

Then alembic upgrade ... (the first three letters or numbers of migration)
```
Щоб запустити дану програму (branch = api_pharmacy), введіть наступне в консолі


``` 
set FLASK_APP=application.py
python application.py
```





