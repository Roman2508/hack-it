import os
from flask import Flask, request
from datetime import datetime
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db = SQLAlchemy(app)


class Administrator(db.Model):
    __tablename__ = 'administrator'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(2000), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    continent = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.Date(), default=datetime.utcnow)

    def __init__(self, title, text, image, continent):
        self.title = title
        self.text = text
        self.image = image
        self.continent = continent


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Articles')
def Articles():
    articles = Post.query.all()
    return render_template('articles.html', articles=articles)


@app.route('/details/<id>')
def details(id):
    article = Post.query.filter_by(id=id).first()
    return render_template('details.html', article=article)


@app.route('/admin', methods=['GET'])
def Admin():
    message = 'Enter your login and password.'
    return render_template('login.html', message=message)


@app.route('/admin', methods=['POST'])
def Admin_login():
    login = request.form['login']
    password = request.form['password']

    if Administrator.query.filter_by(login=login).all() == []:
        message = 'Enter correct login!'
        return render_template('login.html', message=message)
    else:
        if Administrator.query.filter_by(password=password).all() == []:
            message = 'Enter correct password!'
            return render_template('login.html', message=message)
        else:
            return render_template('add_article.html')


@app.route('/add_post', methods=['GET'])
def post():
    return render_template('add_article.html')


@app.route('/add_post', methods=['POST'])
def create_post():
    title = request.form['title']
    text = request.form['text']
    URL = request.form['URL']
    continent = request.form['continent']
    row = Post(title, text, URL, continent)
    db.session.add(row)
    db.session.commit()
    return render_template('add_article.html')


@app.route('/<username>')
def show_user_profile(username):
    return render_template('index.html', user_name=username)


@app.route('/interesting-places')
def interestingРlaces():
    places = [
        {
            'title': 'How to avoid expensive travel mistakes',
            'picture': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTZZmFri1SqpGb2NUO7Yi6NpLjdQn5jMM21g&s',
            'description': 'Editorial Foreword The World Travel Guide (WTG) is the flagship digital consumer brand within the Columbus'
        },
        {
            'title': 'Top 5 places to experience supernatural forces',
            'picture': 'https://www.worldtravelguide.net/wp-content/uploads/2020/05/shu-Iceland-Eldhraun-lava-field-294526091-430x246-1.jpg',
            'description': 'Editorial Foreword The World Travel Guide (WTG) is the flagship digital consumer brand within the Columbus'
        },
        {
            'title': 'Three wonderfully bizarre Mexican festivals',
            'picture': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_cFCNnQr_qvSaXNwUXVMUGKkP4Ws2cZ1Rkg&s',
            'description': 'Editorial Foreword The World Travel Guide (WTG) is the flagship digital consumer brand within the Columbus'
        },
        {
            'title': 'The 20 greenest destinations on Earth',
            'picture': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqs-6hKntBwWVt8lWgFkLAv5tS_jCWYhzD8g&s',
            'description': 'Editorial Foreword The World Travel Guide (WTG) is the flagship digital consumer brand within the Columbus'
        },
        {
            'title': 'How to survive on a desert island',
            'picture': 'https://www.desertislandsurvival.com/wp-content/uploads/2023/03/friction.jpg',
            'description': 'Editorial Foreword The World Travel Guide (WTG) is the flagship digital consumer brand within the Columbus'
        },
    ]

    return render_template('interesting-places.html', places=places)


if __name__ == '__main__':
    app.run()
