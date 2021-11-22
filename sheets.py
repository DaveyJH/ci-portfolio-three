"""Handles Google Sheet authorization"""

import gspread
from google.oauth2.service_account import Credentials
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


def update_win(user_name):
    """Insert winning user name and score at top of leaderboard"""

    print("Updating scores database...")

    current_highscore_values_cells = SCORES_SHEET.range("values")
    current_highscore_users_cells = SCORES_SHEET.range("users")

    new_values = [15] + [
        cell.value for cell in current_highscore_values_cells
    ][:-1]
    new_users = [user_name] + [
        cell.value for cell in current_highscore_users_cells
    ][:-1]

    for i in range(10):
        SCORES_SHEET.update_cell(i + 2, 1, new_users[i])
        SCORES_SHEET.update_cell(i + 2, 2, new_values[i])

    print(f"Scores updated...well done {user_name}, you are at the top!")


def update_scores(user_name, score):
    """Insert user name and score on leaderboard"""

    print("Checking scores database...\n")
    print("Please be patient...\n")

    score = score - 1

    current_highscore_values_cells = SCORES_SHEET.range("values")
    current_highscore_users_cells = SCORES_SHEET.range("users")

    values = [cell.value for cell in current_highscore_values_cells]
    users = [cell.value for cell in current_highscore_users_cells]

    if user_name in users:
        checked_users = list(users)
        repeats = users.count(user_name)
        while repeats > 0:
            index = checked_users.index(user_name)
            if int(values[index]) == score:
                print("A user name with that score is already present.")
                print("Scores list will not be updated.\n")
                return
            checked_users[index] = "-"
            repeats -= 1

    for i in range(10):
        if score < int(values[i]):
            insert = i + 1

    new_values = values[:insert] + [str(score)] + values[insert:-1]
    new_users = users[:insert] + [user_name] + users[insert:-1]

    for i in range(10):
        SCORES_SHEET.update_cell(i + 2, 1, new_users[i])
        SCORES_SHEET.update_cell(i + 2, 2, new_values[i])

    print("Scores updated successfully.")
    pause()
    if insert == 0:
        print(
            f"Well done {user_name}. There's only 1 person ahead of you!\n"
        )
    else:
        print(
            f"Well done {user_name}. There are only {insert} people ahead of "
            "you!\n"
        )
