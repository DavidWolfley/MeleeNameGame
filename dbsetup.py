from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:0798@localhost/CourseProject'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app, db)
    return app




class Name(db.Model):
    __tablename__ = 'names'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return self.full_name

    tags = db.relationship('Tag', secondary='players', backref=db.backref('name', uselist=False))


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return self.tag


class Player(db.Model):
    __tablename__ = 'players'
    name_id = db.Column(db.Integer, db.ForeignKey('names.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        return self.name_id


class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    score = db.Column(db.Integer)


with app.app_context():
    db.create_all()
    with open('names.csv', newline='') as names:
        namereader = csv.reader(names)
        for i in names:
            currentname = Name(full_name=i)
            db.session.add(currentname)
        db.session.commit()
        names.close()

    with open('tags.csv', newline='') as tags:
        tagreader = csv.reader(tags)
        for i in tags:
            currenttag = Tag(tag=i)
            db.session.add(currenttag)
        db.session.commit()
        names.close()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Name=Name, Tag=Tag, Player=Player, Score=Score)


if __name__ == '__main__':
    app.run()
