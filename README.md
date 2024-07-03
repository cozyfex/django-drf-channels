# Django v5 Boilerplate

## Package Management

### Install from requirements.txt

```shell
uv pip install -r requirements.txt
```

### Update requirements.txt

```shell
uv pip freeze | uv pip compile - -o requirements.txt
```

### Install new package

```shell
uv pip install <package-name>
```

## gunicorn - WSGI(Web Server Gateway Interface)

### Run command

```shell
# Single worker
gunicorn settings.wsgi:application

# Multiple workers
gunicorn --workers=$(python -c "import multiprocessing as mp; print(mp.cpu_count() * 2 + 1)") settings.wsgi:application
```


