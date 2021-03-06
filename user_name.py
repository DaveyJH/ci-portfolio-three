"""Handles user_name creation and validation"""

from better_profanity import profanity

from prints import red_print


class User():
    """Creates a User object

    ---
    Attributes:
        user_name (str): A validated user_name string chosen by user input
    """

    def __init__(self):
        self.user_name = self._get_user_name()

    def _get_user_name(self):
        """Allows user to input a username

        User input to choose a user name. Alphanumeric characters and spaces
        are valid. Profanity blocked by `better_profanity`. Input repeats
        until valid input received

        ---
        Returns:
            str: A validated string as a username
        """

        while True:
            print("Characters A-Z, a-z, 0-9 and spaces are permitted.")
            print("Maximum user name length of 18 characters.")
            print("Leading and trailing whitespaces will be removed.\n")
            new_user_name = input("Please enter a user name:\n")
            if self._check_user_name(new_user_name):
                break

        return new_user_name.strip()

    def _check_user_name(self, user_name_str: str):
        """Checks username input is valid

        ---
        Args:
            user_name_str (str): The string input from a user to be validated

        Returns:
            bool: True if valid - else False
        """

        try:
            if not user_name_str:
                raise ValueError("You must enter a user name")
            if not "".join(user_name_str.split()).isalnum():
                raise ValueError("Invalid characters detected")
            if profanity.contains_profanity(user_name_str):
                raise ValueError("Profanity detected")
            if len(user_name_str) > 18:
                raise ValueError("User name too long")

        except ValueError as e:
            red_print(f"Invalid data: {e}, please try again.\n")
            return False

        return True
