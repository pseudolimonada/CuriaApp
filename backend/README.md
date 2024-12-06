# Backend

## API Specification

API Specifications can be found [here](https://github.com/pseudolimonada/pgi2024/blob/00d9417b9ef9ab8cd160d5ee9e3485f17fdc1a89/specifications.md)

## Create DB (example)

```shell
sudo -u postgres psql
```

```shell
DROP DATABASE IF EXISTS pgi2024;

CREATE DATABASE pgi2024;

CREATE USER admin WITH ENCRYPTED PASSWORD 'admin';

GRANT ALL PRIVILEGES ON DATABASE pgi2024 TO admin;

ALTER DATABASE pgi2024 OWNER TO admin;

GRANT ALL PRIVILEGES ON SCHEMA public TO admin;

GRANT USAGE ON SCHEMA public TO admin;

GRANT CREATE ON SCHEMA public TO admin;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;

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