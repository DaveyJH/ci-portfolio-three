"""Run a quiz game via a CLI"""

from time import sleep
from html import unescape
from keywords import Keywords

from tokens import initial_token_setup
from matrix import matrix_block
from user_name import User
from quiz import quiz
from validate_yn import validate_yes_no
from prints import yellow_print, cyan_print


def introduction_to_quiz():
    """Print initial welcome strings and allow user to input username

    ---
    Returns:
        object: A `User` instance
    """
    print(f"\n{80*'='}")
    print("\nWelcome!\nAre you clued up enough on code and computers?")
    print("Think you have the knowledge to go all the way?")
    print("Let's see how you do! First, introduce yourself.\n")

    new_user = User()
    print(f"\nWelcome, {new_user.user_name}!")

    return new_user


# * section to run once when program started
# * user's name will be unchangeable
# * introduction will not run on replay
# region initial setup
cyan_print("Computer Literate Investigator".center(80))
cyan_print(f"{'=' * len('Computer Literate Investigator')}".center(80))
matrix_block()
cyan_print("Configuring program...")
sleep(.5)
yellow_print("Initializing Active:Personnel:Inquisitor...")
easy_token, medium_token, hard_token = (initial_token_setup())
current_tokens = (easy_token, medium_token, hard_token)
sleep(.5)
yellow_print(
    "Engaging Automated:Neuro:Solution:Work:Experimentation:"
    "Resources..."
)
sleep(.5)
cyan_print("Configuration complete...")
matrix_block()

user = introduction_to_quiz()
Keywords.help_info(True)
# endregion

quiz(user.user_name, current_tokens)

while validate_yes_no("Play again?"):
    quiz(user.user_name, current_tokens, False)

print("")
matrix_block(6)
print("\n" * 2)
print(f"{'=' * 15}   Thanks for playing!   {'=' * 15}".center(80))
print(f"|{' ' * 10}Questions generated by opentdb.com{' ' * 9}|".center(80))
print(unescape(f"{'=' * 20}   &#169 DaveyJH   {'=' * 20}").center(80))
print("\n" * 2)
matrix_block(6)
