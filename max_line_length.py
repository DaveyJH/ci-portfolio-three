"""Handles line length of text"""


def limit_line_length(string: str):
    """Prints individual lines with a max line length of 80 characters

    Checks for and prevents prepending spaces/split words

    ---
    Args:
        string (str): String to be altered to fit within 80 character lines#
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
