# Django v5 Boilerplate

## Package Management

### Install from requirements.txt

```shell
uv pip install -r requirements.txt
```

### Update requirements.txt

```shell
uv pip freeze | grep -v "install==1.3.5" | uv pip compile - -o requirements.txt
```

### Install new package

```shell
uv pip install <package-name>
```

## Migrate

```shell
python manage.py migrate
```

## gunicorn - WSGI(Web Server Gateway Interface)

### Run command

```shell
# Single worker
gunicorn project.wsgi:application

# Multiple workers
gunicorn --workers=$(python -c "import multiprocessing as mp; print(mp.cpu_count() * 2 + 1)") settings.wsgi:application
```

## daphne - ASGI(Asynchronous Server Gateway Interface)

### Run command

```shell
# Single worker
daphne -p 8001 project.asgi:application

# Multiple workers
daphne -u $(python -c "import multiprocessing as mp; print(mp.cpu_count())") -p 8001 project.asgi:application
```

## Run deploy script

```shell
python deploy/start_servers.py
```

