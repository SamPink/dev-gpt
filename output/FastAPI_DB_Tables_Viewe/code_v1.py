from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.url import URL
from databases import Database

from fastapi import FastAPI

# Update the following database settings to fit your database configuration
DATABASE_SETTINGS = {
    "drivername": "postgresql",
    "host": "localhost",
    "port": "5432",
    "username": "your_username",
    "password": "your_password",
    "database": "your_database",
}

app = FastAPI()
db = Database(URL(**DATABASE_SETTINGS))
engine = create_engine(URL(**DATABASE_SETTINGS))


async def fetch_tables():
    meta = MetaData()
    meta.reflect(bind=engine)

    tables = []
    for table_name, table_obj in meta.tables.items():
        table = {"name": table_name, "columns": [col.name for col in table_obj.columns]}
        tables.append(table)

    return tables


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/tables")
async def get_tables():
    return await fetch_tables()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)