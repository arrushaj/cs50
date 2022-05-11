# CS50 MESSAGE BOARD
#### Video Demo:  https://youtu.be/I3w7p6Mb0pg
#### Description:
My project is a Message Board where you create threads, create replies, update replies, delete replies, delete threads, etc.
It is a Flask project created using mainly Python, HTML, CSS, and a little bit of Javascript. It's also important to mention that I installed a flask-pagination extension. Pagination will not
work without this extension. Also Flask-session is necessary for this to work, crucial actually.
I will go over all of the files contained in the folder.

To start with, the main file, app.py, contains many routes that direct you to their respective HTML forms contained in the templates folder. In addition, there is a database called forum.db
that is updated in many of the routes. So for example, when a thread is created (using the /reply route), the forum database is updated by adding an entry in the thread table along with the replies table. Each time that thread has a response, the database is further updated by adding another entry to the replies table for that reply and setting the previously added thread row's replies field to itself + 1, indicating that there is more than one reply to that thread. If I went over each route and what they did it would take forever so for time's sake I will go over the most intricate routes.

When a user wishes to reply to a specific post in a thread, they hit a reply button which directs them to the "/reply_form" route. This sends you to edit.html which is a page which showcases the
post you are responding to and a textbox where you enter your response. When the response is submitted, it is added to the database as a reply (using /reply_legit route) and is distinguished as a response to another post through a few of its fields in its respective row. This is so that when the thread template is rendered, the template has the knowledge that the post in question is a REPLY to a pre-existing post. The template will then showcase the post it is replying to along with the reply itself.

It's worth mentioning that I desperately wanted to be able to create replies to previous messages dynamically without the use of "/reply_form" using AJAX, but it proved much too difficult as I was having issues with identifying posts that way due to the way Flask renders templates. I think this could be a shortcoming with Flask or maybe just my inexperience.

Likewise, if you want to edit or delete a comment, each of those have their own respective routes that involve database manipulation.

I used Flask-session for logging in and logging out from CS50 Finance. It was a bit limited but I made it work.

Profiles are also available for each user (/profile route). Each profile contains a bio and their respective threads that they have created.

Each sub-board has its own route and it populates their respective HTML form by searching the database for threads that were created for their board.

To discuss the database a little more, it has 4 tables: users, thread, replies, and likes. Users includes users, passwords, and bios. Threads are threads and everything that pertains. Replies are replies to threads and have a thread id as a foreign key. Likes are a system that allows the database to indicate which user is liking which reply. When a reply is deleted, any like row related to it is deleted as well.

I took the liberty of using functions that were used in previous Problem Sets in helpers.py like apology and login_required. These proved very helpful, especially login_required.

Going over the HTML templates, each of the sub-boards (music, film, fashion, etc) have their own HTML but they are nearly identical aside from a header identifying one from another.
Apology.html is self-explained and used from previous Problem Sets. Edit_bio is for editing a user's bio. Edit is explained above. Home is the first thing you see when you open the app.
Layout is the skeleton of each HTML form and is mostly lifted from previous Problem Sets. Login is for logging in. Registering is for registering. Thread is for making a thread.
Last but not least, Viewthread (which is the most complicated HTML form in my opinion) is what is used for each thread.

The only thing holding this project back is the fact that no one is using it currently lol. If I were to expand on it, maybe I would add admin roles. I never really thought that deeply about
roles and the issues that would rise up if people actually started using this forum. You're putting a lost of trust in the community without any roles.

I hope you enjoy this project, it took a lot of time to plan and program!