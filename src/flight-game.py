import mariadb
import geopy


def connect_to_database():
    connection = mariadb.connect(
        host="127.0.0.1",
        port=3306,
        user="user",
        password="password",
        database="flight_game",
        autocommit=True,
    )
    return connection


def main():
    print("Hello world!")


if __name__ == "__main__":
    main()
