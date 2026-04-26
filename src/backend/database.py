import os
import mariadb


class Database:
    def __init__(self):
        self.connection = mariadb.connect(
            host="127.0.0.1",
            port=3306,
            user="user",
            password="password",
            database="skyquest",
            autocommit=True,
        )

    def get_connection(self):
        return self.connection
