"""Runs quiz"""

from time import sleep

from matrix import matrix_line
import questions
import keywords
from sheets import update_win, update_scores
from prints import magenta_print, cyan_print

STAR_LINE = keywords.STAR_LINE
STAR_EMPTY = keywords.STAR_EMPTY
STAR_SOLID = keywords.STAR_SOLID


def quiz(user_name: str, current_tokens: tuple, first_play: bool = True):
    """Runs the quiz

    Quiz continues up to 15 questions or until a user decides to 'take' or
    inputs a wrong answer

    ---
    Args:
        user_name (str): The user name to play through the quiz
        current_tokens (tuple): Easy, medium and hard `Token` objects
        first_play (bool): (default = True) If False, the intro to the quiz
            will recognise a returning user
    """
    available_keywords = keywords.Keywords()
    quiz_end = False
    question_number = 1

    if first_play:
        print("\nGreat...let's begin!")
    else:
        print(f"\nWelcome back, {user_name}")

    while 0 < question_number < 16 and not quiz_end:
        if question_number < 6:
            difficulty = "easy"
            token = current_tokens[0]
        elif 6 <= question_number < 11:
            if question_number == 6:
                magenta_print(
                    "\nWell done on getting this far, you can't score lower "
                    "than 5 now!"
                )
                sleep(.5)
            difficulty = "medium"
            token = current_tokens[1]
        else:
            if question_number == 11:
                magenta_print(
                    "\nWow, fantastic! You are far enough that you can't "
                    "score lower than 10 now!"
                )
                sleep(.5)
            difficulty = "hard"
            token = current_tokens[2]
        question = questions.Question(
            token, difficulty, question_number, available_keywords, user_name
        )
        return_from_question = question.check_answer(
            question.run_question()
        )
        question_number = return_from_question[0]
        quiz_end = return_from_question[1]

    if question_number == 16:
        cyan_print(STAR_LINE)
        cyan_print(
            f"{STAR_SOLID}"
            "That's it! You did it! Congratulations!!"
            f"{STAR_EMPTY}".rjust(36)
            )
        print(
            f"\033[36;1m{STAR_EMPTY}",
            "You answered all 15 question correctly!!".center(76).rstrip(),
            f"{STAR_SOLID}\033[0m".rjust(18)
        )
        cyan_print(
            f"{STAR_SOLID}"
            f"You clearly know your stuff. Well done!!{STAR_EMPTY}".rjust(77)
        )
        cyan_print(STAR_LINE)
        update_win(user_name)

    if quiz_end:
        update_scores(user_name, question_number)
        cyan_print("Good luck for next time!\n")
        matrix_line()
