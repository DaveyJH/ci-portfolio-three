"""Validate a yes/no input"""

from prints import red_print

YN = ("y", "n")


def validate_yes_no(input_string: str = "Please input 'y' or 'n':"):
    """Input string is validated with 'y' or 'n'

    Converts capital 'Y' and 'N' to lowercase

    ---
    Args:
        input_string (str): (default = "Please input 'y' or 'n':") The string
        to be printed as the input. Should clearly identify what information
        will be printed.

    Returns:
        bool: True if input is "y" - else False.
    """

    print(f"\n{input_string} \033[33m{YN}\033[0m\n")
    user_response = input().lower()
    while (
        not user_response.isalpha()
        or user_response not in YN
    ):
        red_print("\nInvalid input received")
        print("Please input 'y' or 'n'")
        user_response = input(f"{input_string} {YN}\n").lower()
        continue

    if user_response == "n":
        return False

    return True
