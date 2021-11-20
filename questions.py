"""Handle questions"""

from html import unescape
from random import randrange, shuffle
import requests
from getch import pause

import tokens
import keywords
from matrix import matrix_line
from max_line_length import limit_line_length as shorten

CORRECT_RESPONSES = (
    "Correct...", "Well done!", "That's right.",
    "You clearly know your stuff.", "That was...error-free!", "Spot on.",
    "Brilliant, that's correct.", "Nice work."
)
INCORRECT_RESPONSES = (
    "Oh dear, that's wrong I'm afraid.", "Oh no! That wasn't correct.",
    "Unfortunately, that answer was incorrect.", "Game over for you.",
    "That does not compute...wrong answer!"
)
READY_WORDS = [
    "Ready?", "OK...", "Next...", "Here we go!", "Try this...",
    "See how you get on with this one.", "Let's see how you get on.",
    "Are you ready for this?"
]
unused_correct_responses = list(CORRECT_RESPONSES)
unused_ready_words = list(READY_WORDS)


class Question():
    """Quiz question with all functions to run

    ---
    Attributes:
        token (object = Token): Current difficulty Token
        difficulty (str): Current difficulty
        question_number (int): Current question number
        key_words (object = Keywords): Keywords containing currently available
        user_name (str): Current user name
    """

    def __init__(
        self, token: tokens.Token, difficulty: str,
        question_number: int, key_words: keywords.Keywords,
        user_name: str
    ) -> None:
        self.token = token
        self.difficulty = difficulty
        self.question_number = question_number
        self.keywords = key_words
        self.user_name = user_name
        self.question_data = self._check_and_retrieve()[1]["results"][0]
        self.choices, self.correct_answer = self._set_answer_letters()

    def _reset_ready_words(self):
        """Repopulates ready words with original list"""

        global unused_ready_words
        unused_ready_words = list(READY_WORDS)

    def _check_and_retrieve(self) -> tuple:
        """Retrieve a response from opentdb API

        Connects to opentdb.com/api to ensure correct query
        parameters have been used in the URL, allowing for valid
        data

        Args:
            difficulty: The current difficulty level set by the
            question number

        Returns:
            tuple: (bool, dict[str, str])
                bool: True if response from API is 0, else false
                dict[str, list]: The question in JSON format
                    example: "results":[{"category":"Science:
                    Computers","type":"multiple",
                    difficulty":"easy","question":"What is the
                    domain name for the country Tuvalu?",
                    correct_answer":".tv","incorrect_answers":[".
                    tu",".tt",".tl"]}]
        """

        api_url = (
            "https://opentdb.com/api.php?amount=1&category"
            f"=18&difficulty={self.difficulty}&type=multiple"
            f"&token={self.token.string}"
        )

        print("\nRetrieving data...")
        response = requests.get(api_url)
        data = response.json()

        if data["response_code"] in (3, 4):
            print("Token expired:")
            self.token.string = self.token.initiate_new_token_string()
            data = self._check_and_retrieve()[1]
            return True, data

        try:
            if data["response_code"] in (1, 2):
                raise ConnectionError(
                    f"Open Trivia Database API connection error: {api_url}\n"
                    f"Response_code from API: {data['response_code']}"
                )
        except ConnectionError as e:
            print(f"Error: {e}")
            print("Program will now terminate!")
            exit()

        print("Data retrieval successful...")
        return True, data

    def _set_answer_letters(self):
        """Give each answer a letter and determines the correct answer.

        Args:
            question: The current question.


        Returns:
            tuple: (dict, str)
                dict[str, str]: Shuffled answers paired with a choice letter.
                str: The correct answer.
        """
        correct_answer = unescape(self.question_data["correct_answer"])
        incorrect_answers = list(self.question_data["incorrect_answers"])
        answers = [correct_answer, *incorrect_answers]
        shuffle(answers)

        abcd = {
            "a": unescape(answers[0]),
            "b": unescape(answers[1]),
            "c": unescape(answers[2]),
            "d": unescape(answers[3]),
        }

        return abcd, correct_answer

    def _display_question(
        self, current_pre_question: str, first_attempt: bool = False
    ):
        """Prints question and possible answers

        Prints a single matrix_line for visual clarity

        Prints a pre_question string, the question and the possible answers. If
        it is the first time the question has been printed, a random string
        will be prepended to the Question Number x

        Questions longer than 80 characters are split over individual lines and
        spaces are trimmed to prevent single space indent on new line

        Args:
            question: The current question.
            abcd: A dict of the available answers with a selection letter.
            pre_question: A string to be prepended to the question number.
            first_attempt: Determines if the prepending string needs defining
                (default: False)

        Returns:
            str: Generated prepend to question number. Default returned if not
                first_attempt (default: "")
        """

        global unused_ready_words

        matrix_line()
        pre_question_str = ""
        if first_attempt:
            if not unused_ready_words:
                self._reset_ready_words()
            pre_question_str = unused_ready_words[
                randrange(len(unused_ready_words))]
            unused_ready_words.remove(pre_question_str)
        if pre_question_str:
            print(
                f"\n{pre_question_str} Question Number "
                f"{str(self.question_number)}"
            )
        else:
            print(
                f"\n{current_pre_question} Question Number"
                f"{str(self.question_number)}"
            )
        print(f"Followed by the {len(self.choices)} possible answers...\n")

        question_str = unescape(self.question_data["question"])

        shorten(question_str)

        print("")

        for letter, answer_str in self.choices.items():
            print(f"{letter}: {answer_str}")

        print(f"The answer is: {self.correct_answer}")
        return pre_question_str

    def run_question(self):
        """Runs the question

        Sets difficulty level depending on question number. Prints question and
        answers and available lifelines. Awaits user input that gets validated

        Args:
            question_num: The current question number

        Returns:
            str: A validated user input
            dict[str, str]: The answers with a key letter for user selection
            str: The question answer
        """

        pre_question = self._display_question(None, True)

        while True:
            print(f"\nAvailable keywords:{self.keywords.available_keywords}")
            print(f"Available choices:{list(self.choices.keys())}")
            user_input = input(
                "Please provide your answer or enter a keyword:\n"
            ).lower()
            input_check = self._check_input(user_input)
            if not input_check:
                self._display_question(
                    pre_question
                )
            else:
                break

        return user_input

    def _check_input(self, new_input: str):
        """Validates user's input after question is printed

        Checks for valid user input and checks if keyword has been used

        Args:
            new_input: The user's input string
            choices: A dictionary of letters and their associated answer.
            answer: The current question answer as a string

        Returns:
            bool: True if answer is received, else False and continue user
                input
            dict[str, str]: Available answer choices
        """

        choices = self.choices

        try:
            if not new_input:
                raise ValueError("No input detected...")
            # change to available keywords
            if new_input in self.keywords.available_keywords:
                choices = self.keywords.used(
                    new_input, choices, self.correct_answer,
                    self.user_name, self.question_number
                )
                self.choices = choices
                return False
            if new_input not in choices:
                raise ValueError(
                    "Invalid input detected, please input an answer or "
                    "available keyword."
                )

        except ValueError as e:
            print(f"{e}\n")
            pause()
            self.choices = choices
            return False

        self.choices = choices
        return True

    def check_answer(
        self, user_input: str, question_number: int
    ):
        """Check user's answer against correct answer

        If the user answer is correct, increment the question number and allow
        the quiz to continue. Otherwise run through loss functions.

        Args:
            user_input: The user's chosen letter.
            choices: Letters with their assigned answer.
            answer: The answer string to the question.
        """

        global unused_correct_responses

        if self.choices[user_input] == self.correct_answer:
            if not unused_correct_responses:
                unused_correct_responses = list(CORRECT_RESPONSES)
            this_response = unused_correct_responses[
                randrange(len(unused_correct_responses))]
            unused_correct_responses.remove(this_response)
            print(f"\n{this_response}\n")
            question_number += 1
            pause()
        else:
            # ! FOR TESTING ONLY
            print(INCORRECT_RESPONSES[randrange(len(INCORRECT_RESPONSES))])
            question_number = 0
            return question_number

        return question_number
