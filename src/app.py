from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import extras

app = Flask(__name__)

# Yhteys tietokantaan
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="salasana",
        cursor_factory=psycopg2.extras.DictCursor
    )
    return conn

#Tässä toi landing page lista jossa lähteet jne
@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM articles ORDER BY id")
    authors = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", authors=authors)

#Täällä voi lisätä lähteitä
@app.route("/add_article", methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        nimi = request.form["name"]
        title = request.form["title"]
        year = request.form.get("year")
        pages = request.form.get("pages")
        url = request.form.get("url")
        notes = request.form.get("notes")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO articles (name, title, year, pages, url, notes)
                    VALUES (%s, %s, %s, %s, %s, %s)
              
            """, (nimi, title, year, pages, url, notes))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add_article.html")

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        nimi = request.form["name"]
        title = request.form["title"]
        year = request.form.get("year")
        publisher = request.form.get("publisher")
        pages = request.form.get("pages")
        notes = request.form.get("notes")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO books (name, title, year, publisher, pages, notes)
                    VALUES (%s, %s, %s, %s, %s, %s)
              
            """, (nimi, title, year, publisher, pages, notes))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add_book.html")

@app.route("/add_inproceedings", methods=["GET", "POST"])
def add_inproceedings():
    if request.method == "POST":
        nimi = request.form["name"]
        title = request.form["title"]
        booktitle = request.form.get("booktitle")
        year = request.form.get("year")
        publisher = request.form.get("publisher")
        pages = request.form.get("pages")
        notes = request.form.get("notes")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO inproceedings (name, title, booktitle, year, publisher, pages, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
              
            """, (nimi, title, booktitle, year, publisher, pages, notes))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add_inproceedings.html")

@app.route("/add_misc", methods=["GET", "POST"])
def add_misc():
    if request.method == "POST":
        nimi = request.form["name"]
        title = request.form["title"]
        year = request.form.get("year")
        url = request.form.get("url")
        notes = request.form.get("notes")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO miscs (name, title, year, url, notes)
                    VALUES (%s, %s, %s, %s, %s)
              
            """, (nimi, title, year, url, notes))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add_misc.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
    
