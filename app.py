from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    watched = db.Column(db.Boolean, default=False)


@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['POST'])
def add_movie():
    title = request.form.get('title')
    if title:
        new_movie = Movie(title=title)
        db.session.add(new_movie)
        db.session.commit()
    return render_template('movie_list.html', movies=Movie.query.all())

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    movie = Movie.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            movie.title = title
            db.session.commit()
        return render_template('movie_list.html', movies=Movie.query.all())
    return render_template('movie_form.html', movie=movie)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return render_template('movie_list.html', movies=Movie.query.all())

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_watched(id):
    movie = Movie.query.get_or_404(id)
    movie.watched = not movie.watched
    db.session.commit()
    return render_template('movie_list.html', movies=Movie.query.all())

if __name__ == '__main__':
    app.run(debug=True)
