# Welcome To CoffeeClique
Student Engagement Tool For Blended Learning

### Group F

The group members are:

1. Alexandros Babalitis
2. William Droin
3. Andrei Lazar
4. Victor Lecardonnel
5. Victoria Schneider
6. Isabel Sebire

## About the project

This is the development GitHub for our project.

Our research shows that students miss being in situations where they meet new people, and would like something to facilitate meeting others with similar interests and to help them feel connected to their peers.

CoffeeClique is a website to keep students engaged during the pandemic, by creating an online space where students can interact with each other and tackle fun and rewarding tasks together. Students can meet others with shared interests at tables in our 'cafe'; our virtual cafe environment creates a student community space in this era of online learning.

## Motivation

We surveyed 45 students in different universities, year groups, and across over 25 diverse subjects for their experiences with remote or blended learning at University.

82.2% of students found that being in situations where you can meet new people is challenging currently. Students miss 'mixing with different groups of people', 'interacting with many people daily', and 'meeting new people'. Other issues were getting in contact with people via social media (26.7%) and finding common interests with people (20%).

Only 15.5% of students currently find a primary support network in course or society friends (primary support networks are primarily with housemates or family). We aim to increase connection and forge friendships particularly between people sharing interests and academic course. 88.6% of students said something to facilitate meeting people with common interests would help them feel less isolated in the pandemic. Furthermore, 48.9% actively seek more friends with similar interests, and one student said they would particularly like to see a feature to 'match people based on common interests' in our app.

Nearly 1/4 of students reported that they actively seek more friends and support within their course, and that an academic peer support network would make them feel less isolated. Many students miss 'learning together' with classmates, and want 'better communication with people on \[their\] course' so they can 'make new friends' and 'discuss course related concerns'. Over half of students said a way to be connected with peers would help them to engage more with module content. Students also said that a way to check off tasks and compare progress to peers would be helpful. Similarly, 37.8% of students wish for more frequent interaction with staff and miss being able to 'chat to lecturers'.

## Features

95.6% of students surveyed used cafes in some degree for studying and socialising pre-covid; CoffeeClique provides a virtual cafe space. With the responses to our research in mind, CoffeeClique has the following Key Features:

* Dynamically join tables based on your course and interests, where you can easily interact with similar students and appropriate staff, and chat live.
* View the interests and collectables of others you share a table with, and connect on social media.
* Check the dashboard with leaderboard and feed of notifications to compare your progress with others.
* Create and complete tasks to earn points, progress through stages, and earn collectables.
* Earn bonus points when you work together for everyone in a group to complete a task.
* Gain structure though recurring tasks, and set study timers to co ordinate break times with others in a group.
* See the number of active users in the cafe for the campus community feeling.
* Work together at 'day' or 'night', using our dark mode feature.

## Usage

As our product is a web app, it is easily accessible both from mobile and desktop devices and does not require installation. You can access CoffeeClique's hosted website here: https://python-django-app-coffee.eu-gb.mybluemix.net

Please refer to our Privacy Policy and Terms of Use for how we process your data and how you are expected to behave using our service.

After signing up for an account, users can log in to access the main functionality of our product. When users first log in, they are presented with a display of the cafe tables they are part of. Users are automatically added to the appropriate cafe tables based on their University and any interests they have added, so they can easily interact with other students with similar interests. To add interests or otherwise modify user information, you can access the appropriate page from the cafe tables home page.

Within a cafe table, users have access to a 'group chat' with the other members of the table. Users can also view who else is at the table, and any tasks set for that group of students by a staff member. Completing these tasks will provide a fun and motivational way to work together.

The task system is gamified and students can gain points by completing tasks, providing an incentive to engage with University activities and each other. A leaderboard of the current top 10 scoring students is an additional incentive; we only display the top 10 users so as not to disincentivise users with less points.

Community, connection, and celebrating individual's interests are key to our project. We hope you will enjoy making new friends at CoffeeClique!

## Technologies

The web app is built in Python using the Django framework and the associated SQLite database, and is hosted on IBM Cloud. We have also used HTML/CSS/JS for the front end. We used Figma to create our mock up designs, and Trello for project management, following the agile kanban methodology.

## Installation

You **do not** need to install anything to use our product; simply navigate to our hosted web site at: https://python-django-app-coffee.eu-gb.mybluemix.net.

However, if for development and testing purposes you wish to run a copy of this project locally, you can follow these steps:
1. Clone this repository
2. Navigate to the directory GSEP_F_In_The_Chat
3. Ensure Python is installed. You can downloaded the latest version of Python at https://www.python.org/downloads/
4. Ensure all dependencies are satisfied (see requirements.txt). Dependencies can be installed using ```pip install sample-package-name```. 
5. Run ```python manage.py runserver```
6. Navigate to http://127.0.0.1:8000/ in a web browser
7. To run tests, run ```python manage.py test```
