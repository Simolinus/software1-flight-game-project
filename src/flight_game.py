import mariadb
import sys
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


def user_input(key, connection):
    if key == "0":
        start_new_game(connection)
        initialize_game()
    elif key == "4":
        print("Exiting")
        sys.exit(0)
    elif key == "1":
        range = 5000
        print("Available airports:")
        print("\n")
        airports_distance = player_distance_to_airports()
        for i in airports_distance:
            if range > int(i[3]):
                print(f"{i[0]}, {i[1]}, {i[2]}")
        print("\n")
        destination = input("Choose destination by ICAO: ").strip().upper()
        print("\n")
        sql = f"UPDATE player SET location = '{destination}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        print(f"Arrived at {destination}")
        return
    elif key == "2":
        while True:
            print("Answer quiz or quit to exit\n")
            quiz = random_quiz(connection)
            if not quiz:
                print("All quizzes answered!")
                break
            correct_answer = quiz[0][2]
            print(quiz[0][1])
            quiz_id = quiz[0][0]
            answer_input = input("Input: ")
            if answer_input == "quit":
                break
            if answer_input == correct_answer:
                print("Correct answer! +100€")
                print("\n")
                sql = "UPDATE quizzes SET answered = ? WHERE answer = ? AND id = ?"
                cursor = connection.cursor()
                cursor.execute(sql, (1, correct_answer, quiz_id))
                sql = "UPDATE player SET money = money + 100"
                cursor.execute(sql)
                cursor.close()
            else:
                print("Wrong answer!")
        return
    elif key == "3":
        print("Clue is ?")
        return


def main():
    connection = connect_to_database()
    while True:
        print(
            "\n0: Start new game\n1: Travel\n2: Answer quiz\n3: Inspect clue\n4: Exit\n"
        )
        current_money(connection)
        player_location_airport_name(connection)
        user_input_key = input("Enter command: ")
        print("\n")
        user_input(user_input_key, connection)


if __name__ == "__main__":
    initialize_game()
    main()
