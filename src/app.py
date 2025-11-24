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
    cur.execute("SELECT * FROM articles ORDER BY id DESC")
    articles = cur.fetchall()
    cur.execute("SELECT * FROM books ORDER BY id DESC")
    books = cur.fetchall()
    cur.execute("SELECT * FROM inproceedings ORDER BY id DESC")
    inproceedings = cur.fetchall()
    cur.execute("SELECT * FROM miscs ORDER BY id DESC")
    miscs = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", articles=articles, books=books, 
                           inproceedings=inproceedings, miscs=miscs)


@app.route('/add_source', methods=['POST'])
def add_source():
    source_type = request.form['lahde']

    if source_type == "article":
        return redirect(url_for('add_article'))
    elif source_type == "book":
        return redirect(url_for('add_book'))
    elif source_type == "inproceedings":
        return redirect(url_for('add_inproceedings'))
    else:
        return redirect(url_for('add_misc'))

#Täällä voi lisätä lähteitä
@app.route("/add_article", methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        journal = request.form["journal"]
        year = request.form["year"]
        month = request.form.get("month")
        volume = request.form.get("volume")
        number = request.form.get("number")
        pages = request.form.get("pages")
        notes = request.form.get("notes")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO articles (author, title, journal, year, month,
                    volume, number, pages, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
              
            """, (author, title, journal, year, month,
                volume, number, pages, notes))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add_article.html")

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        author = request.form["name"]
        title = request.form["title"]
        editor = request.form["editor"]
        publisher = request.form["publisher"]
        year = request.form["year"]
        month = request.form.get("month")
        volume = request.form.get("volume")
        number = request.form.get("number")
        pages = request.form.get("pages")
        notes = request.form.get("notes")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO books (author, title, editor, publisher,
                    year, month, volume, number, pages, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              
            """, (author, title, editor, publisher, year, month,
                volume, number, pages, notes))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add_book.html")

@app.route("/add_inproceedings", methods=["GET", "POST"])
def add_inproceedings():
    if request.method == "POST":
        author = request.form["name"]
        title = request.form["title"]
        booktitle = request.form.get("booktitle")
        year = request.form.get("year")
        month = request.form.get("month")
        editor = request.form.get("editor")
        volume = request.form.get("volume")
        number = request.form.get("number")
        series = request.form.get("series")
        pages = request.form.get("pages")
        address = request.form.get("address")
        organization = request.form.get("organization")
        publisher = request.form.get("publisher")
        notes = request.form.get("notes")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO inproceedings (author, title, booktitle,
                    year, month, editor, volume, number, series, pages,
                    address, organization, publisher, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              
            """, (author, title, booktitle, year, month, editor, volume, number,
                  series, pages, address, organization, publisher, notes))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add_inproceedings.html")

@app.route("/add_misc", methods=["GET", "POST"])
def add_misc():
    if request.method == "POST":
        author = request.form["name"]
        title = request.form["title"]
        year = request.form["year"]
        month = request.form.get("month")
        url = request.form.get("url")
        notes = request.form.get("notes")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO miscs (author, title, year, month, url, notes)
                    VALUES (%s, %s, %s, %s, %s, %s)
              
            """, (author, title, year, month, url, notes))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add_misc.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
    
