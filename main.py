from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
SECRET_KEY = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)
Bootstrap(app)


MOVIE_DB_API_KEY = <UPDATE ME>
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(1000), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")


class EditRatingForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


class AddMovieForm(FlaskForm):
    movie_title = StringField("Movie Title")
    submit = SubmitField("Add Movie")


#db.session.add(new_movie)
#db.create_all()
db.session.commit()
all_movies = db.session.query(Movie).all()
print(all_movies)


@app.route("/")
def home():
    global all_movies
    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route('/add', methods=["GET", "POST"])
def add_movie():
    add_form = AddMovieForm()
    if add_form.validate_on_submit():
        movie_title = add_form.movie_title.data
        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)
    return render_template("add.html", form=add_form)


@app.route('/select', methods=["GET", "POST"])
def select_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": MOVIE_DB_API_KEY})
        data = response.json()
        print(data)
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        global all_movies
        all_movies = db.session.query(Movie).all()
        return redirect(url_for('update_rating', id=new_movie.id))


@app.route("/update", methods=["GET", "POST"])
def update_rating():
    rating_form = EditRatingForm()
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    if rating_form.validate_on_submit():
        movie.rating = float(rating_form.rating.data)
        movie.review = rating_form.review.data
        db.session.commit()
        global all_movies
        all_movies = db.session.query(Movie).all()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=rating_form)


@app.route('/delete')
def delete_movie():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    global all_movies
    all_movies = db.session.query(Movie).all()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
