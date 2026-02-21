import mariadb
import geopy
from geopy import distance


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


def get_distance_between_airports(connection, icao, icao2):
    sql = "SELECT latitude_deg, longitude_deg FROM airport WHERE ident = ? OR ident = ?"
    cursor = connection.cursor()
    cursor.execute(sql, (icao, icao2))
    result = cursor.fetchall()
    airport1 = result[0]
    airport2 = result[1]
    distance_between_airports = distance.distance(airport1, airport2).km
    cursor.close()
    return distance_between_airports


def airport_locations(connection):
    sql = "SELECT latitude_deg, longitude_deg FROM airport"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    result = cursor.fetchall()
    cursor.close()
    return result


def get_player_location(connection):
    sql = "SELECT latitude_deg, longitude_deg FROM airport INNER JOIN game ON airport.ident = game.location WHERE screen_name = screen_name"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    result = cursor.fetchall()
    cursor.close()
    return result


def get_airports(connection):
    sql = "SELECT airport.ident, airport.name, country.name FROM airport, country"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    result = cursor.fetchall()
    cursor.close()
    return result


def create_player(connection, player_name):
    sql = "INSERT INTO game (screen_name, location) VALUES (?, ?)"
    cursor = connection.cursor()
    cursor.execute(sql, (player_name, "EFHK"))
    cursor.close()


def start_new_game(connection):
    sql = "DELETE FROM game"
    sql = "DELETE FROM goal_reached"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    sql = "DELETE FROM goal_reached"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    cursor.close()


def check_for_players(connection):
    sql = "SELECT screen_name from game"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    result = cursor.fetchone()
    cursor.close()
    return result[0]
