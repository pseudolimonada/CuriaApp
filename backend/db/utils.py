import hashlib

import psycopg2
from psycopg2 import pool
from typing import List, Dict

from backend.utils import (
    config,
    logger,
    get_dateobj_from_timestamp,
    get_dateobj_from_date,
)

# creates a pool of connections to the database (being opened/closed implicitly in all endpoints, setup in api.py)
db_pool = pool.SimpleConnectionPool(
    1,
    20,
    user=config["DB_USER"],
    password=config["DB_PASS"],
    host=config["DB_HOST"],
    port=config["DB_PORT"],
    database=config["DB_NAME"],
)


# wrapper to open/close cursor and commit/rollback transactions
def transactional(func):
    def wrapper(*args, **kwargs):
        db_con = args[0]
        with db_con.cursor() as cursor:
            try:
                db_con.autocommit = False
                result = func(*args, **kwargs, cursor=cursor)
            except Exception as e:
                db_con.rollback()
                logger.error(f"Error in transaction: {str(e)}")
                raise
            else:
                db_con.commit()
                return result
            finally:
                db_con.autocommit = True

    return wrapper


# util function to build an simple insert query with a list of fields
def _build_insert_query(table_name, field_list, fetch=None):
    columns = ", ".join(field_list)
    values = ", ".join(["%s"] * len(field_list))
    query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({values}) 
        """
    if fetch:
        query += f" RETURNING {fetch}"
    return query
