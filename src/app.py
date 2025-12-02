import os

from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

from util import to_int

app = Flask(__name__)

load_dotenv()

# Yhteys tietokantaan
def get_db_connection():
    url = os.getenv("DATABASE_URL")
    dsn = url.replace("postgresql+psycopg2://", "postgresql://")
    return psycopg2.connect(dsn, cursor_factory=extras.DictCursor)

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
        month = to_int(request.form.get("month"))
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


@app.route("/edit_article/<int:id>", methods=["GET", "POST"])
def edit_article(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM articles WHERE id = %s", (id,))
    article = cur.fetchone()

    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        journal = request.form["journal"]
        year = request.form["year"]
        month = to_int(request.form.get("month"))
        volume = request.form.get("volume")
        number = request.form.get("number")
        pages = request.form.get("pages")
        notes = request.form.get("notes")

        cur.execute("""
            UPDATE articles
            SET author = %s, title = %s, journal = %s,
                year = %s, month = %s, volume = %s,
                number = %s, pages = %s, notes = %s
            WHERE id = %s
        """, (author, title, journal, year, month,
              volume, number, pages, notes, id))

        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("edit_article.html", article=article)


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        editor = request.form["editor"]
        publisher = request.form["publisher"]
        year = request.form["year"]
        month = to_int(request.form.get("month"))
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

@app.route("/edit_book/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cur.fetchone()

    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        editor = request.form["editor"]
        publisher = request.form["publisher"]
        year = request.form["year"]
        month = to_int(request.form.get("month"))
        volume = request.form.get("volume")
        number = request.form.get("number")
        pages = request.form.get("pages")
        notes = request.form.get("notes")

        cur.execute("""
            UPDATE books
            SET author=%s, title=%s, editor=%s, publisher=%s, year=%s,
                month=%s, volume=%s, number=%s, pages=%s, notes=%s
            WHERE id=%s
        """, (author, title, editor, publisher, year, month,
            volume, number, pages, notes, id))

        conn.commit()
        return redirect(url_for("index"))

    return render_template("edit_book.html", book=book)

@app.route("/add_inproceedings", methods=["GET", "POST"])
def add_inproceedings():
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        booktitle = request.form.get("booktitle")
        year = to_int(request.form.get("year"))
        month = to_int(request.form.get("month"))
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

@app.route("/edit_inproceedings/<int:id>", methods=["GET", "POST"])
def edit_inproceedings(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM inproceedings WHERE id = %s", (id,))
    inproc = cur.fetchone()

    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        booktitle = request.form.get("booktitle")
        year = to_int(request.form.get("year"))
        month = to_int(request.form.get("month"))
        editor = request.form.get("editor")
        volume = request.form.get("volume")
        number = request.form.get("number")
        series = request.form.get("series")
        pages = request.form.get("pages")
        address = request.form.get("address")
        organization = request.form.get("organization")
        publisher = request.form.get("publisher")
        notes = request.form.get("notes")

        cur.execute("""
            UPDATE inproceedings
            SET author=%s, title=%s, booktitle=%s, year=%s, month=%s,
                editor=%s, volume=%s, number=%s, series=%s, pages=%s,
                address=%s, organization=%s, publisher=%s, notes=%s
            WHERE id=%s
        """, (author, title, booktitle, year, month, editor, volume, number,
              series, pages, address, organization, publisher, notes, id))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("index"))

    cur.close()
    conn.close()
    return render_template("edit_inproceedings.html", inproc=inproc)

@app.route("/add_misc", methods=["GET", "POST"])
def add_misc():
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        year = request.form["year"]
        month = to_int(request.form.get("month"))
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

@app.route("/edit_misc/<int:id>", methods=["GET", "POST"])
def edit_misc(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM miscs WHERE id = %s", (id,))
    misc = cur.fetchone()

    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        year = request.form["year"]
        month = to_int(request.form.get("month"))
        url = request.form.get("url")
        notes = request.form.get("notes")

        cur.execute("""
            UPDATE miscs
            SET author=%s, title=%s, year=%s, month=%s, url=%s, notes=%s
            WHERE id=%s
        """, (author, title, year, month, url, notes, id))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    cur.close()
    conn.close()
    return render_template("edit_misc.html", misc=misc)

#täällä voi hakea lähteitä tietyllä viitetyypillä
@app.route("/get_references")
def get_references_page():
    ref_type = request.args.get("type")
    query = request.args.get("query")
    year = request.args.get("year")

    references = []

    if ref_type or query or year:
        conn = get_db_connection()
        cur = conn.cursor()

        if ref_type == "articles":
            cur.execute("SELECT * FROM articles ORDER BY id DESC")
            references = cur.fetchall()
        elif ref_type == "books":
            cur.execute("SELECT * FROM books ORDER BY id DESC")
            references = cur.fetchall()
        elif ref_type == "inproceedings":
            cur.execute("SELECT * FROM inproceedings ORDER BY id DESC")
            references = cur.fetchall()
        elif ref_type == "miscs":
            cur.execute("SELECT * FROM miscs ORDER BY id DESC")
            references = cur.fetchall()
        else:
            cur.execute("SELECT * FROM articles ORDER BY id DESC")
            references.extend(cur.fetchall())
            cur.execute("SELECT * FROM books ORDER BY id DESC")
            references.extend(cur.fetchall())
            cur.execute("SELECT * FROM inproceedings ORDER BY id DESC")
            references.extend(cur.fetchall())
            cur.execute("SELECT * FROM miscs ORDER BY id DESC")
            references.extend(cur.fetchall())

        cur.close()
        conn.close()

    if year:
        references = [r for r in references if r.get("year") is not None and str (r["year"]) == year] # pylint: disable=line-too-long

    if query:
        references = [
            r for r in references
            if any(query.lower() in str(r.get(field, "")).lower()
                   for field in ["title", "author", "journal", "publisher", "booktitle", "notes"])
        ]

    return render_template(
        "get_references.html",
        references=references,
        ref_type=ref_type,
        query=query,
        year=year
    )

@app.route("/delete_article/<int:id>", methods=["POST"])
def delete_article(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM articles WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete_book/<int:id>", methods=["POST"])
def delete_book(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete_inproceedings/<int:id>", methods=["POST"])
def delete_inproceedings(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM inproceedings WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete_misc/<int:id>", methods=["POST"])
def delete_misc(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM miscs WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
