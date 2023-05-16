# MonitEase

### Description

This application is a mini inventory application which maybe made a full inventory app along the line. This application helps you;
1. Know how many of each stock is remaining.
2. Keep track of your daily sales.
3. Generate Reports or account on a given duration (Daily, weekly etc).
4. Push email when an item reaches restock level.
5. Search of filter by series of conditions (item name, Date sold, have Paid etc).

### Motivation for the Project.

Sometime in 2020, I worked in computer repairs shop, all the records were written on books which makes it difficult to generate accounts at the end of the 
day for days when work end late. With this application, everybody can go home without waiting for account and just generate it from this application.
It happened that the secretary wanted to resign, we had to go through the book from the day the secretary was employed to calculate all the item given to her 
and verify that it matches with what she was leaving behind. 

### Technology

1. This project is built with Django python rest framework.
2. mysql Database.

## Setting Up the Project 

### Install Dependencies

1. **Python 3.10** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/MonitEase` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Django]
- [djangorestframework]
- [mysqlclient]

### Set up the Database

In the settings.py within the MonitEase directory, we have a dictionary called "DATABASES", you can decide to use the specified names.
NOTE: The port number was changed because I have skype on my system and it blocks the default port 3306 of mysql.

The variable after the DATABASE dictionary is for production, so I advise you comment that out while working on development before pushing.

### Run the server

Make sure to start your virtual enviroment.
for linux users, run this

```bash
source myvirtualenv/bin/activate
```

for windows users, run

```bash

```

After starting the virtual envs, navigate to the project directory and run 

```bash
python manage.py runserver
```

### API endpoints documentation


### Auth details

email: august@gmail.com
password: 12345678
role: admin

email: secretary@gmail.com
password: 12345678
role: secratary

email: others@gmail.com
password: 12345678
role: other

email: director@gmail.com
password: 12345678
role: director
