"""Handle questions"""

from html import unescape
from random import randrange, shuffle
import requests
from getch import pause

import tokens
import keywords
from matrix import matrix_line
from max_line_length import limit_line_length as shorten
from max_line_length import limit_answers as shorten_a
from prints import red_print, green_print, yellow_print

CORRECT_RESPONSES = (
    "Correct...", "Well done!", "That's right.",
    "You clearly know your stuff.", "That was...error-free!", "Spot on.",
    "Brilliant, that's correct.", "Nice work."
)
INCORRECT_RESPONSES = (
    "Oh dear, that's wrong I'm afraid.", "Oh no! That wasn't correct.",
    "Unfortunately, that answer was incorrect.", "Uh-oh! Game over for you.",
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
        question_data (dict): Question data retrived from opentdb.com
        choices (dict): Possible answers to question with assigned letters
        correct_answer (str): Correct answer letter
        review_used (bool): True if `review` keyword has been used in question
        longest_answer_length (int): Length of longest answer
        end_quiz (bool): True if incorrect answer given
        safety (int): 0, 1 or 2. Set by question number. Denotes that a safe
            point has been reached
    """

    def __init__(
        self, token: tokens.Token, difficulty: str,
        question_number: int, key_words: keywords.Keywords,
        user_name: str
    ) -> None:
        self.token = token
        # ? take from token.difficulty?
        self.difficulty = difficulty
        self.question_number = question_number
        self.keywords = key_words
        self.user_name = user_name
        self.question_data = self._check_and_retrieve()[1]["results"][0]
        self.choices, self.correct_answer = self._set_answer_letters()
        self.review_used = False
        self.longest_answer_length = self._get_longest_answer_length()
        self.end_quiz = False
        self.safety = 0

    def _get_longest_answer_length(self):
        """Get the length of the longest answer string

        ---
        Returns:
            int: Length of longest answer string
        """
        longest_answer_length = 0

        for k in self.choices:
            if len(self.choices[k]) > longest_answer_length:
                longest_answer_length = len(self.choices[k])

        if longest_answer_length > 60:
            longest_answer_length = 60

        return longest_answer_length

    def _reset_ready_words(self):
        """Repopulates ready words with original list"""

        global unused_ready_words
        unused_ready_words = list(READY_WORDS)

    def _check_and_retrieve(self) -> tuple:
        """Retrieve a response from opentdb API

        Connects to opentdb.com/api to ensure correct query
        parameters have been used in the URL, allowing for valid
        data

        Returns:
            tuple: (bool, dict[str, str])
                bool: True if response from API is 0, else false
                dict: The question in JSON format example:
                    {
                        "response_code":0,
                        "results":[
                            {
                                "category":"Science: Computers",
                                "type":"multiple", difficulty":"easy",
                                "question":"What is the domain name for the
                                    country Tuvalu?",
                                correct_answer":".tv",
                                "incorrect_answers":[
                                    ".tu",".tt",".tl"
                                    ]
                            }
                        ]
                    }
        """

        api_url = (
            "https://opentdb.com/api.php?amount=1&category"
            f"=18&difficulty={self.difficulty}&type=multiple"
            f"&token={self.token.string}"
        )

        yellow_print("\nRetrieving data...")
        response = requests.get(api_url)
        data = response.json()

        try:
            if response.status_code != 200:
                raise TypeError("API response missing")
            if "response_code" not in data:
                raise ValueError("API structure corrupt")
        except (TypeError, ValueError) as e:
            red_print(f"Critical Error: {e}")
            red_print("Program will now terminate!")
            exit()

        if data["response_code"] in (3, 4):
            red_print("Token expired:")
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
            red_print(f"Critical Error: {e}")
            red_print("Program will now terminate!")
            exit()

        green_print("Data retrieval successful...")
        return True, data

    def _set_answer_letters(self):
        """Give each answer a letter and determines the correct answer.

        Returns:
            tuple: (dict, str)
                dict[str, str]: Shuffled answers paired with a choice letter.
                str: The correct answer.
        """

        try:
            if (
                "correct_answer" not in self.question_data
                or "incorrect_answers" not in self.question_data
                or not isinstance(
                    self.question_data["correct_answer"], str)
                or not isinstance(
                    self.question_data["incorrect_answers"], list)
                or len(self.question_data["incorrect_answers"]) != 3
                or not isinstance(
                    self.question_data["incorrect_answers"][0], str)
                or not isinstance(
                    self.question_data["incorrect_answers"][1], str)
                or not isinstance(
                    self.question_data["incorrect_answers"][2], str)
            ):
                raise TypeError("API structure corrupt")
        except (TypeError, ValueError) as e:
            red_print(f"Critical Error: {e}")
            red_print("Program will now terminate!")
            exit()

        correct_answer = unescape(
            self.question_data["correct_answer"]
        ).strip()
        incorrect_answers = list(self.question_data["incorrect_answers"])
        for i in incorrect_answers:
            i = i.strip()
        answers = [correct_answer, *incorrect_answers]
        shuffle(answers)

        abcd = {
            "a": unescape(answers[0]),
            "b": unescape(answers[1]),
            "c": unescape(answers[2]),
            "d": unescape(answers[3]),
        }

        for k in abcd:
            if abcd[k] == correct_answer:
                correct_answer_letter = k

        return abcd, correct_answer_letter

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
            pre_question (str): A string to be prepended to the question
                number
            first_attempt (bool): (default: False) Determines if the
                prepending string needs defining

        Returns:
            str: (default: "") Generated prepend to question number. Default
                returned if not first_attempt
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
                f"\n{current_pre_question} Question Number "
                f"{str(self.question_number)}"
            )
        print(f"Followed by the {len(self.choices)} possible answers...\n")

        question_str = unescape(self.question_data["question"])

        shorten(question_str, True)

        print("")

        for letter, answer_str in self.choices.items():
            print(
                f"\033[33;1m{letter}:\033[0m "
                f"{shorten_a(unescape(answer_str))}"
            )

        return pre_question_str

    def run_question(self):
        """Runs the question

        Sets difficulty level depending on question number. Prints question and
        answers and available lifelines. Awaits user input that gets validated

        Returns:
            str: A validated user input
        """

        if self.question_number >= 6:
            self.safety = 1
        if self.question_number >= 11:
            self.safety = 2

        pre_question = self._display_question(None, True)

        while True:
            print(f"\nAvailable keywords:{self.keywords.available_keywords}")
            print(f"Available choices:{list(self.choices.keys())}")
            user_input = input(
                "Please provide your answer or enter a keyword:\n"
            ).lower().strip()
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
            new_input (str): The user's input string

        Returns:
            bool: True if answer is received, else False
        """

        try:
            if not new_input:
                raise ValueError("No input detected...")
            if (
                new_input in self.keywords.available_keywords
                or new_input == "tux"
            ):
                keyword_response = self.keywords.used(
                    new_input, self.choices, self.correct_answer,
                    self.user_name, self.question_number, self.review_used,
                    self.longest_answer_length, self.safety
                )
                if len(keyword_response):
                    self.choices = keyword_response[0]
                    if keyword_response[1]:
                        self.review_used = True
                    if keyword_response[2]:
                        self.end_quiz = True
                        return True
                return False
            if new_input not in self.choices:
                raise ValueError(
                    "Invalid input detected, please input an answer or "
                    "available keyword."
                )
        except ValueError as e:
            red_print(f"{e}\n")
            pause("\033[36;1mPress any key to continue...\033[0m")
            return False

        print("")
        if not keywords.Keywords.confirm(f"{new_input}"):
            return False

        return True

    def check_answer(
        self, user_input: str
    ):
        """Check user's answer against correct answer

        If the user answer is correct, increment the question number and allow
        the quiz to continue. Otherwise run through loss functions

        ---
        Args:
            user_input (str): The user's chosen letter

        Returns:
            int: The next question number (or safety number for quiz end)
            bool: True if quiz should end
        """

        global unused_correct_responses
        question_number = self.question_number

        if self.end_quiz:
            return question_number, True

        if user_input == self.correct_answer:
            if not unused_correct_responses:
                unused_correct_responses = list(CORRECT_RESPONSES)
            this_response = unused_correct_responses[
                randrange(len(unused_correct_responses))]
            unused_correct_responses.remove(this_response)
            green_print(f"\n{this_response}\n")
            question_number += 1
            pause("\033[36;1mPress any key to continue...\033[0m")
        else:
            self.end_quiz = True
            print("")
            red_print(INCORRECT_RESPONSES[randrange(len(INCORRECT_RESPONSES))])
            print("")
            matrix_line()
            if self.safety == 2:
                return 11, self.end_quiz
            elif self.safety == 1:
                return 6, self.end_quiz
            else:
                return 0, self.end_quiz

        return question_number, self.end_quiz
