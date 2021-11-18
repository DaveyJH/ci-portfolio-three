"""Run a quiz game via a CLI"""
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# ! line breaks before any print statement that follows an input


# from operator import indexOf
# from random import randrange, shuffle
# from html import unescape
from time import sleep

# import requests
import tokens
from better_profanity import profanity
from getch import pause
from matrix import matrix_block, matrix_line
from sheets import SCORES_SHEET
from user_name import user as user_string
from keywords import AvailableKeywords, which_keyword, keyword_description, all_keywords
from validate_yn import validate_yes_no


def introduction_to_quiz():
    """Print initial welcome strings and allow user to input username.

    ---
    Returns:
        str: Validated username.
    """
    print(f"\n{80*'='}")
    print("\nWelcome!\nAre you clued up enough on code and computers?")
    print("Think you have the knowledge to go all the way?")
    print("Let's see how you do! First, introduce yourself.\n")

    new_user = user_string()
    print(f"\nWelcome, {new_user}!")

    return new_user


def validate_yes_no(input_string: str = "Please input 'y' or 'n':"):
    """User selects whether to print info or not.

    ---
    Args:
        input_string (str): (default = "Please input 'y' or 'n':") The string
        to be printed as the input. Should clearly identify what information
        will be printed.

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
        user_response = input(f"{input_string} {YN}\n").lower()
        continue

    if user_response == "n":
        return False

    return True


# def check_api_retrieve_question(
#     difficulty: str, token: str
# ) -> tuple:
#     """Retrieve a response from opentdb API.

#     Connects to opentdb.com/api to ensure correct query parameters have been
#     used in the URL, allowing for valid data.

#     Args:
#         difficulty: The current difficulty level set by the question number

#     Returns:
#         tuple: (bool, dict[str, str], str)
#             bool: True if response from API is 0, else false.
#             dict[str, str]: The response in JSON format.
#             *str: New token string if token has expired.
#     """
#     api_url = (
#         "https://opentdb.com/api.php?amount=1&category"
#         f"=18&difficulty={difficulty}&type=multiple&token={token}"
#     )

#     print("\nRetrieving data...")
#     response = requests.get(api_url)
#     data = response.json()

#     if data["response_code"] in (3, 4):
#         print("Token expired:")
#         new_token = retrieve_api_token(difficulty)
#         data = check_api_retrieve_question(difficulty, new_token)[1]
#         return True, data, new_token

#     try:
#         if data["response_code"] in (1, 2):
#             raise ConnectionError(
#                 f"Open Trivia Database API connection error: {api_url}\n"
#                 f"Response_code from API: {data['response_code']}"
#             )
#     except ConnectionError as e:
#         print(f"Error: {e}")
#         print("Program will now terminate!")
#         exit()

#     print("Data retrieval successful...")
#     return True, data


# def set_answer_letters(question: dict):
#     """Give each answer a letter and determines the correct answer.

#     Args:
#         question: The current question.


#     Returns:
#         tuple: (dict, str)
#             dict[str, str]: Shuffled answers paired with a choice letter.
#             str: The correct answer.
#     """
#     correct_answer = unescape(question["correct_answer"])
#     incorrect_answers = list(question["incorrect_answers"])
#     answers = [correct_answer, *incorrect_answers]
#     shuffle(answers)

#     abcd = {
#         "a": unescape(answers[0]),
#         "b": unescape(answers[1]),
#         "c": unescape(answers[2]),
#         "d": unescape(answers[3]),
#     }

#     return abcd, correct_answer


# def display_question(
#     question: str, abcd: dict,
#     current_pre_question: str, first_attempt: bool = False
# ):
#     """Prints question and possible answers

#     Prints a single matrix_line for visual clarity.

#     Prints a pre_question string, the question and the possible answers. If
#     it is the first time the question has been printed, a random string will
#     be prepended to the Question Number x.

#     Questions longer than 80 characters are split over individual lines and
#     spaces are trimmed to prevent single space indent on new line.

#     Args:
#         question: The current question.
#         abcd: A dict of the available answers with a selection letter.
#         pre_question: A string to be prepended to the question number.
#         first_attempt: Determines if the prepending string needs defining
#             (default: False)

#     Returns:
#         str: Generated prepend to question number. Default returned if not
#             first_attempt (default: "")
#     """

#     global unused_ready_words

#     matrix_line()
#     pre_question_str = ""
#     if first_attempt:
#         if not unused_ready_words:
#             unused_ready_words = list(READY_WORDS)
#         pre_question_str = unused_ready_words[
#             randrange(len(unused_ready_words))]
#         unused_ready_words.remove(pre_question_str)
#     if pre_question_str:
#         print(f"\n{pre_question_str} Question Number {str(question_number)}")
#     else:
#         print(
#             f"\n{current_pre_question} Question Number {str(question_number)}"
#         )
#     print(f"Followed by the {len(abcd)} possible answers...\n")

#     question_str = unescape(question["question"])
#     question_lines = []

#     if len(question_str) <= 80:
#         question_lines.append(question_str)
#     else:
#         while len(question_str) > 80:
#             question_str = question_str.strip()
#             q_line = question_str[:80]
#             if question_str[80] == " ":
#                 question_lines.append(q_line)
#                 question_str = question_str[80:]
#             elif " " in q_line:
#                 last_space = q_line.rindex(" ")
#                 q_line = question_str[:last_space]
#                 question_str = question_str[last_space:].strip()
#                 question_lines.append(q_line)
#             else:
#                 question_lines.append(q_line)
#         question_lines.append(question_str.strip())

#     for line in question_lines:
#         print(line)

#     print("")
#     for letter, answer_str in abcd.items():
#         print(f"{letter}: {answer_str}")

#     return pre_question_str


# def initiate_question(difficulty: str, token: str):
#     """Check and set up question.

#     Check for valid token and updates if necessary. Retrieves question string,
#     choices and answer. Sets string to be used before instance of question.

#     Args:
#         difficulty: A string value containing the current difficulty.
#         token: A string value of the current API token in use.

#     Returns:
#         str: A valid APi token.
#         str: A string to prepend the question.
#         dict[str, str]: The question data in a dictionary. Example...
#             {
#                 "category":"Example Questions",
#                 "type":"multiple",      # multiple or boolean
#                 "difficulty":"easy",
#                 "question":"What is 2 + 2",
#                 "correct_answer":"4",
#                 "incorrect_answers":[
#                     "5",
#                     "8",
#                     "0"
#                 ]
#             }
#         dict[str, str]: Letters with a shuffled set of answers assigned to them
#             to allow user selection. Example...
#                 {
#                     "a": "8",
#                     "b": "0",
#                     "c": "4",
#                     "d": "5"
#                 }
#         str: The answer to the question as a string. Example....
#             "4"
#     """

#     update_token = token
#     api_return = check_api_retrieve_question(difficulty, token)
#     if len(api_return) == 3:
#         # update google sheet
#         update_token = api_return[2]

#     question_data = api_return[1]["results"]
#     choices, answer = set_answer_letters(question_data[0])
#     pre_question_str = display_question(question_data[0], choices, "", True)

#     # ! DELETE BEFORE DEPLOYMENT TESTING ONLY
#     # print("")
#     # print(answer)

#     return update_token, pre_question_str, question_data, choices, answer


# def check_input(new_input: str, choices: dict, answer: str, user_name: str):
#     """Validates user's input after question is printed.

#     Checks for valid user input and checks if keyword has been used.

#     Args:
#         new_input: The user's input string.
#         choices: A dictionary of letters and their associated answer.
#         answer: The current question answer as a string.

#     Returns:
#         bool: True if answer is received, else False and continue user input.
#         dict[str, str]: Available answer choices.
#     """

#     try:
#         if not new_input:
#             raise ValueError("No input detected...")
#         # change to available keywords
#         if new_input in KEYWORDS and new_input in available_keywords:
#             choices = keyword_used(new_input, choices, answer, user_name)
#             return False, choices
#         if new_input not in choices:
#             raise ValueError(
#                 "Invalid input detected, please input an answer or available"
#                 " keyword."
#             )

#     except ValueError as e:
#         print(f"{e}\n")
#         pause()
#         return False, choices

#     return True, choices


# def run_question(question_num: int, user_name: str):
#     """Runs the question.

#     Sets difficulty level depending on question number. Prints question and
#     answers and available lifelines. Awaits user input that gets validated.

#     Args:
#         question_num: The current question number.

#     Returns:
#         str: A validated user input.
#         dict[str, str]: The answers with a key letter for user selection.
#         str: The question answer.
#     """

#     if question_num < 6:
#         current_difficulty = DIFFICULTY_LEVELS[0]
#         current_token = easy_token
#     elif question_num < 11:
#         current_difficulty = DIFFICULTY_LEVELS[1]
#         current_token = medium_token
#     else:
#         current_difficulty = DIFFICULTY_LEVELS[2]
#         current_token = hard_token

#     (
#         current_token,
#         pre_question,
#         question_data,
#         choices,
#         answer
#     ) = initiate_question(current_difficulty, current_token)

#     while True:
#         print(f"\nAvailable keywords:{available_keywords}")
#         print(f"Available choices:{list(choices.keys())}")
#         user_input = input(
#             "Please provide your answer or enter a keyword:\n"
#         ).lower()
#         input_check = check_input(user_input, choices, answer, user_name)
#         if not input_check[0]:
#             choices = input_check[1]
#             display_question(question_data[0], choices, pre_question)
#         else:
#             break

#     return user_input, choices, answer


# def check_answer(user_input: str, choices: dict, answer: str):
#     """Check user's answer against correct answer

#     If the user answer is correct, increment the question number and allow
#     the quiz to continue. Otherwise run through loss functions.

#     Args:
#         user_input: The user's chosen letter.
#         choices: Letters with their assigned answer.
#         answer: The answer string to the question.
#     """

#     global unused_correct_responses
#     global question_number

#     if choices[user_input] == answer:
#         if not unused_correct_responses:
#             unused_correct_responses = list(CORRECT_RESPONSES)
#         this_response = unused_correct_responses[
#             randrange(len(unused_correct_responses))]
#         unused_correct_responses.remove(this_response)
#         print(f"\n{this_response}\n")
#         question_number += 1
#         pause()
#     else:
#         # ! FOR TESTING ONLY
#         print(INCORRECT_RESPONSES[randrange(len(INCORRECT_RESPONSES))])
#         exit()


# def keyword_take():
#     """Ends the quiz and logs the score."""

#     print("\nDo you want to end here?")
#     confirm = input("Please input 'take' again to confirm exit:\n")

#     if confirm != "take":
#         print("Input did not match.\n")
#         return

#     # testing
#     print("TOOK THE MONEY")
#     # ??restart?
#     exit()


# def keyword_scores():
#     """Prints the current high scores from Google Sheet data."""

#     print("\nSo you would like to see the scores?")
#     confirm = input("Please input 'scores' again to confirm exit:\n")

#     if confirm != "scores":
#         print("Input did not match.\n")
#         return

#     print("\nQuerying database...\n")
#     sleep(.5)

#     highscore_values_cells = SCORES_SHEET.range("values")
#     highscore_users_cells = SCORES_SHEET.range("users")

#     highscore_values = [cell.value for cell in highscore_values_cells]
#     highscore_users = [cell.value for cell in highscore_users_cells]

#     highscores = dict(zip(highscore_users, highscore_values))

#     # scores ordered in spreadsheet. check with additional scores etc.
#     # sorted_scores = dict(
#     #     sorted(highscores.items(), key=lambda user: user[1], reverse=True)
#     # )

#     print("The current highscorers are...\n")

#     print(STAR_LINE)
#     for user in highscores:

#         if highscore_users.index(user) % 2 != 0:
#             star = unescape("&#9734")
#             star_end = unescape("&#9733")
#         else:
#             star = unescape("&#9733")
#             star_end = unescape("&#9734")
#         print(star, f"{user}: {highscores[user]}".center(75), star_end)
#         sleep(.1)
#     print(STAR_LINE[::-1].strip())

#     lowest_score = int(highscores[list(highscores.keys())[-1]])

#     if question_number > lowest_score:
#         print("\nYou are on track to make it on the list...")
#         print("...As long as you don't lose it all!\n".rjust(80))
#     else:
#         to_lowest_score = lowest_score - question_number
#         append_s = "s" if to_lowest_score > 1 else ""
#         print(
#             "\nYou aren't quite there yet. Answer at least "
#             f"{lowest_score - question_number} more question{append_s}..."
#         )


# def keyword_even(
#     current_choices: dict, correct_answer: str
# ) -> dict:
#     """Removes 2 incorrect answers from the choices.

#     Requires confirmation of input. If input string does not match, revert to
#     user input.

#     Args:
#         current_choices: A dictionary of the currently available letters and
#             answers.
#         correct_answer: The correct answer string.

#     Returns:
#         dict[str, str]: (If even confirmed) One correct answer, one incorrect
#         answer. Assigned letters remain the same and order is alphabetical.
#     """

#     print("\nWould you like to even the odds?")
#     confirm = input("Please input 'even' again to confirm choice:\n")
#     if confirm != "even":
#         print("Input did not match.\n")
#         return current_choices
#     available_keywords.remove("even")

#     new_choices = {}
#     for k, v in current_choices.items():
#         if v == correct_answer:
#             new_choices.update({k: v})
#             del current_choices[k]
#             break
#     incorrect_answer = list(
#         current_choices.items()
#     )[randrange(len(current_choices))]

#     new_choices.update({incorrect_answer[0]: incorrect_answer[1]})

#     new_items = new_choices.items()
#     sorted_items = sorted(new_items)
#     new_choices = dict(sorted_items)

#     print(FIFTY_LINE)
#     print("\nEvening the odds...\n")
#     sleep(.5)
#     print("Recalculating...\n")
#     sleep(.5)
#     print("Calculation successful!")
#     sleep(.5)
#     print(FIFTY_LINE)
#     print("")

#     return new_choices


# def keyword_review(
#     current_choices: dict, correct_answer: str
# ):
#     """Prints percentages next to avilable choices.

#     Calculates a percentage response for each available answer. Chance of
#     response being correct is lower for higher number questions. Prints
#     responses in similar style to available answers.

#     Args:
#         current_choices: A dictionary of the currently available letters and
#             answers.
#         correct_answer: The correct answer string.
#     """

#     print("\nWould you like to request a review?")
#     confirm = input("Please input 'review' again to confirm choice:\n")
#     if confirm != "review":
#         print("Input did not match.\n")
#         return
#     available_keywords.remove("review")

#     reviewed_answers = current_choices.copy()
#     reviews = {}

#     if question_number < 6:
#         percentage = randrange(50, 80)
#     elif question_number < 11:
#         percentage = randrange(20, 60)
#     else:
#         percentage = randrange(10, 40)

#     if len(current_choices) == 2:
#         r_a = 100 - percentage
#         incorrect_percentages = [r_a]
#     else:
#         remainder = 100 - percentage
#         r_a = randrange(round(remainder / 2))
#         remainder = remainder - r_a
#         r_b = randrange(remainder)
#         r_c = remainder - r_b
#         incorrect_percentages = [r_a, r_b, r_c]

#     for k, v in reviewed_answers.items():
#         if v == correct_answer:
#             reviews.update({k: f"{percentage}%"})
#             del reviewed_answers[k]
#             break

#     while reviewed_answers:
#         incorrect_answer = list(
#             reviewed_answers.items()
#         )[randrange(len(reviewed_answers))]
#         incorrect_answer_percentage = incorrect_percentages[
#             randrange(len(incorrect_percentages))
#         ]
#         reviews.update({
#             incorrect_answer[0]:
#             f"{incorrect_answer_percentage}%"
#         })

#         del reviewed_answers[incorrect_answer[0]]
#         incorrect_percentages.remove(incorrect_answer_percentage)

#     new_items = reviews.items()
#     sorted_items = sorted(new_items)
#     reviews = dict(sorted_items)

#     print(QUERY_LINE)
#     print("Requesting review...\n")
#     sleep(.5)
#     print("Collating responses...\n")
#     sleep(.5)
#     print("Rendering results...")
#     sleep(.5)
#     print(QUERY_LINE)

#     for letter, review in reviews.items():
#         print(f"{letter}: {review}")

#     print("")
#     pause()
#     print("")


# def keyword_call(current_choices: dict, correct_answer: str, user_name: str):
#     """Prints a string with a suggested answer.

#     Calculates a percentage response for each available answer. Chance of
#     response being correct is lower for higher number questions. Prints
#     responses in similar style to available answers.

#     Args:
#         current_choices: A dictionary of the currently available letters and
#             answers.
#         correct_answer: The correct answer string.
#     """

#     print("\nWould you like to call a coder?")
#     confirm = input("Please input 'call' again to confirm choice:\n")
#     if confirm != "call":
#         print("Input did not match.\n")
#         return
#     available_keywords.remove("call")

#     if question_number < 6:
#         percentage = randrange(50, 80)
#     elif question_number < 11:
#         percentage = randrange(20, 60)
#     else:
#         percentage = randrange(10, 40)

#     coder_guess = list(current_choices)[randrange(len(current_choices))]

#     for k, v in current_choices.items():
#         if v == correct_answer and percentage > 50:
#             coder_guess = k

#     if question_number < 6:
#         coder_responses = (
#             f"You came to the right coder, 100% it is '{coder_guess}'.",
#             f"'{coder_guess}', I am sure of it.",
#             f"I think I am right in saying '{coder_guess}'. I'm confident.",
#             f"Easy one for me, that's '{coder_guess}'."
#         )
#     if question_number < 11:
#         coder_responses = (
#             f"I'm pretty confident with this one, it's '{coder_guess}'",
#             f"It has to be '{coder_guess}', I am almost certain.",
#             f"I could be wrong, but I would say it is '{coder_guess}'",
#             f"That's a little tricky but '{coder_guess}' seems to be the one"
#         )
#     else:
#         coder_responses = (
#             f"I'm not sure on this, it could be '{coder_guess}'.",
#             f"That is tricky. I would say '{coder_guess}', but I am guessing",
#             f"It might be '{coder_guess}', but I really am not sure.",
#             f"Wow, that's tough. I'd say '{coder_guess}', but it's a stab in "
#             "the dark."
#         )

#     print(f"\n{unescape(TELEPHONE_LINE)}")
#     print("Calling a coder...\n")
#     sleep(.5)
#     print("Call connected...\n")
#     sleep(.5)
#     print("Providing possibilities...\n")
#     sleep(.5)

#     print(f"{unescape(TELEPHONE)} Hi, {user_name}...")
#     print(
#         f"{unescape(TELEPHONE)} "
#         f"{coder_responses[randrange(len(coder_responses))]}"
#     )
#     print(f"{unescape(TELEPHONE_LINE)}\n")
#     print(
#         f"So, the coder thinks it might be {coder_guess}, but can you trust "
#         "them?"
#     )

#     print("")
#     pause()
#     print("")


# def keyword_used(
#     word: str, current_choices: dict, correct_answer: str, user_name: str
# ):
#     """Run keyword function"""

#     new_choices = current_choices

#     if word == "help":
#         keyword_help()
#         print("\nLet's return to the quiz!")
#         pause()
#     if word == "take":
#         keyword_take()
#     if word == "scores":
#         keyword_scores()
#         print("\nLet's return to the quiz!")
#         pause()

#     if word == "even":
#         if "even" in available_keywords:
#             new_choices = keyword_even(current_choices, correct_answer)
#     if word == "review":
#         if "review" in available_keywords:
#             keyword_review(current_choices, correct_answer)
#     if word == "call":
#         if"call" in available_keywords:
#             keyword_call(current_choices, correct_answer, user_name)

#     return new_choices


# def main():
#     """Runs the quiz."""

#     user_name = introduction_to_quiz()

#     keyword_help(True)

#     print("\nGreat...let's begin!")

#     while question_number < 16:
#         user_input, choices, answer = run_question(question_number, user_name)
#         check_answer(user_input, choices, answer)


# DIFFICULTY_LEVELS = ("easy", "medium", "hard")

WANTS_RULES = "Before we begin, should we run through the rules?"
REFRESH_RULES = "Would you like a reminder of the rules?"
WANTS_KEYWORDS = "Would you like to know a keyword and its function?"
# READY_WORDS = (
#     "Ready?", "OK...", "Next...", "Here we go!", "Try this...",
#     "See how you get on with this one.", "Let's see how you get on.",
#     "Are you ready for this?"
# )
# CORRECT_RESPONSES = (
#     "Correct...", "Well done!", "That's right.",
#     "You clearly know your stuff.", "That was...error-free!", "Spot on.",
#     "Brilliant, that's correct.", "Nice work."
# )
# INCORRECT_RESPONSES = (
#     "Oh dear, that's wrong I'm afraid.", "Oh no! That wasn't correct.",
#     "Unfortunately, that answer was incorrect.", "Game over for you.",
#     "That does not compute...wrong answer!"
# )

# # Unicode character lines and extras
# FIFTY_LINE = f"|{unescape('&#8309&#8304&#8260&#8325&#8320|')*13}"
# QUERY_LINE = f"\n{unescape('&#0191?')*40}"
# STAR_LINE = f"{unescape('&#9734 &#9733 ')}"*20
# TELEPHONE_LINE = ("&#9743 &#9742 "*20)
# TELEPHONE = ("&#128222")

# unused_correct_responses = list(CORRECT_RESPONSES)
# unused_ready_words = list(READY_WORDS)

# todo create quiz instance with these inside
available_keywords = AvailableKeywords()
print(available_keywords.available_keywords)

# * functions to run once when program started
# * user's name will be unchangeable
# * introduction will not run

# def keyword_help(initial_run: bool = False):
#     """Runs through explanations of rules and keywords.

#     Args:
#         initial_run: If True, modifies input string before rules to
#             WANTS_RULES. (default: False)
#     """
#     rules = WANTS_RULES if initial_run else REFRESH_RULES
#     if validate_yes_no(rules):
#         print_rules()

#     while validate_yes_no(WANTS_KEYWORDS):
#         keyword = which_keyword()
#         keyword_description(keyword)
###############################################

# YN = ("y", "n")

# matrix_block()
# print("Configuring program...")
# sleep(.5)
# print("Initializing Active:Personnel:Inquisitor...")
# easy_token, medium_token, hard_token = (
#     token.string for token in tokens.initial_token_setup()
# )
# sleep(.5)
# print("Engaging Automated:Neuro:Solution:Work:Experimentation:Resources...")
# sleep(.5)
# print("Configuration complete...")
# matrix_block()

# # question_number = 1


# user = introduction_to_quiz()
# keyword_help(True)
