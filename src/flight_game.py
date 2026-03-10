import mariadb
import sys
import time
from db_functionality import *
from datetime import datetime

file = open("game_story.txt", "r")
game_story = file.read()
start_time = None
end_time = None


def initialize_game():
    global start_time, end_time
    connection = connect_to_database()
    existing_players = check_for_players(connection)
    if not existing_players:
        start_new_game(connection)
        game_story_objectives(game_story)
        print("\n")
        player_name = input("Enter player name: ")
        create_player(connection, player_name)
        print(f"\nHello {player_name}\n")
    if existing_players:
        print(f"\nHello {existing_players}\n")
    start_time = datetime.now()
    return


def game_story_objectives(game_story, delay=0.03):
    for char in game_story:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def user_input(key, connection):
    if key == "0":
        connection = connect_to_database()
        start_new_game(connection)
        initialize_game()
        return
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
                        print(
                            f"Arrived at {player_location_airport_arrived(connection)}"
                        )
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
                        print(
                            f"Arrived at {player_location_airport_arrived(connection)}"
                        )
                        return
                    else:
                        print("NOT ENOUGH BALANCE (€)\n")
                        break
        print("\n")
        return
    elif key == "2":
        while True:
            print("b: Go back\n")
            quiz = random_quiz(connection)
            if not quiz:
                print("All quizzes answered!")
                break
            correct_answer = quiz[0][2]
            print(f"Quiz: {quiz[0][1]}")
            quiz_id = quiz[0][0]
            answer_input = input("Answer quiz: ")
            if answer_input == "b":
                break
            if answer_input == correct_answer:
                print("Correct answer! Money: +100€, Score: +1")
                print("\n")
                sql = "UPDATE quizzes SET answered = ? WHERE answer = ? AND id = ?"
                cursor = connection.cursor()
                cursor.execute(sql, (1, correct_answer, quiz_id))
                sql = "UPDATE player SET money = money + 100, score = score + 1"
                cursor.execute(sql)
                cursor.close()
            else:
                print("Wrong answer!")
        return
    elif key == "3":
        print("Clue is ?")
        return


def should_game_end(connection):
    current_score = get_player_score(connection)
    if are_all_puzzles_found(connection) == True:
        end_time = datetime.now()
        time_difference = (end_time - start_time).total_seconds()
        if time_difference > 0 and time_difference <= 60:  # 1 minutes
            current_score += 100
        elif time_difference > 60 and time_difference <= 300:  # 5 minutes
            current_score += 80
        elif time_difference > 300 and time_difference <= 600:  # 10 minutes
            current_score += 60
        elif time_difference > 600 and time_difference <= 1200:  # 20 minutes
            current_score += 40
        elif time_difference > 1200 and time_difference <= 1800:  # 30 minutes
            current_score += 10
        cursor = connection.cursor()
        sql = f"UPDATE player SET score = {current_score}"
        cursor.execute(sql)
        cursor.close
        print("\nCongratulations! You found all 10 puzzle pieces.")
        print("\nFinal score: " + str(current_score))
        print("Thank you for playing!")
        print("\nAvailable options:\n0: Start new game\n4: Exit\n")
        user_input_key = input("Enter command: ")
        if user_input_key == "0" or user_input_key == "4":
            user_input(user_input_key, connection)
        else:
            print("Invalid command!")


def main():
    connection = connect_to_database()
    while True:
        player = check_for_players(connection)
        puzzle_piece_at_player = check_for_puzzle_piece(connection)
        if puzzle_piece_at_player and puzzle_piece_at_player[0] != 1:
            print(
                f"Puzzle piece No.{puzzle_piece_at_player[0]} found at {player_location_airport_arrived(connection)}\n"
            )
        acquire_puzzle_piece(connection)
        should_game_end(connection)
        print(f"\n{player}")
        print("--------------")
        print(
            "\nAvailable options:\n0: Start new game\n1: Travel\n2: Answer quiz\n3: Inspect clue\n4: Exit\n"
        )
        print(f"Puzzle pieces found {puzzle_pieces_found(connection)} out of 10")
        current_money(connection)
        player_location_airport_name(connection)
        user_input_key = input("Enter command: ")
        print("\n")
        user_input(user_input_key, connection)


if __name__ == "__main__":
    initialize_game()
    main()
