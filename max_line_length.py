"""Handles line length of text"""

from html import unescape
from prints import cyan_print

# duplicated to prevent circular import
DOTS = unescape("&#8285")
TELEPHONE_RED = unescape("&#128222")


def limit_line_length(string: str, cyan=False):
    """Prints individual lines with a max line length of 80 characters

    Checks for and prevents prepending spaces/split words

    ---
    Args:
        string (str): String to be altered to fit within 80 character lines
        color (bool): True if string is to be printed with cyan coloring
    """

    lines = []
    if len(string) <= 80:
        lines.append(string)
    else:
        while len(string) > 80:
            string = string.strip()
            single_line = string[:80]
            if string[80] == " ":
                lines.append(single_line.strip())
                string = string[80:]
            elif " " in single_line:
                last_space = single_line.rindex(" ")
                single_line = string[:last_space]
                string = string[last_space:].strip()
                lines.append(single_line)
            else:
                lines.append(single_line)
        # add last line
        lines.append(string.strip())

    for line in lines:
        if cyan:
            cyan_print(line)
        else:
            print(line)


def limit_answers(string: str):
    """Separates long answers to individual lines of max 60 characters

    Accounts for prepended choice letter and space by adding 3 spaces to
    lines after first line. Appends life lines to end of first line.

    ---
    Returns:
        Formatted answer string
    """

    def _check_phone_review(single_line, phone, review_used):
        """Check need to append phone symbol and review

        ---
        Args:
            single_line (str): The first line string
            phone (bool): True if phone symbol was present in original choice
            review_used (bool): True if review was present in original choice
        """
        if review_used:
            single_line = single_line + review
            review_used = False
        if phone:
            single_line = single_line + f"  {TELEPHONE_RED}"
            phone = False
        return single_line

    def _check_first_line(choice, single_line, first):
        """Check if single_line is the first line

        ---
        Args:
            choice (str): The current formatted choice
            single_line (str): The current line string
            first (bool): True if this is the first line of `choice`
        Return:
            A formatted `choice` string with prepending spaces and line breaks
            if required
        """

        if first:
            choice = choice + single_line
        else:
            choice = choice + f"\n   {single_line}"
        return choice

    phone = False
    review_used = False
    first = True

    if TELEPHONE_RED in string:
        string = string.replace(f"  {TELEPHONE_RED}", "")
        phone = True

    if DOTS in string:
        dot_index = string.index(DOTS)
        per_index = string[dot_index:dot_index + 4].index("%") + dot_index
        review = string[dot_index - 2:per_index + 1]
        string = string.replace(review, "")
        review_used = True

    choice = ""
    if len(string) <= 60:
        choice = string
        choice = _check_phone_review(choice, phone, review_used)
    else:
        while len(string) > 60:
            string = string.strip()
            single_line = string[:60]
            if string[60] == " ":
                if first:
                    single_line = _check_phone_review(
                        single_line, phone, review_used
                    )
                choice = _check_first_line(choice, single_line, first)
                first = False
                string = string[60:]
            elif " " in single_line:
                last_space = single_line.rindex(" ")
                single_line = single_line[:last_space]
                if first and (review_used or phone):
                    spaces = " " * (60 - len(single_line))
                    single_line = single_line + spaces
                    single_line = _check_phone_review(
                        single_line, phone, review_used
                    )
                choice = _check_first_line(choice, single_line, first)
                first = False
                string = string[last_space:].strip()
            else:
                if first:
                    single_line = _check_phone_review(
                        single_line, phone, review_used
                    )
                choice = _check_first_line(choice, single_line, first)
                first = False
                string = string[60:]
        # add last line
        choice = choice + f"\n   {string.strip()}"

    return choice
