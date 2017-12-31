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