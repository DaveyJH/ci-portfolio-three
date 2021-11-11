"""Run a quiz game via a CLI"""
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import requests


def check_api_url(difficulty: str):
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

    return True


print("Easy:", check_api_url("easy"))
print("Medium:", check_api_url("medium"))
print("Hard:", check_api_url("hard"))
print("Error:", check_api_url("error_string"))
