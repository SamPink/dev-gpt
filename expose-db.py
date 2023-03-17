from typing import Any, Callable, Dict, List, Optional, Union

from fastapi import FastAPI
from sqlalchemy import MetaData, Table, create_engine, select, inspect, Column, Integer, String
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import Session, sessionmaker

import config

app = FastAPI()


class DataAccessLayer:
    def __init__(self, settings: Dict[str, Any]) -> None:
        self.settings: Dict[str, Any] = settings
        self.schema: str = self.settings["database"]["schema"]
        self.connect_string: str = URL.create(
            "mssql+pyodbc",
            query={"odbc_connect": self.settings["database"]["SQLConnectString"]},
        )

        # create the engine
        self.engine: Engine = create_engine(self.connect_string)

        # create the metadata
        self.metadata: MetaData = MetaData(schema=self.schema)
        self.metadata.reflect(bind=self.engine)

        # create the sessionmaker
        self.sessionmaker: Callable[[], Session] = sessionmaker(bind=self.engine)

        # create the endpoints for each table and view
        for table in self.metadata.sorted_tables:
            self.create_endpoint(table.name)

        inspector = inspect(self.engine)
        for view_name in inspector.get_view_names(schema=self.schema):
            self.create_endpoint(view_name)

    def create_endpoint(self, name: str) -> None:
        obj = self.metadata.tables.get(name)
        if obj is None:
            obj = Table(name, self.metadata, autoload=True, autoload_with=self.engine)

        @app.get(f"/{name}")
        async def read_table(
            q: Optional[str] = None,
            limit: Optional[int] = None,
            **kwargs,
        ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:

            if q is not None:
                query = select([obj]).where(
                    [Column(col_name, String) == col_val for col_name, col_val in kwargs.items()]
                )
            else:
                query = select([obj])

            if limit is not None:
                query = query.limit(limit)

            rows = self.engine.execute(query)

            return [dict(row) for row in rows]

        read_table.__doc__ = f"Get all rows from the {name} table or view."
        for column in obj.columns:
            read_table.__doc__ += f"\n- {column.name}: {column.type}"

if __name__ == "__main__":
    dal = DataAccessLayer(config.settings)
    uvicorn.run(app)
