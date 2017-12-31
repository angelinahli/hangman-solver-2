# Hangman Solver V.2.0

[Here's a link to the app](https://hangman-solver.herokuapp.com).

Minimalist flask app built around an [old hangman solver program](https://github.com/angelinahli/hangman-solver) I wrote. Immense gratitude goes towards [Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world), who taught me how to create my first web app. Also thanks to [this page](https://progblog.io/How-to-deploy-a-Flask-App-to-Heroku/) which taught me how to deploy my app to herokuapp.

This program was written quickly and mostly as a learning opportunity for me, so it's quite possibly buggy!

## Pages

1. index.html - landing page
2. test_word.html - allows you to give the computer a word, after which computer will compute how difficult this word is and will tell you what percentile difficulty this word falls into out of the corpus of words the computer knows.
3. solve_word.html - given an input as a string (with some predefined char for blanks), computer will tell you the best character to guess next and the list of words that might fit into the space of this word.

## To do

### most important

### optional
* add a stats page for you to see the distribution of all hangman words in my corpus (finish generate_stats page)
* add a suggestions page for you to submit words that should be added to the corpus?

## Known bugs
* The hangman game can't accomodate multiple users at the same time :(
* The hangman game sometimes switches games. I'll handle this later.
* I'm not sure how to handle the config.py file. I should figure that out in time for the next app!
* Many words seem to be missing from the vocabulary (might want to pull some additional words later)