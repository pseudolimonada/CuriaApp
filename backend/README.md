# Backend

## API Specification

API Specifications can be found [here](https://github.com/pseudolimonada/pgi2024/blob/00d9417b9ef9ab8cd160d5ee9e3485f17fdc1a89/specifications.md)

## Create DB (example)

```shell
sudo -u postgres psql
```

```shell
postgres=# create database pgi2024;
postgres=# create user admin with encrypted password 'pgi2024';
postgres=# grant all privileges on database pgi2024 to admin;
```

## .env (example)

```
DB_USER = pgi2024
DB_PASS = 1234
DB_HOST = 127.0.0.1
DB_PORT = 5432
DB_NAME = pgi2024
APP_HOST = 127.0.0.1
APP_PORT = 8080
APP_SECRET_KEY = secret_key
```