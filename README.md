# MeleeNameGame

This application is titled “The Melee Name Game.” It is a guessing game using SQLAlchemy
and Flask. You first need a blank postgreSQL database titled “Melee”. Once you do, you then
run dbsetup.py. This creates the tables for the database and populates them with the data of the
top 100 Super Smash Bros. Melee players as of 2019. It does so by filling each table with all
values from the csv files titled “names” and “tags”. Theoretically, this means that as long as the
id values in the table correspond with each other, this can be used for any other sort of guessing
game with 1-to-1 relationships. In this case, the “names” file contains all of the real names of the
players, while the “tags” file contains all of their in-game names. After running dbsetup once,
you can now run app.py, containing the guessing game. The index page has a form where you
can enter your name, and the navbar at the top allows you to visit the leaderboard page, which
will be empty until the game is played once. Once you enter your name, you will reach a page
that gives you the “tag” of a player, and a select field with 2 options. One of those options will be
the player’s real name, the other option will be the real name of another player. If your answer is
correct, you will reach the result page telling you you’re correct, and redirecting you back to the
game, with a different name to guess. If your answer is incorrect, you will reach a different result
page with a button to return to the home page. Once you reach this game over page, your score
will be entered into the “score” table of the database, of which every entry is displayed on the
leaderboard page, and sorted up to triple digit numbers.
