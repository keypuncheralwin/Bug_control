# Bug Control
A simple bug tracking application made using flask python, html, css and javascript

[Live Website](https://bug-control.herokuapp.com/)


## How it works and who is it for?
This app is designed for hobbyist developers or developers in small teams to help keep track of bugs in their projects. 

Once the user has logged in it takes them to a dashboad which gives them a personalised overview of the current bugs and the users who reported them. Form there the user is free to view the current bugs in the system, update it, mark it as resolved and archive it. They can also report a new bug.

## How to set this up locally on your machine
The backend of this app was made using python and flask so you'll need to have python installed to run this locally.

Once you've instlled python, go ahead start up a local environment by typing in the following command.

<code>python -m venv venv</code>

Then activate the virtual environment

<code>source venv/bin/activate</code>

You'll need to now install all the required modules to ensure the app runs smoothly on your local server. This can be done by running the following command (adjust it to make sure it is pointing to the right path)


<code>pip install -r /path/to/requirements.txt</code>

Postgress was used to set up the databse but you're welcome to use to whatever database you're comfortable with. Just run the schema file to setup the databse.

