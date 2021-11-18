"""Handle token collection and storing"""

import requests

from sheets import TOKEN_SHEET
from matrix import matrix_block, matrix_line


class Token():
    """Creates a token from the difficulty and provides a string value

    Checks Google Sheets for valid token

    If token is invalid, connects to opentdb.com/api to retrieve fresh token
    to prevent duplicate questions. Token lasts for 6 hours. If questions are
    used up within 6 hours, token must be reset

    Stores valid token string in Google Sheets

    ---
    Attributes:
        difficulty (str): 'easy', 'medium' or 'hard'
        string: Token string value
    """

    def __init__(self, difficulty: str):
        self.difficulty = difficulty
        self.string = self._get_stored_token()

    def _get_stored_token(self) -> str:
        """Retrieve and validate API token

        ---
        Args:
            difficulty (str): 'easy', 'medium' or 'hard'

        Returns:
            Token string value
        """

        print(f"Checking for existing {self.difficulty} token...")
        matrix_block(2)

        if self.difficulty == "easy":
            token = TOKEN_SHEET.acell("A2").value
        elif self.difficulty == "medium":
            token = TOKEN_SHEET.acell("B2").value
        else:
            token = TOKEN_SHEET.acell("C2").value

        token_test_url = f"https://opentdb.com/api.php?amount=1&token={token}"
        response = requests.get(token_test_url)
        data = response.json()

        try:
            if data["response_code"] != 0:
                raise ConnectionError("No valid token found...")
            if data["response_code"] == 0:
                print("Token retireval successful!")
                return token
        except ConnectionError as e:
            print(f"Report: {e}")
            return self._initiate_new_token()

    def _initiate_new_token(self):
        """Request new token from opentdb.com and updates Google Sheet

        ---
        Args:
            difficulty (str): 'easy', 'medium' or 'hard'

        Returns:
            New token string value

        Raises:
            ConnectionError: Open Trivia Database API connection error
                `TERMINATES PROGRAM`
        """

        print(f"Retrieving new {self.difficulty} token...")
        matrix_block(2)

        token_url = "https://opentdb.com/api_token.php?command=request"
        response = requests.get(token_url)
        data = response.json()

        try:
            if data["response_code"] != 0:
                raise ConnectionError(
                    f"Open Trivia Database API connection error: {token_url}\n"
                    f"Response_code from API: {data['response_code']}"
                )
        except ConnectionError as e:
            print(f"Critical Error: {e}")
            print("Program will now terminate!")
            exit()

        print("Token retrieval successful!")

        print("Updating stored token...")
        if self.difficulty == "easy":
            TOKEN_SHEET.update_acell("A2", data["token"])
        elif self.difficulty == "medium":
            TOKEN_SHEET.update_acell("B2", data["token"])
        else:
            TOKEN_SHEET.update_acell("C2", data["token"])
        print(f"{self.difficulty.capitalize()} token successfully updated...")
        matrix_line()

        return data["token"]

    def return_token_string(self):
        """Returns the token string from the object"""

        return self.string


def initial_token_setup():
    """Initialise easy, medium and hard Tokens

    ---
    Returns:
        tuple (obj, obj, obj):
            obj: Easy token.
            obj: Medium token.
            obj: Hard token.
    """

    new_easy_token_obj = Token("easy")
    new_medium_token_obj = Token("medium")
    new_hard_token_obj = Token("hard")
    return new_easy_token_obj, new_medium_token_obj, new_hard_token_obj
