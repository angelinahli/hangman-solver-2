import flask

from app import app
from app.forms import *
from programs.hangman import *
from programs.solver import *

# initialize game of hangman for the user
@app.route("/")
@app.route("/index")
def index():
    return flask.render_template("index.html", 
        title="Home")

@app.route("/new_game", methods=["GET", "POST"])
def new_game():
    global game # I'm not sure if this is the best way to do it?
    if flask.request.method == "GET":
        game = InteractiveHangman()

    form = GuessForm()
    if form.validate_on_submit():
        game.guess_char(form.guess.data)
    else:
        game.errors = [] # reset errors
    return flask.render_template("new_game.html", 
        title="New Game", 
        game=game, 
        form=form)

@app.route("/solve_word", methods=["GET", "POST"])
def solve_word():
    form = SolverForm()
    solver = InteractiveSolver()
    if form.validate_on_submit():
        solver.solve(form.word.data, form.wrong_chars.data)
    return flask.render_template("solve_word.html",
        title="Solve Word",
        solver=solver,
        form=form)

@app.route("/test_word", methods=["GET", "POST"])
def test_word():
    form = TestForm()
    simulator = SimulateHangman()
    if form.validate_on_submit():
        simulator.simulate(form.word.data)
    return flask.render_template("test_word.html",
        title="Test Word",
        simulator=simulator,
        form=form)