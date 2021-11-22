# Name of project

<!-- remove before final deployment -->
[ToDo List](./todo.md)

A gentle reminder to all - to open links in a new tab,
hold 'Ctrl' (or '⌘' on Apple devices) as you click!

<!-- ![Multiple Device Demo](
  ./readme-content/images/multi-device.png) -->

## Live Site

[Computer Literate Investigation](https://computer-literate-investigator.herokuapp.com/)

## Repository

[https://github.com/daveyjh/ci-portfolio-three](
  https://github.com/daveyjh/ci-portfolio-three)

***

## Table of Contents

- [Name of project](#name-of-project)
  - [Live Site](#live-site)
  - [Repository](#repository)
  - [Table of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Brief](#brief)
    - [**C**omputer **L**iterate **I**nvestigation](#computer-literate-investigation)
  - [UX &#8722; User Experience Design](#ux--user-experience-design)
    - [User Requirements](#user-requirements)
      - [First Time User](#first-time-user)
      - [Returning User](#returning-user)
      - [Interested Party](#interested-party)
    - [Initial Concept](#initial-concept)
      - [Wireframes](#wireframes)
      - [Colour Scheme](#colour-scheme)
      - [Typography](#typography)
      - [Imagery](#imagery)
  - [Features](#features)
    - [Existing Features](#existing-features)
    - [Features Left to Implement](#features-left-to-implement)
  - [Technologies Used](#technologies-used)
    - [Python Packages](#python-packages)
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
    - [Personal Development](#personal-development)

***

## Objective

Design an interactive quiz that uses an existing API for questions and answers.
The project should run in a CLI, deployed via Heroku, using Python.

***The needs within this project are not genuine and are made purely
for the purpose of completing my Code Institute project***

***

## Brief

### **C**omputer **L**iterate **I**nvestigation

The goal of this site is to provide an interactive quiz with increasing
difficulty levels. The final product should:

- be programmatically error free
- be written using Python
- have a varied question base to allow replayability
- handle all user input errors gracefully and appropriately
- give clear instructions regarding use and valid inputs

***

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

***

### Initial Concept

I intend to make a quiz application based around the popular television quiz
show *'Who Wants To Be A Millionaire?'*. I anticipate using a pre-populated API
for the questions and answers, using a 'level of difficulty' selection built in
to the API. I also intend to have a couple of 'life-line' options available to
the user. Finally, I would like to implement a high-score spreadsheet
maintained via Google Sheets.

#### Wireframes
<!-- wireframes here -->
<!-- *See [here](./readme-content/wireframes.md#tablet) for other device types* -->
***

#### Colour Scheme

<!-- colour scheme, remember to contrast check!!! -->
***

#### Typography

<!-- orbitron/rajdhani due to style -->
<!-- typography -->
***

#### Imagery

<!-- imagery -->
***

## Features

### Existing Features

<!-- - Feature 1 - allows users X to achieve Y, by having them fill out Z -->
<!-- 1. feature1
>*"User... **story quote**"*
- *explanation*-->
F1
***
<!-- - Feature 2 - allows users X to achieve Y, by having them fill out Z -->
<!-- 1. feature2
>*"User... **story quote**"*
- *explanation*
  ![imgName](imgURL)
-->
F2
***

### Features Left to Implement

1. Even The Odds
   - *This will allow users to remove 2 incorrect answers*
   - If a user inputs a keyword, they will be presented with the question and
    only 2 answers, one of which will be correct. This will only be allowed once
    during each play.

2. Call A Coder
   - *This will allow users to receive some advice from an ersatz friend*
   - If a user requires assistance on a question, they may input a keyword that
    generates a simulated response from another coder. The response received
    may not be correct. I intend to scale this depending on the current
    question number.

3. Request A Review
   - *This will allow users to pose the question to a pseudo panel of
    spectators*
   - If a user is struggling with an answer, they may request assistance from a
     spurious audience. The responses received may not be correct. I intend to
     scale this depending on the current question number.

***

## Technologies Used

### Python Packages

- random
  - shuffle: used to generate random ordering
  - randrange: returns a random integer within a given range
- html
  - unescape: converts HTML entities to printable characters
- time
  - sleep: stalls the program for a defined time
- requests: enables data retrieval from APIs
- gspread: allows communication with Google Sheets
- from google.oauth2.service_account
  - Credentials: used to validate credentials and grant access to google
    service accounts
- better_profanity
  - profanity: simple profanity checker
- getch
  - pause: used to provide a *'Press any key to continue...'* function
<!-- tech used -->
<!-- - *[techNameOne](techURL)*
       - Description -->
<!-- - *[techNameTwo](techURL)*
       - Description -->

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
***
<!-- - bugTwo explanation

*notes on explanation* -->
***

### Resolved

<!-- resolved bugs -->
<!-- 1. bugOne

![bugOneImg](bugOneImgURL)

*Commit - **[sha](commit link with highlighted lines)** - explanation of fix* -->
***
<!-- 1. bugTwo

![bugTwoImg](bugTwoImgURL)

*Commit - **[sha](commit link with highlighted lines)** - explanation of fix* -->
***

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
***

## Credits

### Content
<!-- - the a comes from b -->
<!-- - the c comes from d -->
### Media
<!-- - the a comes from b -->
<!-- - the c comes from d -->
### Acknowledgements
<!-- - acknowledge a, found at [b](bURL), for c -->
<!-- - acknowledge d, found at [e](eURL), for f -->
***

### Personal Development

<!-- notes -->