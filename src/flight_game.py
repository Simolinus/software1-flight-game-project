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
        print(f"\nHello {player_name}\n")
    if existing_players:
        print(f"\nHello {existing_players}\n")


def user_input(key, connection):
    if key == "0":
        start_new_game(connection)
        initialize_game()
    elif key == "4":
        print("Exiting")
        sys.exit(0)
    elif key == "1":
        commercial_range = 3500
        private_range = 500000
        current_balance = get_player_money(connection)
        while True:
            print("Available options:")
            print("1: Commercial flight[300€]\n2: Private flight[500€]\n3: Go back")
            user_input_flight = input("Enter command: ")
            print("\n")
            if user_input_flight == "3":
                break
            if user_input_flight == "1":
                while True:
                    print("Available airports:")
                    airports_distance = player_distance_to_airports()
                    for i in airports_distance:
                        if commercial_range > int(i[3]):
                            print(f"{i[0]}, {i[1]}, {i[2]}")
                    print("\n3: Go back\n")
                    if current_balance >= 300:
                        destination = (
                            input("Choose destination by ICAO: ").strip().upper()
                        )
                        print("\n")
                        if destination == "3":
                            break
                        print("\n")
                        sql = f"UPDATE player SET location = '{destination}'"
                        cursor = connection.cursor()
                        cursor.execute(sql)
                        sql2 = f"UPDATE player SET money = {current_balance}-300"
                        cursor.execute(sql2)
                        cursor.close
                        print(f"Arrived at {destination}")
                        return
                    else:
                        print("NOT ENOUGH BALANCE (€)\n")
                        break
            if user_input_flight == "2":
                while True:
                    print("Available airports:")
                    airports_distance = player_distance_to_airports()
                    for i in airports_distance:
                        if private_range > int(i[3]):
                            print(f"{i[0]}, {i[1]}, {i[2]}")
                    print("\n3: Go back\n")
                    if current_balance >= 500:
                        destination = (
                            input("Choose destination by ICAO: ").strip().upper()
                        )
                        print("\n")
                        if destination == "3":
                            break
                        print("\n")
                        sql = f"UPDATE player SET location = '{destination}'"
                        cursor = connection.cursor()
                        cursor.execute(sql)
                        sql3 = f"UPDATE player SET money = {current_balance}-500"
                        cursor.execute(sql3)
                        cursor.close
                        print(f"Arrived at {destination}")
                        return
                    else:
                        print("NOT ENOUGH BALANCE (€)\n")
                        break
        print("\n")
        return
    elif key == "2":
        while True:
            print("3: Go back\n")
            quiz = random_quiz(connection)
            if not quiz:
                print("All quizzes answered!")
                break
            correct_answer = quiz[0][2]
            print(f"Quiz: {quiz[0][1]}")
            quiz_id = quiz[0][0]
            answer_input = input("Answer quiz: ")
            if answer_input == "3":
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
        player = check_for_players(connection)
        print(player)
        print("////////////////////")
        print(
            "\nAvailable options:\n0: Start new game\n1: Travel\n2: Answer quiz\n3: Inspect clue\n4: Exit\n"
        )
        current_money(connection)
        player_location_airport_name(connection)
        user_input_key = input("Enter command: ")
        print("\n")
        user_input(user_input_key, connection)


if __name__ == "__main__":
    initialize_game()
    main()
