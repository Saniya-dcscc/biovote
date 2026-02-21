from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "biovote_secret"

# folder for candidate images
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

# store votes (temporary)
votes = {c: 0 for c in candidates}

# store image filenames
images = {
    "Isabel Conklin": "isabel.jpg",
    "Conrad Fisher": "conrad.jpg",
    "Jeremiah Fisher": "jeremiah.jpg",
    "Taylor Jewel": "taylor.jpg",
    "Steven Conklin": "steven.jpg"
}


@app.route("/student", methods=["GET", "POST"])
def student():

    if request.method == "POST":
        vote = request.form.get("vote")

        if vote in votes:
            votes[vote] += 1
            flash(f"✅ Your vote for {vote} has been recorded!")

        return redirect(url_for("student"))

    return render_template("student.html", candidates=candidates, images=images)


@app.route("/")
def home():
    return redirect(url_for("student"))


if __name__ == "__main__":
    app.run(debug=True)