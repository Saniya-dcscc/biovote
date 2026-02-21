from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = "biovote_secret"

# Fake fingerprint database (UID → fingerprint registered)
fingerprints = {}

# Candidate images
images = {
    "Isabel Conklin": "isabel.jpg",
    "Conrad Fisher": "conrad.jpg",
    "Jeremiah Fisher": "jeremiah.jpg",
    "Taylor Jewel": "taylor.jpg",
    "Steven Conklin": "steven.jpg"
}

votes = {}

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uid = request.form.get("uid")

        if not uid:
            flash("Enter UID")
            return redirect(url_for("login"))

        session["uid"] = uid

        # If fingerprint not registered → go register
        if uid not in fingerprints:
            return redirect(url_for("register_fingerprint"))

        # else go scan
        return redirect(url_for("scan_fingerprint"))

    return render_template("login.html")


# ================= REGISTER FINGERPRINT =================
@app.route("/register_fp", methods=["GET", "POST"])
def register_fingerprint():
    if "uid" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        uid = session["uid"]
        fingerprints[uid] = True
        flash("Fingerprint registered successfully")
        return redirect(url_for("scan_fingerprint"))

    return render_template("register_fp.html")


# ================= SCAN FINGERPRINT =================
@app.route("/scan_fp", methods=["GET", "POST"])
def scan_fingerprint():
    if "uid" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        return redirect(url_for("student"))

    return render_template("scan_fp.html")


# ================= STUDENT VOTING =================
@app.route("/student", methods=["GET", "POST"])
def student():
    if "uid" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        candidate = request.form.get("vote")

        if session["uid"] in votes:
            flash("You already voted")
        else:
            votes[session["uid"]] = candidate
            flash(f"Vote recorded for {candidate}")

    return render_template("student.html", images=images)


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)