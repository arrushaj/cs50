# CS50 MESSAGE BOARD
#### Video Demo:  https://youtu.be/I3w7p6Mb0pg
#### Description:
My project is a Message Board where you create threads, create replies, update replies, delete replies, delete threads, etc.
It is a Flask project created using mainly Python, HTML, CSS, and a little bit of Javascript.
I will go over all of the files contained in the folder.

To start with, the main file, app.py, contains many routes that direct you to their respective HTML forms contained in the templates folder. In addition, there is a database called forum.db
that is updated in many of the routes. So for example, when a thread is created, the forum database is updated by adding an entry in the thread table along with the replies table. Each time that
thread has a response, the database is further updated by adding another entry to the replies table for that reply and setting the previously added thread row's replies field to itself + 1, indicating that there is more than one reply to that thread.