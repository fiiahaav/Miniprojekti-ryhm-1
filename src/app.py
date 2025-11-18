from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Yhteys tietokantaan
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="salasana"
    )
    return conn

#Tässä toi landing page lista jossa lähteet jne
@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM authors ORDER BY id")
    authors = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", authors=authors)

#Täällä voi lisätä lähteitä
@app.route("/add", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        nimi = request.form["name"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO authors (name) VALUES (%s)", (nimi,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    
