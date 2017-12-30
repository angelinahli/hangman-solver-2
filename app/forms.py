from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class GuessForm(FlaskForm):
    guess = StringField("guess", validators=[DataRequired()])
    submit = SubmitField("submit guess")

class SolverForm(FlaskForm):
    word = StringField("guess", validators=[DataRequired()])
    wrong_chars = StringField("wrong_chars")
    submit = SubmitField("enter")