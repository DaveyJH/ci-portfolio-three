"""Handles keywords"""

from html import unescape
from random import randrange
from time import sleep
import colorama
from getch import pause
from validate_yn import validate_yes_no
from rules import print_rules
from sheets import SCORES_SHEET
from max_line_length import limit_answers as shorten_a
from prints import magenta_print, print_tux, red_print, yellow_print

colorama.init()

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
        "user names that achieved them. You will be asked to confirm your",
        "decision. You will be prompted to press a key, and will subsequently",
        "return to the quiz."
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
WANTS_RULES = "Before we begin, should we run through the rules?"
REFRESH_RULES = "Would you like a reminder of the rules?"
WANTS_KEYWORDS = "Would you like to know a keyword and its function?"
REFRESH_KEYWORDS = "Would you like a reminder of a keyword and its function?"

# Unicode character lines and extras
FIFTY_LINE = f"|{unescape('&#8309&#8304&#8260&#8325&#8320|')*13}"
QUERY_LINE = f"{unescape('&#0191?')*40}"
DOTS = unescape("&#8285")
STAR_LINE = f"{unescape('&#9734 &#9733 ')}"*20
STAR_EMPTY = unescape("&#9734")
STAR_SOLID = unescape("&#9733")
TELEPHONE_LINE = unescape("&#9743 &#9742 "*20)
TELEPHONE_RED = unescape("&#128222")


def which_keyword():
    """Allows user to specify which keyword meaning to check

    ---
    Returns:
        str: Keyword input by user
    """

    print("\nWhich keyword would you like to check out?")
    user_input = input(f"{', '.join(KEYWORDS).title()}:\n").lower().strip()
    while (
        not user_input.isalpha()
        or user_input not in KEYWORDS
    ):
        red_print("\nInvalid input received")
        print(f"Please input: \033[36;1m{', '.join(KEYWORDS).title()}\033[0m")
        user_input = input(
            "Which keyword would you like to check?\n").lower().strip()
        continue

    return user_input


def print_description(word: str):
    """Prints a description of a keyword

    ---
    Args:
        keyword: The keyword chosen by the user
    """

    def print_title():
        """Prints the keyword title and an underline of equal length"""

        print("\n" + f"\033[36;1m{word.upper().center(40)}\033[0m")
        line = "=" * len(word)
        print(f"\033[36;1m{line.center(40)}\033[0m\n")

    print_title()
    for description_line in KEYWORDS[word]:
        print(description_line)
    print("")
    pause("\033[36;1mPress any key to continue...\033[0m")


class Keywords():
    """Available keywords and their functions

    ---
    Attributes:
        available_keywords (list): A list of the available keywords, initially
            generated from the`KEYWORDS` constant. Updated if a one shot
            keyword is used
    """

    def __init__(self) -> None:
        self.available_keywords = list(KEYWORDS.keys())

    def even(
        self, current_choices: dict, correct_answer: str,
    ):
        """Removes 2 incorrect answers from the choices

        Requires confirmation of input. If input string does not match,
        revert to user input

        ---
        Args:
            current_choices (dict): A dictionary of the currently available
                letters and answers
            correct_answer (str): The correct answer letter

        Returns:
            tuple(dict, bool, bool):
                dict[str, str]: (If even confirmed) One correct answer, one
                    incorrect answer. Assigned letters remain the same an
                    order are sorted alphabetically. Else, current_choices
                bool = False: Denotes that this keyword is not `review`
                bool = False: Denotes the quiz has not ended
        """

        print("\nWould you like to even the odds?")
        if not self.confirm("even"):
            return current_choices, False, False
        self.available_keywords.remove("even")

        new_choices = {}
        for k, v in current_choices.items():
            if k == correct_answer:
                new_choices.update({k: v})
                del current_choices[k]
                break

        incorrect_answer = list(
            current_choices.items())[randrange(len(current_choices))]
        new_choices.update({incorrect_answer[0]: incorrect_answer[1]})

        new_items = new_choices.items()
        sorted_items = sorted(new_items)
        new_choices = dict(sorted_items)

        print(f"\n{FIFTY_LINE}")
        print("Evening the odds...\n")
        sleep(.5)
        print("Recalculating...\n")
        sleep(.5)
        print("Calculation successful!")
        sleep(.5)
        print(f"{FIFTY_LINE}\n")

        pause("\033[36;1mPress any key to continue...\033[0m")
        print("")

        return new_choices, False, False

    def review(
        self, current_choices: dict, correct_answer: str, question_number: int,
        longest_answer_length: int
    ):
        """Prints percentages next to avilable choices

        Calculates a percentage response for each available answer. Chance of
        response being correct is lower for higher number questions. Prints
        responses in similar style to available answers

        ---
        Args:
            current_choices (dict): A dictionary of the currently available
                letters and answers
            correct_answer (str): The correct answer letter
            question_number (int): The current question number
            longest_answer_length (int): String length of longest answer

        Returns:
            tuple(dict, bool, bool):
                dict[str, str]: (If review confirmed) Answer choices
                bool: True if confirmed. Denotes that this keyword is `review`
                bool = False: Denotes the quiz has not ended
        """

        print("\nWould you like to request a review?")
        if not self.confirm("review"):
            return current_choices, False, False
        self.available_keywords.remove("review")

        reviewed_answers = dict(current_choices)
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
            r_a = randrange(remainder // 2)
            remainder = remainder - r_a
            r_b = randrange(remainder)
            r_c = remainder - r_b
            incorrect_percentages = [r_a, r_b, r_c]

        # ? no need for k,v .items()
        for k, v in reviewed_answers.items():
            if k == correct_answer:
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
            reviews.update(
                {incorrect_answer[0]: f"{incorrect_answer_percentage}%"}
            )
            # ? reviewed_answers.remove(incorrect_answer[0])
            del reviewed_answers[incorrect_answer[0]]
            incorrect_percentages.remove(incorrect_answer_percentage)

        new_items = reviews.items()
        sorted_items = sorted(new_items)
        reviews = dict(sorted_items)

        print(f"\n{QUERY_LINE}")
        print("Requesting review...\n")
        sleep(.5)
        print("Collating responses...\n")
        sleep(.5)
        print("Rendering results...")
        sleep(.5)
        print(f"{QUERY_LINE}\n")

        for letter, review in reviews.items():
            print(f"{letter}: {review}")

        print("")
        pause("\033[36;1mPress any key to continue...\033[0m")
        print("")

        new_choices = {}
        long = longest_answer_length
        for k, v in current_choices.items():
            phone = False
            if TELEPHONE_RED in v:
                v = v[:-1].strip()
                phone = True
            space = ((long - len(v)) * " ")
            new_choice = {k: f"{v}{space}  {DOTS}{reviews[k]}"}
            if phone:
                new_choice.update(
                    {k: f"{v}{space}  {DOTS}{reviews[k]}  {TELEPHONE_RED}"}
                )
            new_choices.update(new_choice)

        for k in new_choices:
            formatted_answer = shorten_a(new_choices[k])
            new_choices.update({k: formatted_answer})

        return new_choices, True, False

    def call(
        self, current_choices: dict, correct_answer: str, user_name: str,
        question_number: int, review_used: bool, longest_answer_length: int
    ):
        """Prints a string with a suggested answer

        Calculates a chance for the correct answer. Prints a string with
        inserted response from 'coder companion'

        ---
        Args:
            current_choices (dict): A dictionary of the currently available
                letters and answers
            correct_answer (str): The correct answer letter
            user_name (str): The current user name
            question_number (int): The current question number
            review_used (bool): True if review keyword has been used
            longest_answer_length (int): String length of longest answer

        Returns:
            tuple(dict, bool, bool):
                dict[str, str]: (If call confirmed) Answer choices
                bool = False: Denotes that this keyword is not `review`
                bool = False: Denotes the quiz has not ended
        """

        print("\nWould you like to call a coder?")
        if not self.confirm("call"):
            return current_choices, False, False
        self.available_keywords.remove("call")

        if question_number < 6:
            chance = 100
        elif question_number < 11:
            chance = randrange(20, 75)
        else:
            chance = 1

        coder_guess = list(current_choices)[randrange(len(current_choices))]

        if chance > 50:
            for k in current_choices:
                if k == correct_answer:
                    coder_guess = k

        if question_number < 6:
            coder_responses = (
                f"You came to the right coder, 100% it is '{coder_guess}'.",
                f"It's '{coder_guess}', I am sure of it.",
                f"I think I am right in saying '{coder_guess}'. "
                "I'm confident.",
                f"Easy one for me, that's '{coder_guess}'."
            )
        elif 6 <= question_number < 11:
            coder_responses = (
                f"I'm pretty confident with this one, it's '{coder_guess}'.",
                f"It has to be '{coder_guess}', I am almost certain.",
                f"I could be wrong, but I would say it is '{coder_guess}'.",
                f"That's a little tricky but '{coder_guess}' seems to be the "
                "one."
            )
        else:
            coder_responses = (
                f"I'm not sure on this, it could be '{coder_guess}'.",
                f"That is tricky. I would say '{coder_guess}', but I am "
                "guessing.",
                f"It might be '{coder_guess}', but I really am not sure.",
                f"Wow, that's tough. I'd say '{coder_guess}', but it's a stab "
                "in the dark."
            )

        print(f"\n{TELEPHONE_LINE}")
        print("Calling a coder...\n")
        sleep(.5)
        print("Call connected...\n")
        sleep(.5)
        print("Providing possibilities...\n")
        sleep(.5)

        print(f"{TELEPHONE_RED} Hi, {user_name}...")
        print(
            f"{TELEPHONE_RED} "
            f"{coder_responses[randrange(len(coder_responses))]}"
        )
        print(f"{TELEPHONE_LINE}\n")
        print(
            "So, the coder thinks it might be "
            f"\033[36;1m'{coder_guess}'\033[0m"
            ", but can you trust them?\n"
        )

        pause("\033[36;1mPress any key to continue...\033[0m")
        print("")

        long = longest_answer_length
        if review_used:
            current_choices[coder_guess] = (
                f"{current_choices[coder_guess]}  {TELEPHONE_RED}"
            )
        else:
            space = ((long - len(current_choices[coder_guess])) * " ")
            current_choices[coder_guess] = (
                f"{current_choices[coder_guess]}{space}  {TELEPHONE_RED}"
            )

        for k in current_choices:
            formatted_answer = shorten_a(current_choices[k])
            current_choices.update({k: formatted_answer})

        return current_choices, False, False

    def used(
        self, word: str, current_choices: dict, correct_answer: str,
        user_name: str, question_number: int, review_used: bool,
        longest_answer_length: int, safety: int
    ):
        """Processes keyword inputs with relevant function

        ---
        Args:
            word (str): The word to process
            current_choices (dict): A dictionary of the currently available
                letters and answers
            correct_answer (str): The correct answer letter
            user_name (str): The current user name
            question_number (int): The current question number
            review_used (bool): True if review keyword has been used
            longest_answer_length (int): String length of longest answer
            safety (int): 0, 1 or 2. If 1, minimum score is 5. If 2, minimum
                score is 10

        Returns:
            tuple (dict, bool, bool):
                dict: New answer choices
                bool: True if `review` keyword used
                bool: True if `take` keyword used
        """

        keyword_response = current_choices, False, False

        if word == "help":
            self.help_info()
            print("\nLet's return to the quiz!")
            pause("\033[36;1mPress any key to continue...\033[0m")
        if word == "take":
            if self.take():
                keyword_response = current_choices, False, True
        if word == "scores":
            self.scores(question_number, safety)
            print("\nLet's return to the quiz!")
            pause("\033[36;1mPress any key to continue...\033[0m")

        if word == "even":
            keyword_response = self.even(
                current_choices, correct_answer,
            )
        if word == "review":
            keyword_response = self.review(
                current_choices, correct_answer, question_number,
                longest_answer_length
            )
        if word == "call":
            keyword_response = self.call(
                current_choices, correct_answer, user_name, question_number,
                review_used, longest_answer_length
            )
        if word == "tux":
            magenta_print(
                "You found the super secret! Enjoy! (⌐■_■)"
            )
            pause("\033[36;1mPress any key to continue...\033[0m")
            print_tux()
            pause("\033[36;1mPress any key to continue...\033[0m")

        return keyword_response

    @staticmethod
    def confirm(word):
        """Confirm use of keyword with repeated string input

        ---
        Args:
            word (str): Keyword to be used

        Returns:
            bool: True if input duplicated as confirmation, else False
        """

        print(
            f"Please input '\033[36;1m{word}\033[0m' again to "
            "confirm:\n", end="")
        confirm = input().lower().strip()

        if confirm != word:
            if word in KEYWORDS:
                red_print("Input did not match: Keyword not used.\n")
            else:
                red_print("Input did not match: Please try again.\n")
            return False

        return True

    @staticmethod
    def help_info(initial_run: bool = False):
        """Runs through explanations of rules and keywords

        Args:
            initial_run: (default: False) If True, modifies strings accordingly
        """
        wants_rules = WANTS_RULES if initial_run else REFRESH_RULES
        if validate_yes_no(wants_rules):
            print_rules()

        wants_keywords = WANTS_KEYWORDS if initial_run else REFRESH_KEYWORDS
        while validate_yes_no(wants_keywords):
            keyword = which_keyword()
            print_description(keyword)

    @staticmethod
    def take():
        """Ends the quiz and logs the score

        ---
        Returns:
            bool: True if confirmed
        """

        print("\nDo you want to end here?")
        if Keywords.confirm("take"):
            print("\nSo you've decided to end it there.")
            print("That's OK. Please wait a moment...\n")
            return True

        return False

    @staticmethod
    def scores(question_number: int, safety: int):
        """Prints the current high scores from Google Sheet data

        Prints message to user to inform them of progress toward scorboard.
        Prints error message if invalid data retrieved from Sheet

        ---
        Args:
            question_number (int): The current question number
            safety(int): Current safety value. 1 means 5 reached, 2 means 10
                reached
        """

        answer_questions = question_number - 1

        print("\nSo you would like to see the scores?")

        if not Keywords.confirm("scores"):
            return

        yellow_print("\nQuerying database...\n")
        sleep(.5)

        highscore_values_cells = SCORES_SHEET.range("values")
        highscore_users_cells = SCORES_SHEET.range("users")

        highscore_values = [cell.value for cell in highscore_values_cells]
        highscore_users = [cell.value for cell in highscore_users_cells]

        try:
            for i in highscore_values:
                if not i.isnumeric():
                    raise ValueError("Scores database is corrupted - Values.")
            for i in highscore_users:
                if not "".join(i.split()).isalnum():
                    raise ValueError("Scores database is corrupted - Users")
        except ValueError as e:
            red_print(f"Critical error: {e}")
            red_print("Scores could not be displayed")
            return

        print("The current highscorers are...\n")

        print(STAR_LINE)
        for index, user in enumerate(highscore_users):

            if index % 2 != 0:
                star = unescape("&#9734")
                star_end = unescape("&#9733")
            else:
                star = unescape("&#9733")
                star_end = unescape("&#9734")
            print(
                star, f"{user}: {highscore_values[index]}".center(75), star_end
            )
            sleep(.1)
        print(STAR_LINE[::-1].strip())

        lowest_score = int(highscore_values[len(highscore_values) - 1])

        if answer_questions > lowest_score:
            if (
                safety == 1 and lowest_score < 6
                or safety == 2 and lowest_score < 11
            ):
                print("\nYou have made it on to the score board...")
                print("...Try to see how far you can go!\n".rjust(80))
            else:
                print("\nYou are on track to make it on the list...")
                print("...As long as you don't lose it all!\n".rjust(80))

        else:
            to_lowest_score = lowest_score - answer_questions
            append_s = "s" if to_lowest_score > 1 else ""
            print(
                "\nYou aren't quite there yet. Answer at least "
                f"{lowest_score - answer_questions} more question{append_s}..."
            )

        return
