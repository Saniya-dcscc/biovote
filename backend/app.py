from flask import Flask, render_template, request, redirect, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "biovote_secret"

# ---------- UPLOAD FOLDER ----------
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------- DATA ----------
votes = {
    "Isabel Conklin": 0,
    "Conrad Fisher": 0,
    "Jeremiah Fisher": 0,
    "Taylor Jewel": 0,
    "Steven Conklin": 0
}

candidate_images = {
    "Isabel Conklin": "",
    "Conrad Fisher": "",
    "Jeremiah Fisher": "",
    "Taylor Jewel": "",
    "Steven Conklin": ""
}

valid_ranges = [
    (111723043001, 111723043050),
    (111723044001, 111723044050),
    (111723045001, 111723045050),
    (111723046001, 111723046050),
    (111723047001, 111723047050)
]

faculty_users = {
    "sage456": "sage123",
    "jett678": "jett123",
    "Phoenix890": "123",
    "Sova": "sova123"
}

# ---------- ROUTES ----------

@app.route("/", methods=["GET"])
def home():
    return render_template("login.html")


@app.route("/student_login", methods=["POST"])
def student_login():
    uid = request.form["uid"]

    try:
        uid = int(uid)
        for start, end in valid_ranges:
            if start <= uid <= end:
                session["student"] = uid
                return redirect("/student")
    except:
        pass

    return "Invalid UID"


@app.route("/faculty_login", methods=["POST"])
def faculty_login():
    user = request.form["user"]
    password = request.form["password"]

    if user in faculty_users and faculty_users[user] == password:
        session["faculty"] = user
        return redirect("/faculty")

    return "Invalid faculty login"


@app.route("/student", methods=["GET", "POST"])
def student():
    if "student" not in session:
        return redirect("/")

    if request.method == "POST":
        vote = request.form["vote"]
        votes[vote] += 1

    return render_template("student.html", votes=votes, images=candidate_images)


@app.route("/faculty")
def faculty():
    if "faculty" not in session:
        return redirect("/")

    return render_template("faculty.html", votes=votes)


@app.route("/upload", methods=["POST"])
def upload():
    if "faculty" not in session:
        return redirect("/")

    file = request.files["photo"]
    candidate = request.form["candidate"]

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        candidate_images[candidate] = filename

    return redirect("/faculty")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
