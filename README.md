# Title: Maple Match

#### Video Demo:  https://youtu.be/3m8UB4gwVxM

#### Description:
	This project implements a web application, Maple Match, designed to simplify the job search for foreign workers seeking LMIA-approved positions in Canada. It bypasses general job boards and connects users directly with employers offering LMIA-approved opportunities, streamlining the process and accelerating their path to Canadian employment. There are 18553 jobs, 15166 employers, 12606 locations, 399 occupations, 13 regions, 4 program streams

#### Installation/Usage:
	This project is yet to be hosted. However if you wish to run it on a development server, you will need to install the following: the cs50 python library, flask library and the flask-session library. These requirements can be found in the requirements.txt file in the home directory.

#### Motivation:
	A few months back, I heard about the LMIA and how it helps improve the chances of finding a job and subsequently moving to canada. However, upon checking the  excel file containing the job listings, I saw it had almost 20,000 job listings which was too many to keep track of. This was when I was inspired to create this webapp aptly named "Maple match" after the maple leaf in the canadian flag and started working on simplifying the job search.

#### Indepth Description:
	This web application was created to simplify the job search process for individuals seeking opportunities through Canada's Labour Market Impact Assessment (LMIA) program.  This webapp was built using flask as the backend HTML, CS and JavaScript for te frotend and sqlite3 for the database. In the home directory, there are four folders which are static, templates, flask_session, db_builder and five files which are app.py, helpers.py, jobs.db, README.md and requirements.txt.

##	templates:
		This folder contains the all the HTML files in this webapp; apology.html which is rendered when there is an error, index.html the homepage, search.html which is used to search jobs, starred.html which is used to view saved jobs, about.html which has information about LMIA in general, login.html and register.html which are used to login and register respectively.

##	static:
		This folder contains the css file, the favicon.ico and the maple leaf image we use in our webapp

##	flask_session:
		This folder contains data used by flask to implement sessions and SHOULD NOT BE CHANGED OR EDITED

##	db_builder:
		This folder contains the files used to build the database from the cleaned csv file released by the government of canada.
		lmiaQ3.csv is the csv file, db_builder is the python program used to fill the database, schema.sql is the set of instructions used to create the tables, helpers.py contains helper functions, and jobs.db is the database file.

##	app.py:
		This is my main file for the backend of the webapp. It contains all the eight routes I implemented in my webapp namely;   /index for displaying the homepage,
		/login to handle logins,
		/register to handle registrations,
		/logout to handle logouts,
		/search to handle searching for jobs and displaying them,
		/star for handling the saving of jobs to be viewed later,
		/unstar to remove a job from saved jobs and
		/about to display the information concerning LMIA
##	helpers.py:
		This contains the helper functions used in app.py like
		apology which handles the creation of error messages,
		login_required to make sure some routes can only be accessed after logging in,
		region_check to convert regions to integers to be stored in the database,
		program_stream_check to convert program streams to integers to be stored in the database,
		check and validate to validate user input.
##	jobs.db:
		This database file contains all the data required by my webapp and stores all the data received from my webapp

##	README.md:
		This is the file you are currently looking through and it contains a description of my project

##	requirements.txt:
		This contains all the programs/libraries needed to run this webapp on a development server

#### Contributing:
	As of now, this project is yet to be on a remote server, so for any collaborations, E-mail me at ibeaghaemmanuel@gmail.com.

#### Credits:
	All the data used for this project were proided by the Temporary Foreign worker Program of the government of Canada, and
	My apology and login_required functions were adapted from the cs50 pset9 distribution Code
