"""Run a quiz game via a CLI"""
# Write your code to expect a terminal of 80 characters wide and 24 rows high


def get_user_name():
    """Allows user to input a username

    Returns:
        A string as a username.
    """

    while True:
        print("Characters A-Z, a-z, 0-9 and spaces are permitted.")
        new_user_name = input("Please enter a user name:\n")
        if check_user_name(new_user_name):
            break

    return new_user_name


def check_user_name(user_name_str):
    """Checks username input is valid

    Returns:
        True if valid, else false.
    """

    # new_user_name = input("Please enter your user name:\n")
    try:
        if not "".join(user_name_str).isalnum():
            raise ValueError(
                "Invalid characters detected"
            )
    except ValueError as e:
        print(f"Error: {e}, please try again.\n")
        return False

    return True


print(get_user_name())
