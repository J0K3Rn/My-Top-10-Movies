# My-Top-10-Movies

Flask-Bootstrap website that shows my top 10 list of movies. Utilizes TheMovieDB API to acquire movie information and SQLAlchemy to communicate with the database. 

Features:
- Uses TheMovieDB API to get movie info based on name and query for matching movies
- Lists all movies in order by rating
- Ability to add, update, and delete movies
- SQL database
- Uses SQLAlchemy to communicate with database

How to run:
- Download repository
- Open downloaded repository with a command line interface
- run `pip install flask`
- run `pip install flask_bootstrap`
- run `pip install flask_wtf`
- run `pip install wtforms`
- run `pip install wtforms.validators`
- run `pip install requests`
- run `pip install jinja`
- run `pip install Flask-SQLAlchemy`
- Create an account on [The Movie DB](https://www.themoviedb.org/) 
- Get your api key from [Developer TheMovieDB](https://developer.themoviedb.org/reference/intro/authentication)
- Update MOVIE_DB_API_KEY in main.py
- run `python main.py`
- Go to `127.0.0.1:5000/` to view site

Home Page:

![alt text](https://github.com/J0K3Rn/My-Top-10-Movies/blob/main/screenshots/home_page.png?raw=true)

Card Flipped:

![alt text](https://github.com/J0K3Rn/My-Top-10-Movies/blob/main/screenshots/card_flipped.png?raw=true)

Add Movie Page:

![alt text](https://github.com/J0K3Rn/My-Top-10-Movies/blob/main/screenshots/add_movie_page.png?raw=true)

Select Movie From List:

![alt text](https://github.com/J0K3Rn/My-Top-10-Movies/blob/main/screenshots/select_movie_from_list.png?raw=true)

Update Rating Page:

![alt text](https://github.com/J0K3Rn/My-Top-10-Movies/blob/main/screenshots/update_rating_page.png?raw=true)


