import mariadb
import geopy
from geopy.distance import geodesic
from db_functionality import *


def airports_in_player_range():
    connection = connect_to_database()
    player_location = get_player_location(connection)
    airports_location = airport_locations(connection)
    distances = [geodesic(player_location, airport).km for airport in airports_location]
    print(distances)


def main():
    connection = connect_to_database()
    existing_players = check_for_players(connection)
    if not existing_players:
        player_name = input("Enter player name: ")
        create_player(connection, player_name)
        print(f"Hello {player_name}")
    if existing_players:
        print(f"Hello {existing_players}")


if __name__ == "__main__":
    main()
