from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def survey():

    if request.method == "POST":

        name = request.form["name"]
        rating = request.form["rating"]
        improvement = request.form["improvement"]
        new_service = request.form["new_service"]

        conn = sqlite3.connect("survey.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO feedback (name, rating, improvement, new_service)
        VALUES (?, ?, ?, ?)
        """, (name, rating, improvement, new_service))

        conn.commit()
        conn.close()

        return render_template(
            "survey.html",
            success=True
        )

    return render_template(
        "survey.html",
        success=False
    )


@app.route("/admin")
def admin():

    conn = sqlite3.connect("survey.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM feedback")
    responses = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        responses=responses
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)