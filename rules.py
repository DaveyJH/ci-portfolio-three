"""Print rules of the quiz"""

from getch import pause
from prints import cyan_print


def print_rules():
    """Prints the rules"""

    cyan_print("\n" + "THE RULES".center(40))
    cyan_print("=========".center(40))

    print("\nThis quiz consists of 15 questions. The further you go, the")
    print("harder they become. Unless, of course, you know the answers!")
    print("There is no time limit for the questions, but you do have")
    print("just one life. One wrong answer and the game is over.\n")
    print("If you answer 5 or 10 questions correctly, your progress is safe.")
    print("An incorrect answer any time after a safety point will mean your")
    print("score is equal to the most recent safety point reached.\n")

    pause("\033[36;1mPress any key to continue...\033[0m")

    print("\nEach question has four possible answers: A, B, C and D.")
    print("You will be shown the question, followed by the four possible")
    print("answers, each preceded by a letter. Input your answer by use of")
    print("the (hopefully correct!) letter with no additional text. You will")
    print("be asked to confirm your answer. If you answer correctly, you move")
    print("on to the next question. Successfully answer all 15 questions to")
    print("win the ultimate gloating rights!\n")

    pause("\033[36;1mPress any key to continue...\033[0m")

    print("\nThere are some keywords that can be used at any time.")
    print("'Help', 'Take', 'Scores', 'Review', 'Even' and 'Call'.")
    print("Once the quiz begins, these can be explained at any time via the")
    print("'Help' keyword. You will have an opportunity to run through their")
    print("uses in a moment.\n")

    print("Finally, and possibly most importantly...remember to have fun!\n")

    pause("\033[36;1mPress any key to continue...\033[0m")
