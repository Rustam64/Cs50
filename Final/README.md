# Coupanel
#### https://youtu.be/2nzAa96XUXA
#### Description:
Coupanel is a web application for keeping track of items ordered through coupang, South Korea’s popular e commerce platform, as well as get some insights into monthly spendings and earnings. Throughout development I aimed to implement as many concepts and techniques as possible that I learned through the course.
The project is clearly divided into folders and files, please go over them before running the flask file. You should first initialize the database using the init.py file in the root repository before running ‘flask run’ in the terminal in the app folder.
Libraries and technologies used:
•	Flask
•	SQLalchemy
•	Bootstrap
•	Jinga
•	Werkzeug security
Database:
This project makes use of SQL and the python library for managing it, SQL alchemy. The models are stored in models.py and the functions are stored in products functions to avoid cluttering app.py. The SQL tables are as follows:
•	Products - keep track of products, their prices, links etc.
•	Users – usernames and passwords.
•	Monthly Sales – monthly spendings and earnings.
To maintain a clean structure and make the code more readable the functions are as mentioned above stored in a separate file. The SQL queries are difficult to call without app context, therefore they are called through custom functions.
The monthly sales are automated for the most part, they automatically add to the values of orders once they are added to the system, the earnings have not been configured yet, but it can be done in a similar fashion.
Html pages:
The html pages are in the templates folder and are responsible for presenting raw information from the routes in a clear fashion using jinja.
Layout: for a navigation bar using bootstrap and unnecessary filler code.
Index: main page that the user sees and the inventory of items in a table.
Waiting: a table of items that have been ordered so far.
Shipped: a table of items that have been shipped.
Register and login: for creating an account and logging-in.
Monthly: for displaying some data on all current products and monthly spendings.
Core Files:
-Init.py
This file is used to set up the database, be careful when running it as it clears and drops the current tables before recreating them based on models.py.
-helpers.py
This file was taken from the finance project in Harvard CS50, I only kept the login required function as it was neat and helpful in my case.
- App.py
This is the main function where the flask and SQL sessions are set-up and configured. Note that this file should not be run by itself but rather started with ‘flask run from’ the terminal.
The routes in app are as follows:
•	‘/’ or ‘/Index’ – The main page, as well as the page where items that are stored in inventory are displayed.
•	‘/shipped’ – The page where items categorized as ‘shipped’ are displayed.
•	‘/waiting’ – The page where items categorized as ‘waiting are displayed.
•	‘/register’ – A very simple form page to register an account.
•	‘/login’ – A very simple form page to login.
•	‘/logout’ – Not linked to an html file, rather just used a route to logout the current session.
•	‘/orders’ – This page is used for 2 main functions, to help the user search for items on coupang via a search form and to add items to the database, the form takes item information such as name, price and quantity and inserts them into the table, the product link is cut using regular expressions and inserting invalid links will cause an error.
•	‘/monthly’ – This route is used to display how much money worth of items is currently in each category as well as how much was spent in each month.
For productivity reasons, the database also stores the value of each item in the Uzbek market. As the site was developed to help track and sort items that are meant to be shipped to Uzbekistan, is converts the South Korean price to Uzs, compares it to the Uzbek price before giving a suggestion on a price to sell the items at. The suggested price is only displayed in the Index page where items that are to be shipped are, in all other routes, the page only displays the local and Uzbek price.

Although Coupanel is fully functional, there are several features I'd like to implement in the future. These include automatic currency rate updates, user profile customization, better error handling, and improved chart visualizations for monthly analytics. There's also potential for adding receipt image uploads and basic AI-based product suggestions.
