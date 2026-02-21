from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = "biovote_secret"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# candidates
candidates = [
    "Isabel Conklin",
    "Conrad Fisher",
    "Jeremiah Fisher",
    "Taylor Jewel",
    "Steven Conklin"
]

votes = {c: 0 for c in candidates}

images = {
    "Isabel Conklin": "isabel.jpg",
    "Conrad Fisher": "conrad.jpg",
    "Jeremiah Fisher": "jeremiah.jpg",
    "Taylor Jewel": "taylor.jpg",
    "Steven Conklin": "steven.jpg"
}

# ✅ REALISTIC UID RANGE (better than small list)
valid_ranges = [
    (111723043001, 111723043050),
    (111723044001, 111723044050),
    (111723045001, 111723045050)
]

fingerprints = {}


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        uid = request.form.get("uid").strip()

        if not uid.isdigit():
            flash("UID must be numeric")
            return redirect(url_for("login"))

        uid_int = int(uid)

        # ✅ range validation
        valid = False
        for start, end in valid_ranges:
            if start <= uid_int <= end:
                valid = True
                break

        if not valid:
            flash("Invalid College UID")
            return redirect(url_for("login"))

        session["uid"] = uid

        if uid not in fingerprints:
            return redirect(url_for("enroll_fp"))

        return redirect(url_for("verify_fp"))

    return render_template("login.html")


# ---------------- ENROLL FP ----------------
@app.route("/enroll_fp", methods=["GET", "POST"])
def enroll_fp():

    uid = session.get("uid")
    if not uid:
        return redirect(url_for("login"))

    if request.method == "POST":
        fingerprints[uid] = True
        flash("Fingerprint enrolled successfully!")
        return redirect(url_for("verify_fp"))

    return render_template("enroll_fp.html")


# ---------------- VERIFY FP ----------------
@app.route("/verify_fp", methods=["GET", "POST"])
def verify_fp():

    uid = session.get("uid")
    if not uid:
        return redirect(url_for("login"))

    if request.method == "POST":
        if fingerprints.get(uid):
            session["verified"] = True
            return redirect(url_for("student"))
        else:
            flash("Fingerprint mismatch")

    return render_template("verify_fp.html")


# ---------------- STUDENT ----------------
@app.route("/student", methods=["GET", "POST"])
def student():

    if not session.get("verified"):
        return redirect(url_for("login"))

    if request.method == "POST":
        vote = request.form.get("vote")

        if vote in votes:
            votes[vote] += 1
            flash(f"Your vote for {vote} recorded!")

        return redirect(url_for("student"))

    return render_template("student.html", candidates=candidates, images=images)


if __name__ == "__main__":
    app.run(debug=True)