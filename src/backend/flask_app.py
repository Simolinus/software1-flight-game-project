import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.distance import geodesic
from database import Database
import random
from db_functionality import *

db = Database()

app = Flask(__name__)
CORS(app)


@app.route("/airports", methods=["GET"])
def airports():
    cursor = db.get_connection().cursor(dictionary=True)
    sql = "SELECT iso_country, name, ident, latitude_deg, longitude_deg FROM airport"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return json.dumps(result)


@app.route("/currentAirport", methods=["GET"])
def currentAirport():
    connection = db.get_connection()
    result = player_location_airport_name(connection)
    return json.dumps(result)


@app.route("/airportLocations", methods=["GET"])
def airports_locations():
    connection = db.get_connection()
    result = airport_locations(connection)
    return json.dumps(result)


@app.route("/playerlocation", methods=["GET"])
def player_location():
    connection = db.get_connection()
    cursor = db.get_connection().cursor(dictionary=True)
    screen_name = check_for_players(connection)
    sql = "SELECT airport.latitude_deg, airport.longitude_deg FROM airport INNER JOIN player ON airport.ident = player.location WHERE player.screen_name = %s"
    cursor.execute(sql, (screen_name,))
    result = cursor.fetchone()
    cursor.close()
    return json.dumps(result)


@app.route("/player", methods=["GET"])
def player():
    connection = db.get_connection()
    cursor = db.get_connection().cursor(dictionary=True)
    screen_name = check_for_players(connection)
    sql = (
        "SELECT screen_name, money, score, location FROM player WHERE screen_name = %s"
    )
    cursor.execute(sql, (screen_name,))
    result = cursor.fetchone()
    cursor.close()
    print("player debug: ", result)
    return json.dumps(result)


@app.route("/player-update", methods=["POST"])
def update_player():
    try:
        data = request.json
        screen_name = data["screen_name"]
        money = data["money"]
        score = data["score"]

        connection = db.get_connection()
        cursor = connection.cursor()

        sql = """
            UPDATE player
            SET money = %s, score = %s
            WHERE screen_name = %s
        """
        cursor.execute(sql, (money, score, screen_name))
        connection.commit()

        return jsonify({"status": "success"})

    except Exception as e:
        print("update error:", e)
        return jsonify({"error": "server error"}), 500

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass


@app.route("/map-data", methods=["GET"])
def map_data():
    connection = db.get_connection()
    cursor = db.get_connection().cursor(dictionary=True)
    screen_name = check_for_players(connection)
    sql = "SELECT airport.latitude_deg, airport.longitude_deg, airport.ident FROM airport INNER JOIN player ON airport.ident = player.location WHERE player.screen_name = %s"
    cursor.execute(sql, (screen_name,))
    player_location = cursor.fetchone()

    sql2 = "SELECT ident, name, latitude_deg, longitude_deg FROM airport"
    cursor.execute(sql2)
    airports = cursor.fetchall()
    cursor.close()
    return json.dumps({"player": player_location, "airports": airports})


@app.route("/travel", methods=["POST"])
def travel():
    cursor = db.get_connection().cursor(dictionary=True)
    data = request.json
    destination = data["destination"]
    travel_type = data["type"]
    sql = "SELECT airport.latitude_deg, airport.longitude_deg, airport.ident, player.money FROM player JOIN airport ON airport.ident = player.location"
    cursor.execute(sql)
    player = cursor.fetchone()
    sql2 = "SELECT latitude_deg, longitude_deg FROM airport WHERE ident = %s"
    cursor.execute(sql2, (destination,))
    dest = cursor.fetchone()
    if not player or not dest:
        cursor.close()
        return json.dumps({"error": "Invalid player or destination"}), 400
    dist = geodesic(
        (player["latitude_deg"], player["longitude_deg"]),
        (dest["latitude_deg"], dest["longitude_deg"]),
    ).km
    if travel_type == "commercial":
        MAX_RANGE = 3500
        COST = 300
    elif travel_type == "private":
        MAX_RANGE = 1000000000
        COST = 800
    else:
        cursor.close()
        return json.dumps({"error": "Invalid travel type"}), 400
    if dist > MAX_RANGE:
        cursor.close()
        return json.dumps({"error": "Destination out of range"}), 400
    if player["money"] < COST:
        cursor.close()
        return json.dumps({"error": "Not enough money"}), 400
    sql3 = "UPDATE player SET location = %s, money = money - %s LIMIT 1"
    cursor.execute(sql3, (destination, COST))
    cursor.close()
    return json.dumps(
        {"status": "success", "new_location": destination, "distance": dist}
    )

@app.route("/acquire-puzzle-piece", methods=["GET"])
def aquire():
    connection = db.get_connection()
    puzzle_piece = acquire_puzzle_piece(connection)
    acquired = check_if_puzzle_piece_acquired(connection, puzzle_piece)
    if acquired == 0:
        return json.dumps({"piece": f"puzzle_piece NO.{puzzle_piece} found"})
    elif acquired == 1:
        return json.dumps({"piece": f"puzzle_piece NO.{puzzle_piece} already acquired"})
    else:
        return json.dumps({"error": "Something went wrong"}), 400

@app.route("/count-acquired-puzzles", methods=["GET"])
def count_acquired_puzzles():
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM puzzle_pieces WHERE acquired = 1")
    result = cursor.fetchone()[0]
    cursor.close()
    print("count-acquired-puzzles:", result)
    return jsonify({"count": result})

@app.route("/start-new-game", methods=["POST"])
def button_start_new_game():
    connection = db.get_connection()
    data = request.get_json()
    screen_name = data.get("screen_name")
    print("Received:", screen_name)
    start_new_game(connection)
    create_player(connection, screen_name)
    return jsonify({
        "message": "new game started",
        "screen_name": screen_name
    })


@app.route("/quiz", methods=["GET"])
def get_quiz():
    connection = db.get_connection()
    result = random_quiz(connection)
    return json.dumps(result)


@app.route("/clue", methods=["GET"])
def get_clue():
    connection = db.get_connection()
    result = get_puzzle_clues(connection)
    return json.dumps(result)


if __name__ == "__main__":
    app.run(use_reloader=True, host="127.0.0.1", port=3000)
