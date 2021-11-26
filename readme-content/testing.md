# Testing

[Back to main](../README.md)

- [Testing](#testing)
  - [User Name](#user-name)
  - [Yes/No Validation - Rules](#yesno-validation---rules)
  - [Yes/No Validation - Keywords](#yesno-validation---keywords)

## User Name

The user name should be up to 18 characters in length. It may contain numbers,
letters and spaces. No special characters are valid and profanity is excluded via
the [`better_profanity`](../README.md#python-packages) package.

- Start the program and press enter with no input:
  ![No user name input](./images/testing/user-no-input.png)
  - Result is as expected, a string reports that you must enter a user name.
  - Input is re-initiated.
- Start the program and enter a user name containing profanity:
  ![Profanity in user name](./images/testing/user-profanity.png)
  - Result is as expected, a string reports that profanity has been detected.
  - Input is re-initiated.
- Start the program and enter a user name containing invalid characters:
  ![Invalid characters in user name](
    ./images/testing/user-invalid-chars.png)
  - Result is as expected, a string reports that invalid characters have been
    detected.
  - Input is re-initiated.
- Start the program and enter a user name longer than 18 characters:
   ![Long user name](./images/testing/user-over-18-chars.png)
  - Result is as expected, a string reports that the user name is too long.
  - Input is re-initiated.
- Start the program and enter a valid user name:
  ![Valid user name](./images/testing/user-invalid-chars.png)
  - Result is as expected, user name is accepted.
  - Program continues.

## Yes/No Validation - Rules

- With a valid user name:
  - Press enter with no input when `('y', 'n')` is present:
    ![Yes/No no input](./images/testing/yn-no-input.png)
    - Result is as expected, a string reports an invalid input is received.
    - Input is re-initiated.
  - Press enter with an invalid input when `('y', 'n')` is present:
    ![Yes/No invalid input](
      ./images/testing/yn-invalid-input.png)
    - Result is as expected, a string reports an invalid input is received.
    - Input is re-initiated.
  - Press enter with a valid 'y' input when `('y', 'n')` is present:
    ![Yes/No y-valid input](./images/testing/yn-y.png)
    - Result is as expected, program continues to the rules.
  - Press enter with a valid 'n' input when `('y', 'n')` is present:
    ![Yes/No n-valid input](./images/testing/yn-n.png)
    - Result is as expected, program continues to next user input prompt.

## Yes/No Validation - Keywords

- With a valid user name
- After displaying or passing the rules:
  - Press enter with no input when `('y', 'n')` is present:
    - [*Similar image above*](#yesno-validation---rules)
    - Result is as expected, a string reports an invalid input is received.
    - Input is re-initiated.
  - Press enter with an invalid input when `('y', 'n')` is present:
    - [*Similar image above*](#yesno-validation---rules)
    - Result is as expected, a string reports an invalid input is received.
    - Input is re-initiated.
  - Press enter with a valid 'y' input when `('y', 'n')` is present:
    ![Yes/No y-valid input](./images/testing/keyword-y.png)
    - Result is as expected, program continues to the keywords.
  - Press enter with a valid 'n' input when `('y', 'n')` is present:
    ![Yes/No n-valid input](./images/testing/keyword-n.png)
    - Result is as expected, program continues to load question data.
