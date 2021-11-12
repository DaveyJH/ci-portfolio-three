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

    print("\n" + "THE RULES".rjust(30))
    print("=========".rjust(30))

    print("\nThis quiz consists of 15 questions. The further you go, the")
    print("harder they become. Unless, of course, you know the answers!")
    print("There is no time limit for the questions, but you do have")
    print("just one life. One wrong answer and the game is over.\n")

    print("Each question has four possible answers: A, B , C and D.")
    print("You will be shown the question, followed by the four possible")
    print("answers, each preceded by a letter. Input your answer by use of")
    print("the (hopefully correct!) letter with no additional text. You will")
    print("be asked to confirm your answer. If you answer correctly, you move")
    print("on to the next question. Successfully answer all 15 questions to")
    print("win the ultimate gloating rights!\n")

    print("Press a key to continue...\n")

    print("There are some keywords that can be used at any time.")
    print("'Help','Take', 'Scores', 'Review', 'Even' and 'Call'.")
    print("Once the quiz begins, these can be explained at any time via the")
    print("'Help' keyword. You will have an opportunity to run through their")
    print("uses in a moment.\n")

    print("Finally, and possibly most importantly...remember to have fun!\n")

    print("Press a key to continue...\n")


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
