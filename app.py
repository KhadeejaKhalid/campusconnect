from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def dashboard():
    conn = get_db()
    labs = conn.execute("SELECT * FROM labs").fetchall()
    timetable = conn.execute("SELECT * FROM timetable").fetchall()
    posts = conn.execute("SELECT * FROM forum ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", labs=labs, timetable=timetable, posts=posts)

# ---------------- TIMETABLE ----------------

@app.route("/timetable", methods=["GET", "POST"])
def timetable():
    conn = get_db()
    if request.method == "POST":
        subject = request.form["subject"]
        day = request.form["day"]
        time = request.form["time"]

        conn.execute("INSERT INTO timetable (subject, day, time) VALUES (?, ?, ?)",
                     (subject, day, time))
        conn.commit()
        return redirect("/timetable")

    data = conn.execute("SELECT * FROM timetable").fetchall()
    conn.close()
    return render_template("timetable.html", timetable=data)

# ---------------- LABS ----------------

@app.route("/labs", methods=["GET", "POST"])
def labs():
    conn = get_db()
    if request.method == "POST":
        subject = request.form["subject"]
        deadline = request.form["deadline"]

        conn.execute("INSERT INTO labs (subject, deadline) VALUES (?, ?)",
                     (subject, deadline))
        conn.commit()
        return redirect("/labs")

    data = conn.execute("SELECT * FROM labs").fetchall()
    conn.close()
    return render_template("labs.html", labs=data)

# ---------------- FORUM ----------------

@app.route("/forum", methods=["GET", "POST"])
def forum():
    conn = get_db()
    if request.method == "POST":
        question = request.form["question"]
        conn.execute("INSERT INTO forum (question) VALUES (?)", (question,))
        conn.commit()
        return redirect("/forum")

    posts = conn.execute("SELECT * FROM forum ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("forum.html", posts=posts)

def init_db():
    conn = sqlite3.connect("database.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS timetable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        day TEXT NOT NULL,
        time TEXT NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS labs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        deadline TEXT NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS forum (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
