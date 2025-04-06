from flask import Flask, request  # type: ignore
from flask import render_template  # type: ignore
import os
from flask_sqlalchemy import SQLAlchemy  # type: ignore

DATABASE_NAME = 'data.sqlite'
base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(base_dir, DATABASE_NAME)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db = SQLAlchemy(app)


class Administrator_data(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password


# admin = Administrator_data(login='admin', password='111111')
# db.session.add(admin)
# db.session.commit()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/<name>")
def user_index(name):
    return render_template('index.html', user_name=name)


@app.route("/articles")
def articles():
    return '<h1>Незабаром тут ви побачите наші статті</h1><p>Сторінка в розробці</p>'


@app.route("/admin")
def admin():
    return render_template('login.html')


@app.route("/discover")
def discover():
    articles = [
        'How to avoid expensive travel mistakes',
        'Top 5 places to experience supernatural forces',
        'Three wonderfully bizarre Mexican festivals',
        'The 20 greenest destinations on Earth',
        'How to survive on a desert island',
    ]

    return render_template('discover.html', articles=articles)


@app.route("/test/<username>")
def test(username):
    return f'<h1>Test page: {username}</h1>'


@app.route("/admin", methods=['GET'])
def get_admin_login():
    return render_template('login.html', message="")


@app.route("/admin", methods=["POST"])
def admin_login():
    login = request.form['login']
    password = request.form['password']

    admin_login = Administrator_data.query.filter_by(login=login).all()

    if admin_login == []:
        message = "Введіть правильний логін"
        return render_template('login.html', message=message)
    else:
        admin_password = Administrator_data.query.filter_by(
            password=password).all()
        if admin_password == []:
            message = "Введіть правильний пароль"
            return render_template('login.html', message=message)
        else:
            return render_template('add_article.html')


@app.route("/add_article", methods=['GET'])
def get_add_article_form():
    return render_template('add_article.html')


@app.route("/add_article", methods=['POST'])
def add_article():
    title = request.form['title']
    text = request.form['text']
    url = request.form['url']
    continent = request.form['continent']
    return render_template('add_article.html')

# db.create_all()


if __name__ == '__main__':
    app.run()
