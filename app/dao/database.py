import os
import asyncpg

init_sql = os.getenv("INIT_SQL", "db/init.sql")

class Database:
    @staticmethod
    async def reset_database():
        conn = await get_database()

        try:
            # Read SQL file contents
            with open(init_sql, 'r') as file:
                sql_commands = file.read()

            # Execute SQL commands
            await conn.execute(sql_commands)
        finally:
            await conn.close()

# Função para conectar ao banco de dados
async def get_database():
    try:
        DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/mykpi") 
        return await asyncpg.connect(DATABASE_URL)
    except Exception as e:
        raise e