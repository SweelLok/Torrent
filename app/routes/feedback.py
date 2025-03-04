from flask import render_template, request, session, redirect, url_for, jsonify
from app import app
from connection import get_db_connection
from app.forms import FeedbackForm


@app.get("/feedback/")
def get_feedback():
    form = FeedbackForm()
    form.rating.choices = [(1, "Negative"), (2, "Positive")]
    connection = get_db_connection()
    feedback = connection.execute(
        "SELECT * FROM feedback").fetchall()
    connection.close()

    return render_template("feedback.html", form=form, feedback=feedback)

@app.post("/feedback/")
def post_add_feedback():
    form = FeedbackForm()
    form.rating.choices = [(1, "Negative"), (2, "Positive")]
    
    if form.validate_on_submit():
        connection = get_db_connection()
        connection.execute(
            "INSERT INTO feedback (text, rating) VALUES (?, ?)",
            (form.text.data, form.rating.data))
        connection.commit()
        connection.close()
    
    return redirect(url_for("get_feedback"))