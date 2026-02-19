from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "cloudbiovote_secret_key"
app.config["SESSION_PERMANENT"] = False

# Temporary storage (testing only)
users = {}

# ✅ Valid UID ranges
valid_ranges = [
    (111723043001, 111723043050),
    (111723044001, 111723044050),
    (111723045001, 111723045050),
    (111723046001, 111723046050),
    (111723047001, 111723047050),
]


def is_valid_uid(uid):
    try:
        uid_number = int(uid)
    except:
        return False

    for start, end in valid_ranges:
        if start <= uid_number <= end:
            return True
    return False


@app.route("/")
def home():
    return redirect(url_for("login"))


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uid = request.form.get("uid", "").strip()
        credential = request.form.get("credential", "").strip()

        if not uid or not credential:
            return "Please fill all fields"

        if not is_valid_uid(uid):
            return "Invalid UID. Not in allowed student range."

        if uid in users:
            return "UID already registered."

        users[uid] = credential
        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uid = request.form.get("uid", "").strip()
        credential = request.form.get("credential", "").strip()

        if uid in users and users[uid] == credential:
            session["uid"] = uid
            return redirect(url_for("dashboard"))
        else:
            return "Invalid UID or Credential."

    return render_template("index.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "uid" not in session:
        return redirect(url_for("login"))

    # Temporary vote results (for chart demo)
    results = {
        "Candidate A": 5,
        "Candidate B": 3,
        "Candidate C": 8
    }

    return render_template(
        "dashboard.html",
        faculty="Faculty Panel",
        results=results
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("uid", None)
    return redirect(url_for("login"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
