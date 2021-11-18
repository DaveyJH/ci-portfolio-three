"""Run a quiz game via a CLI"""

# from operator import indexOf
# from random import randrange, shuffle
# from html import unescape
from time import sleep

# import requests
import tokens
# from better_profanity import profanity
# from getch import pause
from matrix import matrix_block, matrix_line
from sheets import SCORES_SHEET
from user_name import create_user
# from keywords import
# from validate_yn import validate_yes_no


def introduction_to_quiz():
    """Print initial welcome strings and allow user to input username

    ---
    Returns:
        str: Validated username
    """
    print(f"\n{80*'='}")
    print("\nWelcome!\nAre you clued up enough on code and computers?")
    print("Think you have the knowledge to go all the way?")
    print("Let's see how you do! First, introduce yourself.\n")

    new_user = create_user()
    print(f"\nWelcome, {new_user}!")

    return new_user

# * section to run once when program started
# * user's name will be unchangeable
# * introduction will not run on replay

matrix_block()
print("Configuring program...")
sleep(.5)
print("Initializing Active:Personnel:Inquisitor...")
easy_token, medium_token, hard_token = (
    token.string for token in tokens.initial_token_setup()
)
sleep(.5)
print("Engaging Automated:Neuro:Solution:Work:Experimentation:Resources...")
sleep(.5)
print("Configuration complete...")
matrix_block()

user = introduction_to_quiz({})
def keyword_help(initial_run: bool = False):
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
# todo add to quiz instance

# available_keywords = +