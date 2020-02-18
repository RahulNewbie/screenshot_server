# Instruction to run screenshot_server application

This application is made in python 3.8 ( compitable for python 3.7 and 3.6). I have used pep8 and pylint to check coding standards.

## Installation: Use tox to run the application

### Tox installation:

Files made for tox:
1. setup.py : (Re)Distributable package installation.

2. requirements.txt : Setting up the development environment.

3. tox.ini : Basic information about the project and the test environments. Should be in the same location as setup.py.

### Execution:

Browse to the project location in the command prompt and run 

python -m tox 

This command will install the application in python 3.7 and python 3.8. For any specific version please run

tox -e py38

Application will be running in localhost:5000

I installed this in my personal windows machine for python 3.7 and 3.8

### Usage: 

This application will open two types of API endpoint for the user

####1. To get screenshot of a website url, use the following command structure in browser

http://localhost:5000/url/option

Here url is the website url

option can have two value

view : This option will show the screenshot in browser

address: This option will show the the address of the saved screenshot

#### As an example

http://localhost:5000/goal.com/view


http://localhost:5000/goal.com/address

Someone can use curl -X GET also for the same

####2. To get the list of all save screenshot in chronological order

http://localhost:5000/list

This will show all the captured screenshot address along with the website url from database.

### Unit test

To run unit test cases, please go to the project folder and run the following command

python unit_test.py


