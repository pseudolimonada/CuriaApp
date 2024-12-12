# Backend

python db_redeploy.py to generate all tables and populate products, admin user, farinha e afeto business.

in .env dont forget to add app_admin_password



## API Specification

API Specifications can be found [here](https://github.com/pseudolimonada/pgi2024/blob/00d9417b9ef9ab8cd160d5ee9e3485f17fdc1a89/specifications.md)

## Create DB (example)

```shell
sudo -u postgres psql
```

```shell
DROP DATABASE IF EXISTS pgi2024;

CREATE DATABASE pgi2024;

CREATE USER admin WITH ENCRYPTED PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE pgi2024 TO admin;

ALTER DATABASE pgi2024 OWNER TO admin;

GRANT ALL PRIVILEGES ON SCHEMA public TO admin;

GRANT USAGE ON SCHEMA public TO admin;

GRANT CREATE ON SCHEMA public TO admin;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;

```

> [!NOTE]
> if your admin user already exists with a different password, in the .env example put the db_user/pass with the correct name/password



## .env (example)

```
DB_USER = admin
DB_PASS = admin
DB_HOST = localhost
DB_USER = admin
DB_PASS = admin
DB_HOST = localhost
DB_PORT = 5432
DB_NAME = pgi2024
```