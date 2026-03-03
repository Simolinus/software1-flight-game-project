import mariadb
import random
import geopy
from geopy import distance
from geopy.distance import geodesic


def connect_to_database():
    connection = mariadb.connect(
        host="127.0.0.1",
        port=3306,
        user="user",
        password="password",
        database="skyquest",
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
    sql = "SELECT latitude_deg, longitude_deg FROM airport INNER JOIN player ON airport.ident = player.location WHERE screen_name = screen_name"
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
    sql = "INSERT INTO player (money, screen_name, location) VALUES (?, ?, ?)"
    cursor = connection.cursor()
    cursor.execute(sql, (1000, player_name, "EFHK"))
    cursor.close()


def start_new_game(connection):
    cursor = connection.cursor()
    sql = "DELETE FROM player"
    cursor.execute(
        sql,
    )
    sql = "UPDATE puzzle_pieces SET acquired = DEFAULT"
    cursor.execute(
        sql,
    )
    sql = "UPDATE quizzes SET answered = DEFAULT"
    cursor.execute(
        sql,
    )
    sql = "UPDATE airport SET puzzle_piece = DEFAULT"
    cursor.execute(
        sql,
    )
    sql = "UPDATE quizzes SET answered = DEFAULT"
    cursor.close()
    randomize_puzzle_piece_location(connection)


def check_for_players(connection):
    sql = "SELECT screen_name from player"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return None
    return result[0]


def airports_id(connection):
    sql = "SELECT id FROM airport WHERE NOT id = '2307'"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    airports = cursor.fetchall()
    cursor.close()
    return airports


def puzzle_pieces_id(connection):
    sql = "SELECT id FROM puzzle_pieces"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    puzzle_pieces = cursor.fetchall()
    cursor.close()
    return puzzle_pieces


def randomize_puzzle_piece_location(connection):
    cursor = connection.cursor()
    airports = airports_id(connection)
    random_airports = random.sample(airports, 10)
    puzzle_pieces = puzzle_pieces_id(connection)
    random.shuffle(puzzle_pieces)
    for i in range(10):
        puzzle_piece_id = puzzle_pieces[i][0]
        airport_id = random_airports[i][0]
        sql = "UPDATE airport SET puzzle_piece = ? WHERE id = ?"
        cursor.execute(sql, (puzzle_piece_id, airport_id))
    cursor.close()


def airports_in_player_range():
    connection = connect_to_database()
    player_location = get_player_location(connection)
    airports_location = airport_locations(connection)
    distances = [geodesic(player_location, airport).km for airport in airports_location]
    print(distances)


def check_for_puzzle_piece(connection):
    sql = "SELECT puzzle_piece FROM airport, player WHERE airport.ident = player.location AND puzzle_piece IS NOT null"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return None
    return result[0]


def acquire_puzzle_piece(connection):
    cursor = connection.cursor()
    puzzle_piece_at_player = check_for_puzzle_piece(connection)
    if puzzle_piece_at_player:
        sql = "UPDATE puzzle_pieces SET acquired = ? WHERE id = ?"
        cursor.execute(sql, (1, puzzle_piece_at_player))
    cursor.close


def player_location_airport_name(connection):
    sql = "SELECT ident, country.name, airport.name FROM airport, player, country WHERE airport.ident = player.location AND airport.iso_country = country.iso_country"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    location = cursor.fetchone()
    print(f"Current location: {location[0]}, {location[1]}, {location[2]}")


def current_money(connection):
    sql = "SELECT money FROM player"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    money = cursor.fetchone()
    print(f"Current money: {money[0]}€")


def which_quiz(connection):
    sql = "SELECT id, quiz, answer FROM quizzes WHERE NOT answered = '1'"
    cursor = connection.cursor()
    cursor.execute(
        sql,
    )
    quizzes = cursor.fetchall()
    cursor.close()
    return quizzes


def random_quiz(connection):
    cursor = connection.cursor
    quizzes = which_quiz(connection)
    one_random_quiz = random.sample(quizzes, 1)
    print(one_random_quiz[0][1])
    return one_random_quiz[0][2]
