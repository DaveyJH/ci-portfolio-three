"""Handles line length of text"""

from keywords import TELEPHONE_RED, DOTS


def limit_line_length(string: str):
    """Prints individual lines with a max line length of 80 characters

    Checks for and prevents prepending spaces/split words

    ---
    Args:
        string (str): String to be altered to fit within 80 character lines
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
        print(line)


def limit_question(string: str):

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
    else:
        while len(string) > 60:
            string = string.strip()
            single_line = string[:60]
            if string[60] == " ":
                if review_used:
                    single_line = single_line + review
                    review_used = False
                if phone:
                    single_line = single_line + f"  {TELEPHONE_RED}"
                    phone = False
                if first:
                    choice = choice + single_line
                else:
                    choice = choice + f"\n   {single_line}"
                first = False
                string = string[60:]
            elif " " in single_line:
                last_space = single_line.rindex(" ")
                single_line = string[:last_space]
                if review_used or phone:
                    spaces = " " * (60 - len(single_line))
                    single_line = single_line + spaces
                    if review_used:
                        single_line = single_line + review
                        review_used = False
                    if phone:
                        single_line = single_line + f"  {TELEPHONE_RED}"
                        phone = False
                if first:
                    choice = choice + single_line
                else:
                    choice = choice + f"\n   {single_line}"
                first = False
                string = string[last_space:].strip()
            else:
                if review_used:
                    single_line = single_line + review
                    review_used = False
                if phone:
                    single_line = single_line + f"  {TELEPHONE_RED}"
                    phone = False
                if first is True:
                    choice = choice + single_line
                else:
                    choice = choice + f"\n   {single_line}"
                first = False
                string = string[60:]
        # add last line
        choice = choice + f"\n   {string}"

    return choice
