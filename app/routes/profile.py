from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, logout_user

from app import app
from connection import get_db_connection


@app.get("/profile/")
@login_required
def get_profile():
	user_id = request.args.get("user_id", current_user.user_id)
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT users.username, profile.* FROM users 
		LEFT JOIN profile ON users.user_id = profile.user_id 
		WHERE users.user_id = ?""", (user_id,))
	profile = cursor.fetchone()
	conn.close()
	
	return render_template("profile.html", profile=profile,)


@app.get("/edit_profile/")
@login_required
def get_edit_profile():
	user_id = request.args.get("user_id", current_user.user_id)
	if "user_id" in request.args:
		user_id = request.args.get("user_id")
		if str(user_id) != str(current_user.user_id):
			return redirect(url_for("get_profile", user_id=user_id))
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT users.username, profile.*  FROM users 
		LEFT JOIN profile ON users.user_id = profile.user_id 
		WHERE users.user_id = ?""", (current_user.user_id,))
	profile = cursor.fetchone()
	conn.close()

	return render_template("edit_profile.html", profile=profile,
												is_owner=str(user_id) == str(current_user.user_id))


@app.post("/edit_profile/")
@login_required
def post_edit_profile():
	if "user_id" in request.form and str(request.form["user_id"]) != str(current_user.user_id):
		return redirect(url_for("get_profile"))

	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("""UPDATE users SET username = ?, WHERE user_id = ? """, 
		(request.form["username"], current_user.user_id))
	cursor.execute("SELECT * FROM profile WHERE user_id = ?", (current_user.user_id,))
	profile_exists = cursor.fetchone()

	if profile_exists:
		cursor.execute("""UPDATE profile SET photo = ?, prof_description = ? WHERE user_id = ? """, 
			(request.form["photo"], request.form["prof_description"], current_user.user_id))
	else:
		cursor.execute("""INSERT INTO profile (user_id, photo, prof_description, points) VALUES (?, ?, ?, 0)""", 
			(current_user.user_id, request.form["photo"], request.form["prof_description"]))
	
	conn.commit()
	conn.close()
	return redirect(url_for("get_profile"))


@app.route("/delete_account/", methods=['POST'])
@login_required
def delete_account():
	try:
		user_id = current_user.user_id
		conn = get_db_connection()
		cursor = conn.cursor()

		cursor.execute("PRAGMA foreign_keys = ON;")

		cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
		
		conn.commit()
		logout_user()
		flash('Your account has been successfully deleted.', 'success')
		return redirect(url_for('get_login'))
		
	except Exception as e:
		print(f"Error deleting account: {e}")
		flash('An error occurred while deleting your account.', 'error')
		return redirect(url_for('get_edit_profile'))
		
	finally:
		if 'conn' in locals():
			conn.close()