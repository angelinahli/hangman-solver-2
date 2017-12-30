import flask

from app import app
from app.forms import *
from programs.hangman import *

# initialize game
game = InteractiveHangman()

@app.route("/")
@app.route("/index")
def index():
    return flask.render_template("index.html", title="Home")

@app.route("/new_game", methods=["GET", "POST"])
def new_game():
    
    form = GuessForm()
    if form.validate_on_submit():
        game.guess_char(form.guess.data)
    else:
        game.errors = [] # reset errors
    
    return flask.render_template("new_game.html", 
        title="New Game", 
        game=game, 
        form=form)