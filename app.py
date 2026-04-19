
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os

app = Flask(__name__)
app.secret_key = "change-me"

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        age = request.form.get("age","").strip()
        phone = request.form.get("phone","").strip()
        if not name or not age or not phone:
            flash("All fields are required.")
            return redirect(url_for("index"))
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO users(name, age, phone) VALUES (?, ?, ?)", (name, int(age), phone))
        conn.commit()
        conn.close()
        flash("Saved successfully!")
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/records")
def records():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id,name,age,phone FROM users ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return render_template("records.html", rows=rows)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
