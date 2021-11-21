"""Runs quiz"""

import questions
import keywords


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
    question_number = 1

    if first_play:
        print("\nGreat...let's begin!")
    else:
        print(f"Welcome back, {user_name}")

    while 0 < question_number < 16:
        if question_number < 6:
            difficulty = "easy"
            token: object = current_tokens[0]
        elif 6 <= question_number < 11:
            difficulty = "medium"
            token: object = current_tokens[1]
        else:
            difficulty = "hard"
            token: object = current_tokens[2]
        question = questions.Question(
            token, difficulty, question_number, available_keywords, user_name
        )
        question_number = question.check_answer(
            question.run_question()
        )

    if question_number == 16:
        print("Congrats all the way.....")
        # update scores
