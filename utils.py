import asyncpg
from asyncpg.pool import Pool
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def pool_conn():
    host = os.environ.get("POSTGRESQL_HOST")
    port = os.environ.get("POSTGRESQL_PORT")
    database = os.environ.get("POSTGRESQL_DB")
    user = os.environ.get("POSTGRESQL_USERNAME")
    password = os.environ.get("POSTGRESQL_PASSWORD")
    DATABASE_URL = f"postgres://{user}:{password}@{host}:{port}/{database}"
    return DATABASE_URL

async def get_pool() -> Pool:
    pool = await asyncpg.create_pool(pool_conn(), min_size=1, max_size=4)
    return pool

async def post_data_to_table(query_str: str) -> str:
    async with (await get_pool()).acquire() as connection:
        try:
            await connection.execute(query_str)
            return 'OK'

        except Exception as ex:
            logging.error(str(ex))
            error_traceback = traceback.format_exc()
            ex_error = f"{str(ex)}\n{error_traceback}"
            return f'POST ERROR: {ex_error}\n{query_str}'

async def update_data_1():
    query = """
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE full_names.name || '.' || split_part(short_names.name, '.', 2) = short_names.name;
"""
    status = await post_data_to_table(query)
    return status

async def update_data_2():
    query = """
UPDATE full_names
SET status = short_names.status
WHERE EXISTS (
    SELECT 1
    FROM short_names
    WHERE full_names.name || '.' || split_part(short_names.name, '.', 2) = short_names.name
);
"""
    status = await post_data_to_table(query)
    return status



async def update_data_3():
    query = """UPDATE full_names
SET status = (
    SELECT short_names.status
    FROM short_names
    WHERE full_names.name || '.' || split_part(short_names.name, '.', 2) = short_names.name
)
WHERE EXISTS (
    SELECT 1
    FROM short_names
    WHERE full_names.name || '.' || split_part(short_names.name, '.', 2) = short_names.name
);
"""
    status = await post_data_to_table(query)
    return status