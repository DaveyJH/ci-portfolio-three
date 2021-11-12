"""Run a quiz game via a CLI"""
# Write your code to expect a terminal of 80 characters wide and 24 rows high

from better_profanity import profanity


def get_user_name():
    """Allows user to input a username.

    User input to choose a user name. Alphanumeric characters and spaces are
    valid. Profanity blocked by `better_profanity`. Input repeats until valid
    input received.

    Returns:
        A string as a username.
    """

    while True:
        print("Characters A-Z, a-z, 0-9 and spaces are permitted.")
        print("Leading and trailing whitespaces will be removed.\n")
        new_user_name = input("Please enter a user name:\n")
        if check_user_name(new_user_name):
            break

    return new_user_name.strip()


def check_user_name(user_name_str: str):
    """Checks username input is valid.

    Returns:
        True if valid - else false.
    """

    try:
        if not user_name_str:
            raise ValueError("You must enter a user name")
        if not "".join(user_name_str.split()).isalnum():
            raise ValueError("Invalid characters detected")
        if profanity.contains_profanity(user_name_str):
            raise ValueError("Profanity detected")

    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def wants_info(input_string: str):
    """User selects whether to print info or not.

    Args:
        input_string: The string to be printed as the input. Should clearly
            identify what information will be printed.

    Returns:
        True if input is "y" - else False.
    """

    user_response = input(f"{input_string} {YN}\n").lower()
    while (
        not user_response.isalpha()
        or user_response not in YN
    ):
        print("\nInvalid input received")
        print("Please input 'y' or 'n'")
        user_response = input(f"{input_string}\n").lower()
        continue

    if user_response == N:
        return False

    return True


def print_rules():
    """Prints the rules."""

    print("\nthis is the rule")
    print("this is the 2nd rule")
    print("this is the 3rd rule")
    print("this is the 4th rule")
    print("this is the 5th rule\n")


YN = ("y", "n")
Y = "y"
N = "n"

print("Welcome! Are you clued up enough on code and computers?")
print("Think you have the knowledge to go all the way?")
print("Let's see how you do! First, introduce yourself.\n")

user_name = get_user_name()
print("")
print(f"Welcome, {user_name}!\n")

WANTS_RULES = "Before we begin, should we run through the rules?"

if wants_info(WANTS_RULES):
    print_rules()


# input y/n show rules
print("Would you like to know the keywords?")
# input y/n show keywords
print("Great...let's begin!")
