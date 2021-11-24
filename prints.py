"""Handle text colouring"""

from random import randint
import colorama

colorama.init()


def red_print(string):
    """Print string in red"""
    string = f"\033[31;1m{string}\033[0m"
    print(string)


def green_print(string):
    """Print string in bright green"""
    string = f"\033[32;1m{string}\033[0m"
    print(string)


def cyan_print(string):
    """Print string in cyan"""
    string = f"\033[36;1m{string}\033[0m"
    print(string)


def magenta_print(string):
    """Print string on magenta background"""
    string = f"\033[47;45;1m{string}\033[0m"
    print(string)


def yellow_print(string):
    """Print string in yellow"""
    string = f"\033[33;1m{string}\033[0m"
    print(string)


def matrix_style(string):
    """Print string with styled individual characters"""

    result = []

    def random_style(char):
        styles = (
            # green
            "\033[32m",
            # brightgreen
            "\033[32;1m",
            # white
            "\033[37;1m",
            # black
            "\033[30m",
            # grey
            "\033[40m",
            # white on black
            "\033[37;1m\033[40m",
            # white on green
            "\033[37;1m\033[42m",
            # green on white
            "\033[32m\033[47;1m",
            # grey on white
            "\033[40m\033[47;1m",
            # black on white
            "\033[30m\033[47m",
            # green on black
            "\033[32m\033[40m",
            # black on green
            "\033[30m\033[42m",
            # grey on black
            "\033[40m\033[30m",
            # grey on green
            "\033[40m\033[42m"
        )
        style = styles[randint(0, len(styles) - 1)]
        new_char = f'{style}{char}\033[0m'
        result.append(new_char)
        return

    for char in string:
        random_style(char)
    print("".join(result))


def print_tux():
    "Print tux!"
    print(
        "\033[36;1m"
        r"""
              ;####;.
             ;######;.
             #/^Y/^Y##
             #|ʘ||ʘ|##
             #/ᵕ^`¬:##
             #`._.' Y#.
            ╯/      `#;.
           ╯ﾉ        Y#;.
          ╯#;        :##;
         ╯#"         'Y##;
        ¦#(           :###
         ##,         _a##;
       ._/"Y#;,    .|`;#;'|
       \    Y#'    `|  '  `.
       /     \.___~/|    .'
       `--..__)#==##`._.'

        """
        "\n\033[33;1mDaveyJH \033[41;1m(⌐■_■)\033[0m"
    )
