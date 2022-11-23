
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





