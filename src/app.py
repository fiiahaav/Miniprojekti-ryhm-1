import os
import io

from flask import Flask, render_template, request, redirect, url_for, send_file
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

@app.route("/download_bibtex_article/<int:id>")
def download_bibtex_article(id):
    """Download single article as BibTeX"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM articles WHERE id = %s", (id,))
    article = cur.fetchone()
    cur.close()
    conn.close()
    
    if not article:
        return "Article not found", 404
    
    bibtex_content = f"""@article{{article_{article['id']},
    author = {{{article['author']}}},
    title = {{{article['title']}}},
    journal = {{{article['journal']}}},
    year = {{{article['year']}}}"""
    
    if article.get('month'):
        bibtex_content += f",\n  month = {{{article['month']}}}"
    if article.get('volume'):
        bibtex_content += f",\n  volume = {{{article['volume']}}}"
    if article.get('number'):
        bibtex_content += f",\n  number = {{{article['number']}}}"
    if article.get('pages'):
        bibtex_content += f",\n  pages = {{{article['pages']}}}"
    if article.get('notes'):
        bibtex_content += f",\n  note = {{{article['notes']}}}"
    
    bibtex_content += "\n}\n"
    
    filename = f"article_{article['id']}.bib"
    return send_file(
        io.BytesIO(bibtex_content.encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name=filename
    )

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

@app.route("/download_bibtex_book/<int:id>")
def download_bibtex_book(id):
    """Download single book as BibTeX"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cur.fetchone()
    cur.close()
    conn.close()
    
    if not book:
        return "Book not found", 404
    
    bibtex_content = f"""@book{{book_{book['id']},
    author = {{{book['author']}}},
    title = {{{book['title']}}},
    publisher = {{{book['publisher']}}},
    year = {{{book['year']}}}"""
    
    if book.get('editor'):
        bibtex_content += f",\n  editor = {{{book['editor']}}}"
    if book.get('month'):
        bibtex_content += f",\n  month = {{{book['month']}}}"
    if book.get('volume'):
        bibtex_content += f",\n  volume = {{{book['volume']}}}"
    if book.get('number'):
        bibtex_content += f",\n  number = {{{book['number']}}}"
    if book.get('pages'):
        bibtex_content += f",\n  pages = {{{book['pages']}}}"
    if book.get('notes'):
        bibtex_content += f",\n  note = {{{book['notes']}}}"
    
    bibtex_content += "\n}\n"
    
    filename = f"book_{book['id']}.bib"
    return send_file(
        io.BytesIO(bibtex_content.encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name=filename
    )

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

@app.route("/download_bibtex_inproceedings/<int:id>")
def download_bibtex_inproceedings(id):
    """Download single inproceedings as BibTeX"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM inproceedings WHERE id = %s", (id,))
    inproc = cur.fetchone()
    cur.close()
    conn.close()
    
    if not inproc:
        return "Inproceedings not found", 404
    
    bibtex_content = f"""@inproceedings{{inproceedings_{inproc['id']},
  author = {{{inproc['author']}}},
  title = {{{inproc['title']}}}"""
    
    if inproc.get('year'):
        bibtex_content += f",\n  year = {{{inproc['year']}}}"
    if inproc.get('booktitle'):
        bibtex_content += f",\n  booktitle = {{{inproc['booktitle']}}}"
    if inproc.get('month'):
        bibtex_content += f",\n  month = {{{inproc['month']}}}"
    if inproc.get('editor'):
        bibtex_content += f",\n  editor = {{{inproc['editor']}}}"
    if inproc.get('volume'):
        bibtex_content += f",\n  volume = {{{inproc['volume']}}}"
    if inproc.get('number'):
        bibtex_content += f",\n  number = {{{inproc['number']}}}"
    if inproc.get('series'):
        bibtex_content += f",\n  series = {{{inproc['series']}}}"
    if inproc.get('pages'):
        bibtex_content += f",\n  pages = {{{inproc['pages']}}}"
    if inproc.get('address'):
        bibtex_content += f",\n  address = {{{inproc['address']}}}"
    if inproc.get('organization'):
        bibtex_content += f",\n  organization = {{{inproc['organization']}}}"
    if inproc.get('publisher'):
        bibtex_content += f",\n  publisher = {{{inproc['publisher']}}}"
    if inproc.get('notes'):
        bibtex_content += f",\n  note = {{{inproc['notes']}}}"
    
    bibtex_content += "\n}\n"
    
    filename = f"inproceedings_{inproc['id']}.bib"
    return send_file(
        io.BytesIO(bibtex_content.encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name=filename
    )

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

@app.route("/download_bibtex_misc/<int:id>")
def download_bibtex_misc(id):
    """Download single misc as BibTeX"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM miscs WHERE id = %s", (id,))
    misc = cur.fetchone()
    cur.close()
    conn.close()
    
    if not misc:
        return "Misc not found", 404
    
    bibtex_content = f"""@misc{{misc_{misc['id']},
    author = {{{misc['author']}}},
    title = {{{misc['title']}}},
    year = {{{misc['year']}}}"""
    
    if misc.get('month'):
        bibtex_content += f",\n  month = {{{misc['month']}}}"
    if misc.get('url'):
        bibtex_content += f",\n  howpublished = {{\\url{{{misc['url']}}}}}"
    if misc.get('notes'):
        bibtex_content += f",\n  note = {{{misc['notes']}}}"
    
    bibtex_content += "\n}\n"
    
    filename = f"misc_{misc['id']}.bib"
    return send_file(
        io.BytesIO(bibtex_content.encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name=filename
    )

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
