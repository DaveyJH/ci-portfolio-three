"""Run a quiz game via a CLI"""
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# ! line breaks before any print statement that follows an input

from random import randrange, shuffle
from html import unescape
from time import sleep

import requests
import gspread
from google.oauth2.service_account import Credentials
from better_profanity import profanity
from getch import pause

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("ci_p3_quiz")

TOKEN_SHEET = SHEET.worksheet("tokens")
SCORES_SHEET = SHEET.worksheet("scores")


def matrix_line():
    """Print a random line of 60 1s and 0s followed by a 0.5s delay"""

    line = ""
    for n in range(80):
        line = line + (str(MATRIX_CHARS[
            randrange(len(MATRIX_CHARS))]))
    print(line)
    sleep(.5)


def matrix_block(num: int = 5):
    """Print block of matrix lines

    Args:
        num: Integer value determining how many lines to print.
    """

    for n in range(num):
        matrix_line()


def retrieve_api_token(difficulty: str) -> str:
    """Retrieve and validate API token

    Checks Google Sheets for valid token. If token is invalid,
    connects to opentdb.com/api to retrieve fresh token to prevent duplicate
    questions. Token lasts for 6 hours. If user plays multiple times within 6
    hours, token must be reset.

    Args:
        difficulty: Easy, medium or hard.

    Returns:
        str: API token.
    """

    print(f"Checking for existing {difficulty} token...")
    matrix_block(2)

    if difficulty == "easy":
        token = TOKEN_SHEET.acell("A2").value
    elif difficulty == "medium":
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
            print("Token retireval successful")
            return token
    except ConnectionError as e:
        print(f"Report: {e}")

    print(f"Retrieving new {difficulty} token...")
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
        print(f"Error: {e}")
        print("Program will now terminate!")
        exit()

    print("Token retrieval successful!")

    print("Updating stored token...")
    if difficulty == "easy":
        token = TOKEN_SHEET.update_acell("A2", data["token"])
    elif difficulty == "medium":
        token = TOKEN_SHEET.update_acell("B2", data["token"])
    else:
        token = TOKEN_SHEET.update_acell("C2", data["token"])
    print(f"{difficulty.capitalize()} token updated...")
    matrix_line()

    return data["token"]


def initial_token_setup():
    """Initialise easy, medium and hard API tokens.

    Returns:
        tuple (str, str, str):
            str: Easy token string.
            str: Medium token string.
            str: Hard token string.
    """

    new_easy_token = retrieve_api_token("easy")
    new_medium_token = retrieve_api_token("medium")
    new_hard_token = retrieve_api_token("hard")
    return new_easy_token, new_medium_token, new_hard_token


def introduction_to_quiz():
    """Print initial welcome strings and allow user to input username.

    Returns:
        str: Validated username.
    """
    print(f"\n{80*'='}")
    print("\nWelcome!\nAre you clued up enough on code and computers?")
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
        str: A validated string as a username.
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

    Args:
        user_name_str: The string input from a user to be validated.

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
    print("just one life. One wrong answer and the game is over.\n")
    print("If you answer 5 or 10 questions correctly, your progress is safe.")
    print("An incorrect answer any time after a safety point will mean your")
    print("score is equal to the most recent safety point reached.\n")

    pause()

    print("\nEach question has four possible answers: A, B, C and D.")
    print("You will be shown the question, followed by the four possible")
    print("answers, each preceded by a letter. Input your answer by use of")
    print("the (hopefully correct!) letter with no additional text. You will")
    print("be asked to confirm your answer. If you answer correctly, you move")
    print("on to the next question. Successfully answer all 15 questions to")
    print("win the ultimate gloating rights!\n")

    pause()

    print("\nThere are some keywords that can be used at any time.")
    print("'Help', 'Take', 'Scores', 'Review', 'Even' and 'Call'.")
    print("Once the quiz begins, these can be explained at any time via the")
    print("'Help' keyword. You will have an opportunity to run through their")
    print("uses in a moment.\n")

    print("Finally, and possibly most importantly...remember to have fun!\n")

    pause()


def which_keyword():
    """Allows user to specify which keyword meaning to check

    Returns:
        str: Keyword input by user.
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


def check_api_retrieve_question(
    difficulty: str, token: str
) -> tuple:
    """Retrieve a response from opentdb API.

    Connects to opentdb.com/api to ensure correct query parameters have been
    used in the URL, allowing for valid data.

    Args:
        difficulty: The current difficulty level set by the question number

    Returns:
        tuple: (bool, dict[str, str], str)
            bool: True if response from API is 0, else false.
            dict[str, str]: The response in JSON format.
            *str: New token string if token has expired.
    """
    api_url = (
        "https://opentdb.com/api.php?amount=1&category"
        f"=18&difficulty={difficulty}&type=multiple&token={token}"
    )

    print("\nRetrieving data...")
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


def set_answer_letters(question: dict):
    """Give each answer a letter and determines the correct answer.

    Args:
        question: The current question.


    Returns:
        tuple: (dict, str)
            dict[str, str]: Shuffled answers paired with a choice letter.
            str: The correct answer.
    """
    correct_answer = unescape(question["correct_answer"])
    incorrect_answers = list(question["incorrect_answers"])
    answers = [correct_answer, *incorrect_answers]
    shuffle(answers)

    abcd = {
        "a": unescape(answers[0]),
        "b": unescape(answers[1]),
        "c": unescape(answers[2]),
        "d": unescape(answers[3]),
    }

    return abcd, correct_answer


def display_question(
    question: str, abcd: dict,
    current_pre_question: str, first_attempt: bool = False
):
    """Prints question and possible answers

    Prints a single matrix_line for visual clarity.

    Prints a pre_question string, the question and the possible answers. If
    it is the first time the question has been printed, a random string will
    be prepended to the Question Number x.

    Questions longer than 80 characters are split over individual lines and
    spaces are trimmed to prevent single space indent on new line.

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
            unused_ready_words = list(READY_WORDS)
        pre_question_str = unused_ready_words[
            randrange(len(unused_ready_words))]
        unused_ready_words.remove(pre_question_str)
    if pre_question_str:
        print(f"\n{pre_question_str} Question Number {str(question_number)}")
    else:
        print(
            f"\n{current_pre_question} Question Number {str(question_number)}"
        )
    print(f"Followed by the {len(abcd)} possible answers...\n")

    question_str = unescape(question["question"])
    question_lines = []

    if len(question_str) <= 80:
        question_lines.append(question_str)
    else:
        while len(question_str) > 80:
            question_str = question_str.strip()
            q_line = question_str[:80]
            if question_str[80] == " ":
                question_lines.append(q_line)
                question_str = question_str[80:]
            elif " " in q_line:
                last_space = q_line.rindex(" ")
                q_line = question_str[:last_space]
                question_str = question_str[last_space:].strip()
                question_lines.append(q_line)
            else:
                question_lines.append(q_line)
        question_lines.append(question_str.strip())

    for line in question_lines:
        print(line)

    print("")
    for letter, answer_str in abcd.items():
        print(f"{letter}: {answer_str}")

    return pre_question_str


def initiate_question(difficulty: str, token: str):
    """Check and set up question.

    Check for valid token and updates if necessary. Retrieves question string,
    choices and answer. Sets string to be used before instance of question.

    Args:
        difficulty: A string value containing the current difficulty.
        token: A string value of the current API token in use.

    Returns:
        str: A valid APi token.
        str: A string to prepend the question.
        dict[str, str]: The question data in a dictionary. Example...
            {
                "category":"Example Questions",
                "type":"multiple",      # multiple or boolean
                "difficulty":"easy",
                "question":"What is 2 + 2",
                "correct_answer":"4",
                "incorrect_answers":[
                    "5",
                    "8",
                    "0"
                ]
            }
        dict[str, str]: Letters with a shuffled set of answers assigned to them
            to allow user selection. Example...
                {
                    "a": "8",
                    "b": "0",
                    "c": "4",
                    "d": "5"
                }
        str: The answer to the question as a string. Example....
            "4"
    """

    update_token = token
    api_return = check_api_retrieve_question(difficulty, token)
    if len(api_return) == 3:
        # update google sheet
        update_token = api_return[2]

    question_data = api_return[1]["results"]
    choices, answer = set_answer_letters(question_data[0])
    pre_question_str = display_question(question_data[0], choices, "", True)

    # ! DELETE BEFORE DEPLOYMENT TESTING ONLY
    # print("")
    # print(answer)

    return update_token, pre_question_str, question_data, choices, answer


def check_input(new_input: str, choices: dict, answer: str):
    """Validates user's input after question is printed.

    Checks for valid user input and checks if keyword has been used.

    Args:
        new_input: The user's input string.
        choices: A dictionary of letters and their associated answer.
        answer: The current question answer as a string.

    Returns:
        bool: True if answer is received, else False and continue user input.
        dict[str, str]: Available answer choices.
    """

    try:
        if not new_input:
            raise ValueError("No input detected...")
        # change to available keywords
        if new_input in KEYWORDS and new_input in available_keywords:
            choices = keyword_used(new_input, choices, answer)
            return False, choices
        if new_input not in choices:
            raise ValueError(
                "Invalid input detected, please input an answer or available"
                " keyword."
            )

    except ValueError as e:
        print(f"{e}\n")
        pause()
        return False, choices

    return True, choices


def run_question(question_num: int):
    """Runs the question.

    Sets difficulty level depending on question number. Prints question and
    answers and available lifelines. Awaits user input that gets validated.

    Args:
        question_num: The current question number.

    Returns:
        str: A validated user input.
        dict[str, str]: The answers with a key letter for user selection.
        str: The question answer.
    """

    if question_num < 6:
        current_difficulty = DIFFICULTY_LEVELS[0]
        current_token = easy_token
    elif question_num < 11:
        current_difficulty = DIFFICULTY_LEVELS[1]
        current_token = medium_token
    else:
        current_difficulty = DIFFICULTY_LEVELS[2]
        current_token = hard_token

    (
        current_token,
        pre_question,
        question_data,
        choices,
        answer
    ) = initiate_question(current_difficulty, current_token)

    while True:
        print(f"\nAvailable keywords:{available_keywords}")
        print(f"Available choices:{list(choices.keys())}")
        user_input = input(
            "Please provide your answer or enter a keyword:\n"
        ).lower()
        input_check = check_input(user_input, choices, answer)
        if not input_check[0]:
            choices = input_check[1]
            display_question(question_data[0], choices, pre_question)
        else:
            break

    return user_input, choices, answer


def check_answer(user_input: str, choices: dict, answer: str):
    """Check user's answer against correct answer

    If the user answer is correct, increment the question number and allow
    the quiz to continue. Otherwise run through loss functions.

    Args:
        user_input: The user's chosen letter.
        choices: Letters with their assigned answer.
        answer: The answer string to the question.
    """

    global unused_correct_responses
    global question_number

    if choices[user_input] == answer:
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
        exit()


def keyword_help(initial_run: bool = False):
    """Runs through explanations of rules and keywords.

    Args:
        initial_run: If True, modifies input string before rules to
            WANTS_RULES. (default: False)
    """
    rules = WANTS_RULES if initial_run else REFRESH_RULES
    if wants_info(rules):
        print_rules()

    while wants_info(WANTS_KEYWORDS):
        keyword = which_keyword()
        keyword_description(keyword)


def keyword_take():
    """Ends the quiz and logs the score."""

    print("\nDo you want to end here?")
    confirm = input("Please input 'take' again to confirm exit:\n")

    if confirm != "take":
        print("Input did not match.\n")
        return

    # testing
    print("TOOK THE MONEY")
    # ??restart?
    exit()


def keyword_scores():
    """Prints the current high scores from Google Sheet data."""

    print("THE SCORES ARE...")


def keyword_even(
    current_choices: dict, correct_answer: str
) -> dict:
    """Removes 2 incorrect answers from the choices.

    Requires confirmation of input. If input string does not match, revert to
    user input.

    Args:
        current_choices: A dictionary of the currently available letters and
            answers.
        correct_answer: The correct answer string.

    Returns:
        dict[str, str]: (If even confirmed) One correct answer, one incorrect
        answer. Assigned letters remain the same and order is alphabetical.
    """

    print("\nWould you like to even the odds?")
    confirm = input("Please input 'even' again to confirm choice:\n")
    if confirm != "even":
        print("Input did not match.\n")
        return current_choices
    available_keywords.remove("even")

    new_choices = {}
    for k, v in current_choices.items():
        if v == correct_answer:
            new_choices.update({k: v})
            del current_choices[k]
            break
    incorrect_answer = list(
        current_choices.items()
    )[randrange(len(current_choices))]

    new_choices.update({incorrect_answer[0]: incorrect_answer[1]})

    new_items = new_choices.items()
    sorted_items = sorted(new_items)
    new_choices = dict(sorted_items)

    print("\nEvening the odds...\n")
    sleep(.5)
    print("Recalculating...\n")
    sleep(.5)
    print("Calculation successful!\n")
    sleep(.5)

    return new_choices


def keyword_review(
    current_choices: dict, correct_answer: str
):
    """Prints percentages next to avilable choices.

    Calculates a percentage response for each available answer. Chance of
    response being correct is lower for higher number questions. Prints
    responses in similar style to available answers.

    Args:
        current_choices: A dictionary of the currently available letters and
            answers.
        correct_answer: The correct answer string.
    """

    print("\nWould you like to request a review?")
    confirm = input("Please input 'review' again to confirm choice:\n")
    if confirm != "review":
        print("Input did not match.\n")
        return
    available_keywords.remove("review")

    reviewed_answers = current_choices.copy()
    reviews = {}

    if question_number < 6:
        percentage = randrange(50, 80)
    elif question_number < 11:
        percentage = randrange(20, 60)
    else:
        percentage = randrange(10, 40)

    if len(current_choices) == 2:
        r_a = 100 - percentage
        incorrect_percentages = [r_a]
    else:
        remainder = 100 - percentage
        r_a = randrange(round(remainder / 2))
        remainder = remainder - r_a
        r_b = randrange(remainder)
        r_c = remainder - r_b
        incorrect_percentages = [r_a, r_b, r_c]

    for k, v in reviewed_answers.items():
        if v == correct_answer:
            reviews.update({k: f"{percentage}%"})
            del reviewed_answers[k]
            break

    while reviewed_answers:
        incorrect_answer = list(
            reviewed_answers.items()
        )[randrange(len(reviewed_answers))]
        incorrect_answer_percentage = incorrect_percentages[
            randrange(len(incorrect_percentages))
        ]
        reviews.update({
            incorrect_answer[0]:
            f"{incorrect_answer_percentage}%"
        })

        del reviewed_answers[incorrect_answer[0]]
        incorrect_percentages.remove(incorrect_answer_percentage)

    new_items = reviews.items()
    sorted_items = sorted(new_items)
    reviews = dict(sorted_items)

    print("\nRequesting review...\n")
    sleep(.5)
    print("Collating responses...\n")
    sleep(.5)
    print("Rendering results...\n")
    sleep(.5)

    for letter, review in reviews.items():
        print(f"{letter}: {review}")

    print("")
    pause()
    print("")


def keyword_call(current_choices: dict, correct_answer: str):
    """Prints a string with a suggested answer.

    Calculates a percentage response for each available answer. Chance of
    response being correct is lower for higher number questions. Prints
    responses in similar style to available answers.

    Args:
        current_choices: A dictionary of the currently available letters and
            answers.
        correct_answer: The correct answer string.
    """

    print("\nWould you like to call a coder?")
    confirm = input("Please input 'call' again to confirm choice:\n")
    if confirm != "call":
        print("Input did not match.\n")
        return
    available_keywords.remove("call")

    if question_number < 6:
        percentage = randrange(50, 80)
    elif question_number < 11:
        percentage = randrange(20, 60)
    else:
        percentage = randrange(10, 40)

    coder_guess = list(current_choices)[randrange(len(current_choices))]

    for k, v in current_choices.items():
        if v == correct_answer and percentage > 50:
            coder_guess = k

    if question_number < 6:
        coder_responses = (
            f"You came to the right coder, 100% it is '{coder_guess}'.",
            f"'{coder_guess}', I am sure of it.",
            f"I think I am right in saying '{coder_guess}'. I'm confident.",
            f"Easy one for me, that's '{coder_guess}'."
        )
    if question_number < 11:
        coder_responses = (
            f"I'm pretty confident with this one, it's '{coder_guess}'",
            f"It has to be '{coder_guess}', I am almost certain.",
            f"I could be wrong, but I would say it is '{coder_guess}'",
            f"That's a little tricky but '{coder_guess}' seems to be the one"
        )
    else:
        coder_responses = (
            f"I'm not sure on this, it could be '{coder_guess}'.",
            f"That is tricky. I would say '{coder_guess}', but I am guessing",
            f"It might be '{coder_guess}', but I really am not sure.",
            f"Wow, that's tough. I'd say '{coder_guess}', but it's a stab in "
            "the dark."
        )

    print("\nCalling a coder...\n")
    sleep(.5)
    print("Call connected...\n")
    sleep(.5)
    print("Providing possibilities...\n")
    sleep(.5)

    print(f"{coder_responses[randrange(len(coder_responses))]}")

    print("")
    pause()
    print("")


def keyword_used(
    word: str, current_choices: dict, correct_answer: str
):
    """Run keyword function"""

    new_choices = current_choices

    if word == "help":
        keyword_help()
        print("\nLet's return to the quiz!")
        pause()
    if word == "take":
        keyword_take()
    if word == "scores":
        keyword_scores()
        print("\nLet's return to the quiz!")
        pause()

    if word == "even":
        if "even" in available_keywords:
            new_choices = keyword_even(current_choices, correct_answer)
    if word == "review":
        if "review" in available_keywords:
            keyword_review(current_choices, correct_answer)
    if word == "call":
        if"call" in available_keywords:
            keyword_call(current_choices, correct_answer)

    return new_choices


def main():
    """Runs the quiz."""

    user_name = introduction_to_quiz()

    keyword_help(True)

    print("\nGreat...let's begin!")

    while question_number < 16:

        user_input, choices, answer = run_question(question_number)
        check_answer(user_input, choices, answer)


MATRIX_CHARS = (1, 0)
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
        "decision. Once you do, you will be presented with the responses from",
        "100 people to the current question. They may not be correct so it is",
        "up to you if you take the majority answer or not.",
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
available_keywords = list(KEYWORDS.keys())
WANTS_RULES = "Before we begin, should we run through the rules?"
REFRESH_RULES = "Would you like a reminder of the rules?"
WANTS_KEYWORDS = "Would you like to know a keyword and its function?"
READY_WORDS = (
    "Ready?", "OK...", "Next...", "Here we go!", "Try this...",
    "See how you get on with this one.", "Let's see how you get on.",
    "Are you ready for this?"
)
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
unused_correct_responses = list(CORRECT_RESPONSES)
unused_ready_words = list(READY_WORDS)
DIFFICULTY_LEVELS = ("easy", "medium", "hard")
# check google sheet value

matrix_block()
print("Configuring program...")
sleep(.5)
print("Initializing Active:Personnel:Inquisitor...")
easy_token, medium_token, hard_token = initial_token_setup()
sleep(.5)
print("Engaging Automated:Neuro:Solution:Work:Experimentation:Resources...")
sleep(.5)
print("Configuration complete...")

question_number = 1

matrix_block()

main()
