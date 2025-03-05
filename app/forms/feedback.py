from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField, validators


class FeedbackForm(FlaskForm):
    text = TextAreaField("Your feedback", validators=[validators.InputRequired()], render_kw={"placeholder": "Input your feedback here..."})
    rating = SelectField("Rating")
    submit = SubmitField("Submit")