Mini-EBay Project
Christopher Nelson
Intro to Database Systems

Description
Final project for the Intro to Database Systems. Users can create items to bid on, or bid on items themselves.
SQLite was used to create the database and manage the bids and items. Python, and webpy, were also used to 
interact with the database. HTML was used to design the website.

To run, you'll need sqlite and webpy installed, then do the following:

In the command prompt, navigate to the project directory and type:
sqlite3 ebay.db

At the sqlite> prompt type the following twice (bug with schema.sql):
.read ebay/schema.sql

Exit the sqlite> prompt and type the following:
cd ebay
python ebay.py

Open the displayed address on your browser. 

