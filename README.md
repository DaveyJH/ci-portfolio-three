# Name of project

A gentle reminder to all - to open links in a new tab,
hold 'Ctrl' (or '⌘' on Apple devices) as you click!

<!-- ![Multiple Device Demo](
  ./readme-content/images/multi-device.png) -->

## Live Site

[**C**omputer **L**iterate **I**nvestigator](
  https://computer-literate-investigator.herokuapp.com/)

## Repository

[https://github.com/daveyjh/ci-portfolio-three](
  https://github.com/daveyjh/ci-portfolio-three)

---

## Table of Contents

- [Name of project](#name-of-project)
  - [Live Site](#live-site)
  - [Repository](#repository)
  - [Table of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Brief](#brief)
    - [**C**omputer **L**iterate **I**nvestigator](#computer-literate-investigator)
  - [UX &#8722; User Experience Design](#ux--user-experience-design)
    - [User Requirements](#user-requirements)
      - [First Time User](#first-time-user)
      - [Returning User](#returning-user)
      - [Interested Party](#interested-party)
    - [Initial Concept](#initial-concept)
      - [Wireframes](#wireframes)
        - [Desktop](#desktop)
        - [Mobile](#mobile)
      - [Colour Scheme](#colour-scheme)
      - [Typography](#typography)
      - [Imagery](#imagery)
  - [Logic](#logic)
    - [Initial Flow](#initial-flow)
    - [Python Logic](#python-logic)
  - [Features](#features)
    - [Existing Features](#existing-features)
      - [UX](#ux)
      - [Keywords](#keywords)
    - [Features Left to Implement](#features-left-to-implement)
  - [Technologies Used](#technologies-used)
    - [Python Packages](#python-packages)
    - [Other Tech](#other-tech)
      - [VSCode Extensions](#vscode-extensions)
  - [Testing](#testing)
  - [Bugs](#bugs)
    - [Current](#current)
    - [Resolved](#resolved)
  - [Development](#development)
  - [Deployment](#deployment)
  - [Credits](#credits)
    - [Content](#content)
    - [Media](#media)
    - [Acknowledgements](#acknowledgements)

---

## Objective

Design an interactive quiz that uses an existing API for questions and answers.
The project should run in a CLI, deployed via Heroku, using Python.

***The needs within this project are not genuine and are made purely
for the purpose of completing my Code Institute project***

---

## Brief

### **C**omputer **L**iterate **I**nvestigator

The goal of this site is to provide an interactive quiz with increasing
difficulty levels. The final product should:

- be programmatically error free
- be written using Python
- have a varied question base to allow replayability
- handle all user input errors gracefully and appropriately
- give clear instructions regarding use and valid inputs

---

## UX &#8722; User Experience Design

### User Requirements

Some example user stories which will affect the design

#### First Time User

> *"As a programmer, I would like to test my knowledge"*
>
> *"As a quiz fanatic, I would like to know how I compare with other users"*
>
> *"As someone who hasn't used a CLI before, I would like to know my inputs
> are valid"*

#### Returning User

> *"As a returning user, I would like to see a list of high-scores"*
>
> *"I would like to know if my scores are in the high-scores list"*
>
> *"If I return to play again, I would like to play different questions"*

#### Interested Party

> *"As someone interested in how the application has been made, I am interested
> to see how user inputs have been validated and errors have been handled"*

---

### Initial Concept

I intend to make a quiz application based around the popular television quiz
show *'Who Wants To Be A Millionaire?'*. I anticipate using a pre-populated API
for the questions and answers, using a 'level of difficulty' selection built in
to the API. I also intend to have a couple of 'life-line' options available to
the user. Finally, I would like to implement a high-score spreadsheet
maintained via Google Sheets.

#### Wireframes

Due to the nature of this project the wireframes are very basic. There is only
one page and the design does not change across any devices, only a change in
content.

##### Desktop

![Desktop Wireframe](./readme-content/wireframes/index.png)  

##### Mobile

![Mobile Wireframe](./readme-content/wireframes/mobile.png)

---

#### Colour Scheme

The colour scheme for this project relies heavily on the colours available
through the `colorama` package within Python. The package has allowed a few
colours to be applied to text within the terminal environment. The colours
outside the terminal are designed based around a classic CRT style monitor.  
Contrast checks have been done to ensure the 'Run Program' button and text
present are of a high enough contrast to be easily read.

---

#### Typography

VT323 has been chosen from Google Fonts for the header, footer and button.
The font is styled much like a classic terminal font and is perfect for this
application.

---

#### Imagery

The background image is a modified image from [pexels.com](https://pexels.com)
and has been used as it reminded me of the introductory lighting that was used
on the 'Who Wants To Be A Millionaire' television show. The colours also
compliment the rest of the design.

---

## Logic

I spent some time planning the logic behind the application to ensure I had a
general idea of how it should be approached. I created flowcharts to allow me
to follow the logic through the application as it developed. The charts were
generated using [Draw.io Integration](#technologies-used) and are shown below.
As can be expected, the flow and features changed over the course of the
project and so the charts do not accurately reflect all aspects of the end
product.

### Initial Flow

![Flow Chart](readme-content/images/quiz-logic.png)

---

### Python Logic

![Flow Chart](readme-content/images/python-logic.png)

## Features

### Existing Features

#### UX

> *"As a programmer, **I would like to test my knowledge**"*

- The quiz uses an API that has a 'Science: Computers' category. This ensures
  the questions are related to code and computing in general.

---

> *"As a quiz fanatic, **I would like to know how I compare with other
> users**"*
>
> *"As a returning user, **I would like to see a list of high-scores**"*
>
> *"I would like to know if **my scores are in the high-scores list**"*

- The program has a score board feature. This can be accessed by users through
  the use of a keyword.

  ![Score Board](readme-content/images/scoreboard.png)

---

> *"As someone who hasn't used a CLI before, **I would like to know my inputs
> are valid**"*

- All user inputs are validated and errors allow repeat opportunites to input
  a valid selection.

  ![Invalid Input](readme-content/images/testing/user-no-input.png)

---

> *"If I return to play again, **I would like to play different questions**"*

- The API used has a token service that prevents repeat questions. The token
  only lasts 6 hours and the question quantity is fairly limited. Without
  adding some additional, verbose code, using and storing these tokens is the
  most effective way of trying to prevent repetition for users.

---

> *"As someone interested...**how user inputs have been validated and errors
> have been handled**"*

- The practices used within the program validate data when retrieving it from
  external sources. The overall design ensures a positive user experience and
  handles errors in an appropriate manner.

  ``` Python
  try:
      if response.status_code != 200:
          raise TypeError("API response missing")
      if "response_code" not in data:
          raise ValueError("API structure corrupt")
  except (TypeError, ValueError) as e:
      red_print(f"Critical Error: {e}")
      red_print("Program will now terminate!")
      exit()
  ```

---

#### Keywords

1. Even The Odds
   - *This allows users to remove 2 incorrect answers*
   - If a user inputs a keyword, they will be presented with the question and
    only 2 answers, one of which will be correct. This will only be allowed
    once during each play.

2. Call A Coder
   - *This allows users to receive some advice from an ersatz friend*
   - If a user requires assistance on a question, they may input a keyword that
    generates a simulated response from another coder. The response received
    may not be correct. The chance of the response being correct is scaled
    depending on the current question number.

3. Request A Review
   - *This allows users to pose the current question to a pseudo panel of
    spectators*
   - If a user is struggling with an answer, they may request assistance from a
     spurious audience. The responses received may not be correct and are
     scaled depending on the current question number.

4. Help
   - *This allows users to read through the rules and keyword meanings during
    the quiz*
   - This will prevent user frustration due to forgettinng any keyword
    meanings.

5. Take
   - *This allows users to leave the quiz with their current score*
   - By providing this feature, if users are unsure of an answer, they may
    stop the quiz in the hope of having their score entered on the score board.

6. Scores
   - *This allows users to view the score board at any time*
   - This feature enables users to check where they are in relation to the high
    scores before deciding whether to attempt difficult questions. It also adds
    a nice competetive element to encourage returning visits.

7. ???
   - *There is a secret keyword that has a secret function*
   - This feature is just here for fun...remember, the cake is a lie!
   - 'Hi Ron!' ༼ ◕_◕ ༽つ

---

### Features Left to Implement

At present, I am happy with the features in the program. Possible additions
could include:

- a category option - for users not interested in computers
- personal tokens - to further reduce the likelihood of repeated questions
- a larger scores database - over time, the top scores may be difficult for
    some users to reach. A larger database would allow for recognition of the
    position achieved if it is not within the top ten

---

## Technologies Used

### Python Packages

- requests: enables data retrieval from APIs
- gspread: allows communication with Google Sheets
- colorama: allows terminal text to be printed in different colours/styles
- random
  - shuffle: used to generate random ordering
  - randrange: returns a random integer within a given range
- html
  - unescape: converts HTML entities to printable characters
- time
  - sleep: stalls the program for a defined time
- google.oauth2.service_account
  - Credentials: used to validate credentials and grant access to google
    service accounts
- better_profanity
  - profanity: simple profanity checker
- getch
  - pause: used to provide a *'Press any key to continue...'* function

---

### Other Tech

- *[Instant Eyedropper](http://instant-eyedropper.com/)*
  - A quick and simple application to obtain hex values from any colour on my
  display. I downloaded this while playing around with my laptop layout/display
  settings. I have the app set to run on startup and remain minimized in my
  system tray. This allows quick access and if I click the colour, it
  automatically copies the value to my clipboard.
- *[WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)*
  - A basic contrast checking service for conformity to the Web Content
  Accessibility Guidelines. The service allows input of a foreground and
  background colour and displays the resulting contrast ratio, including a quick
  reference to meeting WCAG AA / AAA standards.
- *[Windows Snipping Tool](https://support.microsoft.com/en-us/windows/use-snipping-tool-to-capture-screenshots-00246869-1843-655f-f220-97299b865f6b)*
  - A screenshot tool built in to Windows. It allows quick, partial screenshots
  to be taken that can be saved as image files.
- *[Balsamiq](https://balsamiq.com/)*
  - Balsamiq was used to create [wireframes](./readme-content/wireframes.md)
  for the project.
- *[Adobe Photoshop](https://www.adobe.com/uk/)*
  - The background image was modified and converted using this image editing
  software
- *[Font Awesome](https://fontawesome.com/)*
  - The project uses icons from Font Awesome version 5.
- *[Google Fonts](https://fonts.google.com/)*
  - The fonts used in the website are imported from Google Fonts.
- *[Multi Device Mockup Generator](https://techsini.com/multi-mockup/index.php)*
  - The image at the top of this document was created using a free service
  provided by TechSini.&#8203;com
- *[W3C Markup Validation Service](validator.w3.org)*
  - A service to check the HTML and CSS files for errors. During
  development, I copied the entire text from the files and ran them through the
  direct input method. Upon completion, I ran the deployed site through the
  'Validate by URI' method with [results here](#w3c-validator).
- *[PEP8 online](http://pep8online.com/)*
  - An online Python code validation service.
- *[Visual Studio Code](https://code.visualstudio.com/)*
  - A free, streamlined code editor. The [extensions](#vscode-extensions)
  available have allowed me to customize my workspace and become more
  efficient.

#### VSCode Extensions

Links to the VSCode marketplace for each extension used throughout this project:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Better Comments](https://marketplace.visualstudio.com/items?itemName=aaron-bond.better-comments)
- [Bracket Pair Colorizer 2](https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer-2)
- [GitHub Pull Request and Issue Provider](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github)
- [Highlight Matching Tag](https://marketplace.visualstudio.com/items?itemName=vincaslt.highlight-matching-tag)
- [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one)
- [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)
- [Preview on Web Server](https://marketplace.visualstudio.com/items?itemName=yuichinukiyama.vscode-preview-server)
- [Colored Regions](https://marketplace.visualstudio.com/items?itemName=mihelcic.colored-regions)
- [Reflow Markdwon](https://marketplace.visualstudio.com/items?itemName=marvhen.reflow-markdown)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Draw.io](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio)
- [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)


## Testing

<!-- explain testing
? item tested
? expected result
? how test was performed
? actual result
? differences
? action required
? re-test
- more detail and better format required compared with project 1
look at daisy's testing documentation and [webinar](https://us02web.zoom.us/rec/play/9FIKllHX2ZiQNFRhYPn_hBh_ZeA8964ZvIDLnhpKGAf1NLVc3_hBJ6zSL8Hv5Hx7ALnPtDmbg8CmFAs.YVsZ9LR_uI7OjEwH)-->

<!-- validation of html, css and script. -->
<!-- lighthouse testing -->

## Bugs

### Current

<!-- current bugs -->

<!-- - bugOne explanation

*notes on explanation* -->
---
<!-- - bugTwo explanation

*notes on explanation* -->
---

### Resolved

<!-- resolved bugs -->
<!-- 1. bugOne

![bugOneImg](bugOneImgURL)

*Commit - **[sha](commit link with highlighted lines)** - explanation of fix* -->
---
<!-- 1. bugTwo

![bugTwoImg](bugTwoImgURL)

*Commit - **[sha](commit link with highlighted lines)** - explanation of fix* -->
---

## Development

<!-- section missed in first project. 
!describe development process -->

## Deployment

<!-- !check this section, may need adjusting as using additional languages -->

<!-- **Github Pages**
- Navigate to the relevant GitHub Repository [here](github repo URL)
- Select "Settings" from the options below the name of the repository

![Settings Snip](./readme-content/images/github-settings.png)
- Select "Pages" from the left hand menu

![Pages Snip](./readme-content/images/pages-select.png)
- Select "Branch: main" as the source and leave the directory as "/(root)"

![Source Snip](./readme-content/images/pages-source.png)

- Click the Save button

- Take note of the URL provided

![URL Snip](./readme-content/images/pages-url.png)

- GitHub takes a short while to publish the page. The bar turns green if you refresh the pages tab and the page has been deployed

![Confirmed Deployment Snip](./readme-content/images/pages-deployed.png)
- Click the link or copy the URL to a browser to reach the deployed page
https://daveyjh.github.io/ci-portfolio-one-v4/

The site is now live and operational -->
---

## Credits

### Content

- The question database and API fucntionality was obtained through
  [opentdb.com](https://opentdb.com/)
- The terminal function and template for the deployable application was
  provided by [Code Institute](https://codeinstitute.net), with special mention
  to [Matt Rudge](https://github.com/lechien73)

### Media

- The background image was sourced from [pexels.com](https://pexels.com) and
  was provided by [Wendy Wei](
    https://www.pexels.com/@wendywei?utm_content=attributionCopyText&utm_medium=referral&utm_source=pexels)

### Acknowledgements

- Thank you to [Fiona Tracey](https://github.com). I reached out in the Code
  Institute Slack community with a minor issue. Fiona provided a wonderfully
  simple solution to prevent some unused variable warnings as detailed below:

  ```Python
  string = "this is a string" # This string was from the KEYWORDS list
  line = ""

  for char in string:
      line += "="      # 'char' variable is unused 

  # Above was my original code to create an underline of '='s for some titles

  # Below is a neater solution that led to a better approach to other code
  # within the repo

  line = "=" * len(KEYWORDS[index])
  ```

- Thank you to [David Bowers](https://github.com/dnlbowers) for saving me from
  having to trawl through previous Slack messages. Within minutes of asking, he
  provided a link to the exact information I was looking for, detailed below.
  He also has some really awesome work available to look through on his GitHub
  profile, well worth a look.

- Thank you to [Matt Boden](https://github.com/MattBCoding) for sharing his
  project. From there I was able to see the easiest way to style my own project
  to give a more pleasing UX. Matt has a fantastic approach to code, I highly
  recommend a review of his work.

- A big thanks to [Jim Morel](https://www.linkedin.com/in/jim-morel/) and many
  more of the Code Institute slack community members. Jim was able to point me
  in the right direction regarding virtual environments on VSCode and has an
  eternally-positive attitude that really helps in many ways.

- A final huge thank you to [Abi Harrison](https://github.com/abibubble.com)
  and [Emanuel Jose Felisberto Dos Santos Moreira Da Silva](
    https://github.com/manni8436),
  *what an amazing name!* With a great attitude to continued development,
  encouragement along the way, and testing whenever it was needed - These
  two continue to make my developer journey thoroughly enjoyable.
  ![Nerd Life](readme-content/images/nerd-life-text.png)

---
