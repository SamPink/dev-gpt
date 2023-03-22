import sqlite3

conn = sqlite3.connect("test_db.db")
c = conn.cursor()

c.execute('''CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
c.execute('''INSERT INTO people (name, age) VALUES ('Alice', 30)''')
c.execute('''INSERT INTO people (name, age) VALUES ('Bob', 28)''')

c.execute('''CREATE TABLE cars (id INTEGER PRIMARY KEY, make TEXT, model TEXT)''')
c.execute('''INSERT INTO cars (make, model) VALUES ('Toyota', 'Camry')''')
c.execute('''INSERT INTO cars (make, model) VALUES ('Honda', 'Civic')''')

conn.commit()
conn.close()
from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select

app = FastAPI()
engine = create_engine("sqlite:///test_db.db")

@app.get("/tables/{table_name}")
async def get_table(table_name: str):
    meta = MetaData()
    meta.reflect(bind=engine)
    table = meta.tables.get(table_name)

    if table:
        with engine.connect() as conn:
            response = conn.execute(select([table])).fetchall()
        
        data = [dict(zip(row.keys(), row)) for row in response]
        return {"data": data}
    
    return {"error": f"Table '{table_name}' not found"}

@app.get("/tables/list")
async def get_tables_list():
    meta = MetaData()
    meta.reflect(bind=engine)
    
    tables = [table for table in meta.tables]
    return {"tables": tables}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)