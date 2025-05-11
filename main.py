import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, jsonify

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Photos(db.Model):
    __tablename__ = 'Photos'
    id = db.Column(db.Integer, nullable=False, unique=True,
                   primary_key=True, autoincrement=True)
    photo_name = db.Column(db.String(25), nullable=False)
    likes_number = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(50), nullable=False)
    hashtags = db.Column(db.String(40), nullable=False)
    effect = db.Column(db.String(25), nullable=False)

    def __init__(self, photo_name, likes_number, description, hashtags, effect):
        self.photo_name = photo_name
        self.likes_number = likes_number
        self.description = description
        self.hashtags = hashtags
        self.effect = effect


class Comments(db.Model):
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, nullable=False, unique=True,
                   primary_key=True, autoincrement=True)
    photo_src = db.Column(db.String(25), nullable=False)
    comment_text = db.Column(db.Text(), nullable=False)

    def __init__(self, photo_src, comment_text):
        self.photo_src = photo_src
        self.comment_text = comment_text


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload/photo', methods=['POST'])
def uploadPhoto():
    file = request.files['file']
    name_parts = file.filename.split('.')
    file_extention = name_parts[len(name_parts) - 1]
    last_row = db.session.query(Photos).order_by(Photos.id.desc()).filter()
    filename = name_parts[0] + str(last_row.id + 1) + '.' + file_extention
    file.save(os.path.join('static', 'img', 'photos', filename))
    description = request.form['description']
    hashtags = request.form['hashtags']
    effect = request.form['effect'] + '(' + request.form['effect-level'] + '%)'
    row = Photos(filename=filename, description=description,
                 hashtags=hashtags, effect=effect)
    db.session.add(row)
    db.session.commit()
    return render_template('index.html')


@app.route("/api/get/data", methods=["GET"])
def getData():
    users = [
        {"user": "Abc", "password": "11111111"},
        {"user": "Cba", "password": "12345678"},
    ]
    return jsonify(users)


@app.route("/api/get/photos/all", methods=["GET"])
def getAllPhotos():
    db_photos = Photos.query.all()
    photos = []
    for row in db_photos:
        photo_data = {}
        photo_data["src"] = '../static/img/photos/' + row.photo_name
        photo_data["likes"] = row.likes_number
        photo_data["effect"] = row.effect
        commentsNumber = db.session.query(
            Comments.photo_src == row.photo_name).count()
        photo_data["commentsNumber"] = commentsNumber
        photos.append(photo_data)

    return jsonify(photos)


if __name__ == "__main__":
    app.run()
