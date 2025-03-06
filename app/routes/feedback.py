from flask import render_template, redirect, url_for, session
from flask_login import login_required

from app import app
from connection import get_db_connection
from app.forms import FeedbackForm


@app.get("/feedback/")
@login_required
def get_feedback():
    form = FeedbackForm()
    form.rating.choices = [(1, "Negative"), (2, "Positive")]
    connection = get_db_connection()
    
    feedback = connection.execute(
        "SELECT f.feedback_id, f.text, f.rating, u.username FROM feedback f "
        "JOIN users u ON f.user_id = u.user_id"
    ).fetchall()
    
    connection.close()
    return render_template("feedback.html", form=form, feedbacks=feedback)

@app.post("/feedback/")
def post_add_feedback():
    form = FeedbackForm()
    form.rating.choices = [(1, "Negative"), (2, "Positive")]

    if form.validate_on_submit():
        user_id = session.get("user_id")

        if user_id:
            connection = get_db_connection()
            connection.execute(
                "INSERT INTO feedback (user_id, text, rating) VALUES (?, ?, ?)",
                (user_id, form.text.data, form.rating.data)
            )
            connection.commit()
            connection.close()
    
    return redirect(url_for("get_feedback"))

@app.post("/feedback/<int:feedback_id>/delete")
def post_delete_feedback(feedback_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM feedback WHERE feedback_id = ?", (feedback_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("get_admin"))