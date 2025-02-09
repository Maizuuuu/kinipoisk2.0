from flask import Flask, render_template, request
import sqlite3

app = Flask("main")
db_name = "films.db"


class Film:
    def __init__(
        self,
        id,
        title,
        year,
        genres,
        country,
        description,
        duration,
        rating,
        age_rating,
        poster,
    ):
        self.id = id
        self.title = title
        self.year = year
        self.genres = genres
        self.country = country
        self.description = description
        self.duration = duration
        self.rating = rating
        self.age_rating = age_rating
        self.poster = poster


def get_films_list(page=1, limit=25, offset=25):
    con = sqlite3.connect(db_name)
    sql = """SELECT * FROM movie
    LIMIT ? OFFSET ?"""
    q = con.execute(sql, [limit, (page - 1) * offset])
    data = q.fetchall()
    return [Film(*d) for d in data]

def search(text):
    con = sqlite3.connect(db_name)
    sql = f"""SELECT * FROM movie
    WHERE title LIKE "%{text}%" OR genres LIKE "%{text}%" OR country LIKE "%{text}%" """
    q = con.execute(sql)
    data = q.fetchall()
    return [Film(*d) for d in data]

def get_film_by_id(id):
    con = sqlite3.connect(db_name)
    sql = """SELECT * FROM movie
    WHERE id = ?"""
    q = con.execute(sql, [id])
    data = q.fetchone()
    return Film(*data)

@app.route("/")
def home():
    films = get_films_list()
    return render_template("index.html", films=films, page =1)

@app.route("/pages/<int:page>")
def pages(page):
    films = get_films_list(page)
    return render_template("index.html", films=films, page=page)


@app.route("/films/<int:id>")
def film(id):
    film = get_film_by_id(id)
    return render_template("film.html", film = film)

@app.route("/search", methods = ['POST'])
def search_page():
    form = request.form
    text = form.get("search")
    films = search(text)
    return render_template("search.html", films=films, search = text)
app.run(host="0.0.0.0", port=8080, debug=True)
