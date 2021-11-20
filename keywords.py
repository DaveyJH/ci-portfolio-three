"""Handles keywords"""

from html import unescape
from random import randrange
from time import sleep
from getch import pause
from validate_yn import validate_yes_no
from rules import print_rules
from sheets import SCORES_SHEET

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


def print_description(word: str):
    """Prints a description of a keyword

    ---
    Args:
        keyword: The keyword chosen by the user
    """

    def print_title():
        """Prints the keyword title and an underline of equal length"""

        print("\n" + f"{word.upper()}".center(40))
        line = "=" * len(word)
        print(f"{line.center(40)}\n")

    def print_content(description):
        """Prints the content explaining the keyword

        ---
        Args:
            description (str): The keyword description to be printed
        """

        print(f"{description}")

    print_title()
    for description_line in KEYWORDS[word]:
        print_content(description_line)
    print("")
    pause()


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

    def even(self, current_choices: dict, correct_answer: str) -> dict:
        """Removes 2 incorrect answers from the choices

        Requires confirmation of input. If input string does not match,
        revert to user input

        ---
        Args:
            current_choices (dict): A dictionary of the currently available
                letters and answers
            correct_answer (str): The correct answer string

        Returns:
            dict[str, str]: (If even confirmed) One correct answer, one
                incorrect answer. Assigned letters remain the same and order
                are sorted alphabetically
        """

        print("\nWould you like to even the odds?")
        if not self.confirm("even"):
            return current_choices
        self.available_keywords.remove("even")

        new_choices = {}
        for k, v in current_choices.items():
            if v == correct_answer:
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

        pause()
        print("")

        return new_choices

    def review(
        self, current_choices: dict, correct_answer: str, question_number: int
    ):
        """Prints percentages next to avilable choices

        Calculates a percentage response for each available answer. Chance of
        response being correct is lower for higher number questions. Prints
        responses in similar style to available answers

        ---
        Args:
            current_choices (dict): A dictionary of the currently available
                letters and answers
            correct_answer (str): The correct answer string
            question_number (int): The current question number
        """

        print("\nWould you like to request a review?")
        if not self.confirm("review"):
            return
        self.available_keywords.remove("review")

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
                incorrect_answer[0]: f"{incorrect_answer_percentage}%"
            })

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
        pause()
        print("")

        # todo #2 return choices with appended %s

    def call(
        self, current_choices: dict, correct_answer: str, user_name: str,
        question_number: int
    ):
        """Prints a string with a suggested answer

        Calculates a chance for the correct answer. Prints a string with
        inserted response from 'coder companion'

        ---
        Args:
            current_choices (dict): A dictionary of the currently available
                letters and answers
            correct_answer (str): The correct answer string
            user_name (str): The current user name
            question_number (int): The current question number
        """

        print("\nWould you like to call a coder?")
        if not self.confirm("call"):
            return
        self.available_keywords.remove("call")

        if question_number < 6:
            chance = 100
        elif question_number < 11:
            chance = randrange(20, 65)
        else:
            chance = 1

        coder_guess = list(current_choices)[randrange(len(current_choices))]

        if chance > 50:
            for k, v in current_choices.items():
                if v == correct_answer:
                    coder_guess = k

        if question_number < 6:
            coder_responses = (
                f"You came to the right coder, 100% it is '{coder_guess}'.",
                f"'{coder_guess}', I am sure of it.",
                f"I think I am right in saying '{coder_guess}'. "
                "I'm confident.",
                f"Easy one for me, that's '{coder_guess}'."
            )
        if 6 <= question_number < 11:
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
            f"So, the coder thinks it might be '{coder_guess}'', but can you "
            "trust them?\n"
        )

        pause()
        print("")

        # todo #2 return choices with appended TELEPHONE_RED

    def used(
        self, word: str, current_choices: dict, correct_answer: str,
        user_name: str, question_number
    ):
        """Processes keyword inputs with relevant function

        ---
        Args:
            word (str): The word to process
            current_choices (dict): A dictionary of the currently available
                letters and answers
            correct_answer (str): The correct answer_string
            user_name (str): The current user name
            question_number (int): The current question number        
        """

        new_choices = current_choices

        if word == "help":
            self.help_info()
            print("\nLet's return to the quiz!")
            pause()
        if word == "take":
            self.take()
        if word == "scores":
            self.scores(question_number)
            print("\nLet's return to the quiz!")
            pause()

        if word == "even":
            new_choices = self.even(current_choices, correct_answer)
        if word == "review":
            self.review(current_choices, correct_answer, question_number)
        if word == "call":
            self.call(
                current_choices, correct_answer, user_name, question_number
            )

        return new_choices

    @staticmethod
    def confirm(word):
        """Confirm use of keyword with repeated string input

        ---
        Args:
            word (str): Keyword to be used"""

        confirm = input(f"Please input '{word}' again to confirm:\n")

        if confirm != word:
            print("Input did not match: Keyword not used.\n")
            return False

        return True

    @staticmethod
    def help_info(initial_run: bool = False):
        """Runs through explanations of rules and keywords

        Args:
            initial_run: If True, modifies strings accordingly (default: False)
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
        """Ends the quiz and logs the score"""

        print("\nDo you want to end here?")
        if Keywords.confirm("take"):

            # testing
            # todo #1 create end function and add question number to params
            print("TOOK THE MONEY")
            # ??restart?
            exit()

    @staticmethod
    def scores(question_number: int):
        """Prints the current high scores from Google Sheet data

        Prints message to user to inform them of progress toward scorboard

        ---
        Args: question_number (int): The current question number"""

        answer_questions = question_number - 1

        print("\nSo you would like to see the scores?")

        if not Keywords.confirm("scores"):
            return

        print("\nQuerying database...\n")
        sleep(.5)

        highscore_values_cells = SCORES_SHEET.range("values")
        highscore_users_cells = SCORES_SHEET.range("users")

        highscore_values = [cell.value for cell in highscore_values_cells]
        highscore_users = [cell.value for cell in highscore_users_cells]

        highscores = dict(zip(highscore_users, highscore_values))

        print("The current highscorers are...\n")

        print(STAR_LINE)
        for user in highscores:

            if highscore_users.index(user) % 2 != 0:
                star = unescape("&#9734")
                star_end = unescape("&#9733")
            else:
                star = unescape("&#9733")
                star_end = unescape("&#9734")
            print(star, f"{user}: {highscores[user]}".center(75), star_end)
            sleep(.1)
        print(STAR_LINE[::-1].strip())

        lowest_score = int(highscores[list(highscores.keys())[-1]])

        if answer_questions > lowest_score:
            print("\nYou are on track to make it on the list...")
            print("...As long as you don't lose it all!\n".rjust(80))
        else:
            to_lowest_score = lowest_score - answer_questions
            append_s = "s" if to_lowest_score > 1 else ""
            print(
                "\nYou aren't quite there yet. Answer at least "
                f"{lowest_score - answer_questions} more question{append_s}..."
            )
