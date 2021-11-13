"""Run a quiz game via a CLI"""
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# ! line breaks before any print statement that follows an input

from better_profanity import profanity
from getch import pause


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

    user_response = input(f"\n{input_string} {YN}\n").lower()
    while (
        not user_response.isalpha()
        or user_response not in YN
    ):
        print("\nInvalid input received")
        print("Please input 'y' or 'n'")
        user_response = input(f"{input_string}{YN}\n").lower()
        continue

    if user_response == N:
        return False

    return True


def print_rules():
    """Prints the rules."""

    print("\n" + "THE RULES".center(40))
    print("=========".center(40))

    print("\nThis quiz consists of 15 questions. The further you go, the")
    print("harder they become. Unless, of course, you know the answers!")
    print("There is no time limit for the questions, but you do have")
    print("just one life. One wrong answer and the game is over.\n\n")
    print("If you answer 5 or 10 questions correctly, your progress is safe.")
    print("An incorrect answer any time after a safety point will mean your")
    print("score is equal to the most recent safety point reached.\n")

    pause()

    print("\nEach question has four possible answers: A, B , C and D.")
    print("You will be shown the question, followed by the four possible")
    print("answers, each preceded by a letter. Input your answer by use of")
    print("the (hopefully correct!) letter with no additional text. You will")
    print("be asked to confirm your answer. If you answer correctly, you move")
    print("on to the next question. Successfully answer all 15 questions to")
    print("win the ultimate gloating rights!\n")

    pause()

    print("\nThere are some keywords that can be used at any time.")
    print("'Help','Take', 'Scores', 'Review', 'Even' and 'Call'.")
    print("Once the quiz begins, these can be explained at any time via the")
    print("'Help' keyword. You will have an opportunity to run through their")
    print("uses in a moment.\n")

    print("Finally, and possibly most importantly...remember to have fun!\n")

    pause()


def which_keyword():
    """Allows user to specify which keyword meaning to check

    Returns:
        Keyword
    """

    print("\nWhich keyword would you like to check out?")
    user_input = input(f"{', '.join(KEYWORDS).title()}:\n").lower()
    while (
        not user_input.isalpha()
        or user_input not in KEYWORDS
    ):
        print("\nInvalid input received")
        print(f"Please input: {', '.join(KEYWORDS).title()}")
        user_input = input("Which keyword would you like to check?\n").lower()
        continue

    return user_input


def keyword_description(word: str):
    """Prints a description of the keyword

    Args:
        keyword: The keyword chosen by the user.
    """

    def print_title():
        """Prints the keyword title and an underline of equal length

        Args:
            index: The index of keyword in KEYWORDS to allow correct title to
                be printed.
        """

        print("\n" + f"{word.upper()}".center(40))
        line = "=" * len(word)
        print(f"{line.center(40)}\n")

    def print_content(description):
        """Prints the content explaining the keyword

        Args:
            index: The index of keyword in KEYWORDS to allow correct
                explanation to be printed.
        """

        print(f"{description}")

    print_title()
    for description in KEYWORDS[word]:
        print_content(description)
    print("")
    pause()


YN = ("y", "n")
Y = "y"
N = "n"
KEYWORDS = {
    "help": (
        "The 'help' keyword allows you to return to these handy tips.",
        "You will be asked if you would like to run through the rules again,",
        "then if you would like to run through the keywords and their",
        "functions. Once you are done, you will be returned to the quiz."
    ),
    "take": (
        "The 'take' keyword can be used when you are happy with your",
        "progress through the quiz and don't feel you can confidently",
        "continue. You will be asked to confirm your decision. If you do",
        "confirm, the quiz will end and your score will be recorded if it",
        "is in the top ten scores. If you change your mind and don't 'take'",
        "you will be returned to the quiz."
    ),
    "scores": (
        "The 'scores' keyword allows you to view the top 10 scores and the",
        "user names that achieved them. You will be prompted for an input and",
        "will subsequently return to the quiz."
    ),
    "review": (
        "This is a one shot keyword!! Once used, it cannot be used again in",
        "the same quiz!!\nIf you choose to use 'review', you will need to",
        "confirm your decision. Once you do, you will be presented with",
        "answers to the current question from 100 people. They may not be",
        "correct so it is up to you if you take the majority answers or not.",
        "You will be prompted to return to the question and may then continue."
    ),
    "even": (
        "This is a one shot keyword!! Once used, it cannot be used again in",
        "the same quiz!!\nIf you choose to use 'even', you will need to",
        "confirm your decision. Once you do, two of the incorrect answers",
        "to the current question will be removed. The question will be shown",
        "again with only the two remaining answers. This will even the odds."
    ),
    "call": (
        "This is a one shot keyword!! Once used, it cannot be used again in",
        "the same quiz!!\nIf you choose to use 'call', you will need to",
        "confirm your decision. Once you do, you will be presented with",
        "a response from a coder companion. They will give you their thoughts",
        "on the question. However, they may not be correct so it is up to you",
        "to make the final decision",
        "You will be prompted to return to the question and may then continue."
    )
}


print("Welcome!\nAre you clued up enough on code and computers?")
print("Think you have the knowledge to go all the way?")
print("Let's see how you do! First, introduce yourself.\n")

user_name = get_user_name()
print(f"\nWelcome, {user_name}!")

WANTS_RULES = "Before we begin, should we run through the rules?"
WANTS_KEYWORDS = "Would you like to know a keyword and its function?"


def main():
    """Runs the quiz."""
    if wants_info(WANTS_RULES):
        print_rules()


while wants_info(WANTS_KEYWORDS):
    keyword = which_keyword()
    keyword_description(keyword)

print("\nGreat...let's begin!")
