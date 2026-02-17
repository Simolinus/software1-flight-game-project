import mariadb
import geopy
from db_functionality import *


def main():
    connection = connect_to_database()
    player_name = input("Enter player name: ")
    create_player(connection, player_name)
    print(f"Hello {player_name}")


if __name__ == "__main__":
    main()
