# Hangman Solver V.2.0

Minimalist flask app built around an [old hangman solver program](url-to-my-old-repo) I wrote. Immense gratitude goes towards [Miguel Grinberg](url-to-flask-tutorial), who taught me step by step how to create my first web app.

## Pages
1. index.html - landing page
2. new_game.html - refreshes each time you click on the page, allows you to play a new game of hangman against the computer
3. check_word.html - allows you to give the computer a word, after which computer will compute how difficult this word is and will tell you what percentile difficulty this word falls into out of the corpus of words the computer knows.
4. solver.html - given an input as a string (with some predefined char for blanks), computer will tell you the best character to guess next and the list of words that might fit into the space of this word.
5. stats.html - display some stats about which words do better on hangman overall.

## To do
* modify new_game.html to play a new game each time you refresh
* modify new_game.html to include a hangman graphic and standardize the number of lives you have.
* modify index.html to include more information about this game and the rules of hangman.