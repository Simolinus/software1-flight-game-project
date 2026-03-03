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
        print("Available airports:")
        input("Choose airport: ")
        return
    elif key == "2":
        while True:
            print("\n")
            print("Answer quiz or quit to exit\n")
            quiz = random_quiz(connection)
            correct_answer = quiz[0][2]
            print(quiz[0][1])
            quiz_id = quiz[0][0]
            answer_input = input("Input: ")
            if answer_input == "quit":
                break
            if answer_input == correct_answer:
                print("Correct answer!")
                sql = "UPDATE quizzes SET answered = ? WHERE answer = ? AND id = ?"
                cursor = connection.cursor()
                cursor.execute(sql, (1, correct_answer, quiz_id))
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
        user_input(user_input_key, connection)


if __name__ == "__main__":
    initialize_game()
    main()
