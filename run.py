"""Run a quiz game via a CLI"""
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# ! line breaks before any print statement that follows an input

from random import shuffle
from html import unescape
from better_profanity import profanity
from getch import pause

import requests


def retrieve_api_token(difficulty) -> str:
    """Retrieve and validate API token

    Connects to opentdb.com/api to retrieve fresh token to prevent duplicate
    questions. Token lasts for 6 hours. If user plays multiple times within 6
    hours, token must be reset.

    Returns:
        API token
    """

    print(f"Retrieving new {difficulty} token...")

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
        print(f"Error: {e}")
        print("Program will now terminate!")
        exit()

    print("Token retrieval successful!")
    return data["token"]


def initial_token_setup():
    """Initialise easy, medium and hard API tokens.

    Returns:
        Easy, medium and hard token strings in order."""

    new_easy_token = retrieve_api_token("easy")
    new_medium_token = retrieve_api_token("medium")
    new_hard_token = retrieve_api_token("hard")
    return new_easy_token, new_medium_token, new_hard_token


def introduction_to_quiz():
    """Print initial welcome strings and allow user to input username.

    Returns:
        string: Validated username
    """
    print("\n\nWelcome!\nAre you clued up enough on code and computers?")
    print("Think you have the knowledge to go all the way?")
    print("Let's see how you do! First, introduce yourself.\n")

    new_user_name = get_user_name()
    print(f"\nWelcome, {new_user_name}!")

    return new_user_name


def get_user_name():
    """Allows user to input a username.

    User input to choose a user name. Alphanumeric characters and spaces are
    valid. Profanity blocked by `better_profanity`. Input repeats until valid
    input received.

    Returns:
        string: A validated string as a username.
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
        bool: True if valid - else false.
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
        bool: True if input is "y" - else False.
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
        string: Keyword input by user.
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
        "the same quiz!!    --    Use it wisely!!",
        "If you choose to use 'review', you will need to confirm your",
        "decision. Once you do, you will be presented with answers to the",
        "current question from 100 people. They may not be correct so it is",
        "up to you if you take the majority answers or not.",
        "You will be prompted to return to the question and may then continue."
    ),
    "even": (
        "This is a one shot keyword!! Once used, it cannot be used again in",
        "the same quiz!!    --    Use it wisely!!",
        "If you choose to use 'even', you will need to confirm your",
        "decision. Once you do, two of the incorrect answers to the current",
        "question will be removed. The question will be shown again with only",
        "the two remaining answers. This will even the odds."
    ),
    "call": (
        "This is a one shot keyword!! Once used, it cannot be used again in",
        "the same quiz!!    --    Use it wisely!!",
        "If you choose to use 'call', you will need to confirm your",
        "decision. Once you do, you will be presented with a response from a",
        "coder companion. They will give you their thoughts on the question.",
        "However, they may not be correct, so it is up to you to make the",
        "final decision.",
        "You will be prompted to return to the question and may then continue."
    )
}

WANTS_RULES = "Before we begin, should we run through the rules?"
WANTS_KEYWORDS = "Would you like to know a keyword and its function?"

easy_token, medium_token, hard_token = initial_token_setup()


def main():
    """Runs the quiz."""

    # user_name = introduction_to_quiz()

    # if wants_info(WANTS_RULES):
        # print_rules()

    # while wants_info(WANTS_KEYWORDS):
        # keyword = which_keyword()
        # keyword_description(keyword)

    print("\nGreat...let's begin!")


def check_api_retrieve_question(
    difficulty: str, token: str
) -> tuple[bool, object]:
    """Retrieve a response from opentdb API.

    Connects to opentdb.com/api to ensure correct query parameters have been
    used in the URL, allowing for valid data.

    Args:
        difficulty: The current difficulty level set by the question number

    Returns:
        tuple: (bool, data)
            bool: True if response from API is 0, else false.
            data: The response in JSON format.
    """
    api_url = (
        "https://opentdb.com/api.php?amount=1&category"
        f"=18&difficulty={difficulty}&type=multiple&token={token}"
    )

    print("Retrieving data...")
    response = requests.get(api_url)
    data = response.json()

    if data["response_code"] in (3, 4):
        print("Token expired:")
        new_token = retrieve_api_token(difficulty)
        data = check_api_retrieve_question(difficulty, new_token)[1]
        return True, data, new_token

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


def display_question(question):
    """Shows question and possible answers"""

    correct_answer = unescape(question["correct_answer"])
    incorrect_answers = list(unescape(question["incorrect_answers"]))
    answers = [correct_answer, *incorrect_answers]
    shuffle(answers)

    abcd: dict[str, str] = {
        "a": unescape(answers[0]),
        "b": unescape(answers[1]),
        "c": unescape(answers[2]),
        "d": unescape(answers[3]),
    }

    # use a tuple of 'ready' 'ok' 'here we go' etc
    print(f"\nReady? Question number {str(question_number)}")
    print("Followed by the four possible answers...\n")
    print(f"{unescape(question['question'])}\n")
    for letter, answer_str in abcd.items():
        print(f"{letter}:", answer_str)

    return abcd, correct_answer


api_check_result = check_api_retrieve_question("easy", easy_token)
if len(api_check_result) == 3:
    easy_token = api_check_result[2]

question_number = 1
question_data = api_check_result[1]["results"]
choices, answer = display_question(question_data[0])

print("")
print(choices)
print(answer)


# api_validated = api_check[0]
# print("")

main()
