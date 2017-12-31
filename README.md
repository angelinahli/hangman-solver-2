# Hangman Solver V.2.0

Minimalist flask app built around an [old hangman solver program](url-to-my-old-repo) I wrote. Immense gratitude goes towards [Miguel Grinberg](url-to-flask-tutorial), who taught me how to create my first web app. This program was written mostly as a learning opportunity for me, so it's quite possibly somewhat buggy!

## Pages

1. index.html - landing page
2. new_game.html - refreshes each time you click on the page, allows you to play a new game of hangman against the computer
3. test_word.html - allows you to give the computer a word, after which computer will compute how difficult this word is and will tell you what percentile difficulty this word falls into out of the corpus of words the computer knows.
4. solve_word.html - given an input as a string (with some predefined char for blanks), computer will tell you the best character to guess next and the list of words that might fit into the space of this word.

## To do

### most important
* deploy the app

### optional
* add a stats page for you to see the distribution of all hangman words in my corpus (finish generate_stats page)
* add a suggestions page for you to submit words that should be added to the corpus?

## Known bugs

* Many words seem to be missing from the vocabulary (might want to pull some additional words later)
* See above to dos