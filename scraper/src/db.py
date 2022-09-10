import os

import psycopg2


class PostgresDatabase:
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        self.connection = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database=os.getenv('POSTGRES_DB')
        )

    def close(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def commit(self) -> None:
        assert self.connection, 'Database connection is not established'
        self.connection.commit()

    def execute(self, command, values=None) -> None:
        assert self.connection, 'Database connection is not established'
        self.cursor = self.connection.cursor()
        self.cursor.execute(command, values)

    def number_of_properties(self) -> int:
        assert self.connection, 'Database connection is not established'
        self.cursor = self.connection.cursor()
        self.cursor.execute('SELECT * FROM sreality.property')
        return self.cursor.rowcount
