"""Run a quiz game via a CLI"""
# Write your code to expect a terminal of 80 characters wide and 24 rows high
from random import shuffle
from html import unescape

import requests


def check_api_url(difficulty: str) -> tuple[bool, object]:
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
        "https://opentdb.com/api.php?amount=5&category"
        f"=18&difficulty={difficulty}&type=multiple"
    )
    response = requests.get(api_url)
    data = response.json()

    try:
        if data['response_code'] != 0:
            raise ConnectionError(
                f"Open Trivia Database API URL incorrect: {api_url}\n"
                f"Response_code from API: {data['response_code']}"
            )
    except ConnectionError as e:
        print(f"Error: {e}")
        print("Program will now terminate!")
        exit()

    return True, data


api_check = check_api_url("easy")
api_validated = api_check[0]
question_data = api_check[1]["results"]

# print(api_validated)
# print(len(question_data))


def display_question(question, question_number):
    """Shows question and possible answers"""

    correct_answer = unescape(question["correct_answer"])
    incorrect_answers = list(unescape(question["incorrect_answers"]))
    answers = [correct_answer, *incorrect_answers]
    shuffle(answers)

    print(f"Ready? Question number {str(question_number)},")
    print("Followed by the four possible answers...")
    print(unescape(question["question"]))
    print(answers)


display_question(question_data[0], 1)

# for question in question_data:
#     print(unescape(question["question"]))

# for question in question_data:
#     print(unescape(question["correct_answer"]))

# for question in question_data:
#     for q in question["incorrect_answers"]:
#         print(unescape(q))
