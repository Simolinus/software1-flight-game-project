import mariadb
from db_functionality import *


def initialize_game():
    connection = connect_to_database()
    existing_players = check_for_players(connection)
    if not existing_players:
        start_new_game(connection)
        player_name = input("Enter player name: ")
        create_player(connection, player_name)
        print(f"Hello {player_name}")
    if existing_players:
        print(f"Hello {existing_players}")


def main():
    connection = connect_to_database()


if __name__ == "__main__":
    initialize_game()
    main()
