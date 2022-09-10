import os

import psycopg2


class PostgresDatabase:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database=os.getenv('POSTGRES_DB')
        )
        self.cursor = self.connection.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def get_properties(self):
        assert self.connection, 'Database connection is not established'
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            'SELECT * FROM sreality.property'
        )
        return self.cursor.fetchall()
