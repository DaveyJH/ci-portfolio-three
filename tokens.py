"""Handle token collection and storing"""

import requests

from sheets import TOKEN_SHEET
from matrix import matrix_block, matrix_line
from prints import red_print, green_print, cyan_print, yellow_print


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
        self.string = self._get_stored_token_string()

    def _get_stored_token_string(self) -> str:
        """Retrieve and validate API token

        ---
        Args:
            difficulty (str): 'easy', 'medium' or 'hard'

        Returns:
            Token string value
        """

        cyan_print(f"Checking for existing {self.difficulty} token...")
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
            if response.status_code != 200:
                raise TypeError("API response missing")
            if "response_code" not in data:
                raise ValueError("API structure corrupt")
            if data["response_code"] != 0:
                raise ConnectionError("No valid token found...")
            if data["response_code"] == 0:
                green_print("Token retrieval successful!")
        except ConnectionError as e:
            red_print(f"Report: {e}")
            return self.initiate_new_token_string()
        except (TypeError, ValueError) as e:
            red_print(f"Critical Error: {e}")
            red_print("Program will now terminate!")
            exit()

        return token

    def initiate_new_token_string(self):
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

        yellow_print(f"Retrieving new {self.difficulty} token...")
        matrix_block(2)

        token_url = "https://opentdb.com/api_token.php?command=request"
        response = requests.get(token_url)
        data = response.json()

        try:
            if response.status_code != 200:
                raise TypeError("API response missing")
            if "response_code" not in data:
                raise ValueError("API structure corrupt")
            if data["response_code"] != 0:
                raise ConnectionError(
                    f"Open Trivia Database API connection error: {token_url}\n"
                    f"Response_code from API: {data['response_code']}"
                )
        except (ValueError, ConnectionError, TypeError) as e:
            red_print(f"Critical Error: {e}")
            red_print("Program will now terminate!")
            exit()

        green_print("Token retrieval successful!")

        yellow_print("Updating stored token...")
        if self.difficulty == "easy":
            TOKEN_SHEET.update_acell("A2", data["token"])
        elif self.difficulty == "medium":
            TOKEN_SHEET.update_acell("B2", data["token"])
        else:
            TOKEN_SHEET.update_acell("C2", data["token"])
        green_print(
            f"{self.difficulty.capitalize()} token successfully "
            "updated..."
        )
        matrix_line()

        return data["token"]


def initial_token_setup():
    """Initialise easy, medium and hard Tokens

    ---
    Returns:
        tuple (obj, obj, obj):
            obj: Easy token
            obj: Medium token
            obj: Hard token
    """

    new_easy_token_obj = Token("easy")
    new_medium_token_obj = Token("medium")
    new_hard_token_obj = Token("hard")
    return new_easy_token_obj, new_medium_token_obj, new_hard_token_obj
