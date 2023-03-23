# mfss

МФСБ




## Переменные
- POSTGRES_HOST - хост базы данных
- POSTGRES_DB - имя базы данных
- POSTGRES_USER - пользователь базы данных
- POSTGRES_PASSWORD - пароль пользователя базы данных
- POSTGRES_PORT - порт базы данных 
## Использование

Загрузка первоначальных данных в базу производится через fixtures

```bash
python manage.py loaddata <имя файла>
Пример :

python manage.py loaddata settings.json

```

После проведения миграций создать суперпользователя из стандартной команды джанго:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

```




# github
…or create a new repository on the command line

```bash
echo "# mfss" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Sabron/mfss.git
git push -u origin main                       
```
…or push an existing repository from the command line

```bash
git remote add origin https://github.com/Sabron/mfss.git
git branch -M main
git push -u origin main
```

tar -cvf userpic.tar.gz /home/hronos/hronos_school//att/USERPIC  - Архивирование
tar -cvf userpic.tar.gz /home/hronos/hronos_school/static/att/USERPIC  - Архивирование


git config --global credential.helper store

```bash
Это делается командой git remote add, но делать её можно только на существующем репозитории, так что вам понадобится ещё и git init. 
Потом вам понадобится получить из репозитория коммиты командой git fetch и сделать git reset чтобы вносить свои изменения не с нуля, 
а начиная с головы репозитория.

git init
git remote add origin https://github.com/Sabron/mfss.git
git fetch origin
git reset --mixed origin/main
git add .
git commit -m "комментарий к коммиту"
git push -u origin main

URL репозитория можно получить нажав на ту самую кнопку Clone в интерфейсе github.
```