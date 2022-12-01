from flask import Flask, render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:0798@localhost/CourseProject'

db = SQLAlchemy(app)


answer = ''
sides = [1, 2]
name1 = ''
name2 = ''
allscores = []
savedscore = 0

playeranswer = random.randrange(1, 100)
otheranswer = random.randrange(1, 100)

score = 0


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

    def __repr__(self):
        return ('Name:  ' + str(self.name) + ' |   Score:  ' + str(self.score))


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class GuessForm(FlaskForm):
    guess = SelectField('Left or Right?', id='guess', choices=[(name1, name1), (name2, name2)],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    global score
    global playeranswer
    playeranswer = random.randrange(1, 100)  # Randomizes correct answer
    score = 0                       # Resets score whenever this page is visited
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('game'))
    return render_template('index.html', form=form, name=session.get('name'), score=score)


app.add_url_rule('/', 'index', index)


@app.route('/game', methods=['GET', 'POST'])
def game():
    global score
    global otheranswer
    global playeranswer
    otheranswer = random.randrange(1, 100)  # Sets the incorrect answer to a random value
    currentanswer = playeranswer
    tag = Tag.query.get(currentanswer)
    if otheranswer == currentanswer:  # If the incorrect answer matches the correct answer,
        while otheranswer == currentanswer:  # get another random value for the incorrect answer
            otheranswer = random.randrange(1, 100)
    answerside = random.choice(sides)  # Randomly sets the correct answer to be either the top or bottom selection
    if answerside == 1:                # in the form
        name1 = Name.query.get(currentanswer)
        name2 = Name.query.get(otheranswer)
    elif answerside == 2:
        name2 = Name.query.get(currentanswer)
        name1 = Name.query.get(otheranswer)
    form = GuessForm()
    if request.method == 'POST':
        session['guess'] = form.guess.data
        return redirect(url_for('result'))
    return render_template('game.html', form=form, guess=session.get('guess'), name1=name1, name2=name2, tag=tag,
                           score=score)


@app.route('/result', methods=['GET', 'POST'])
def result():
    global score
    global savedscore
    global playeranswer
    if str(session['guess']) == str(Name.query.get(playeranswer)): # Checks to see if the chosen option matches
        score += 1                                                 # the correct answer
        playeranswer = random.randrange(1, 100)
        return render_template('resultcorrect.html', score=score)
    else:
        player = Score(name=session['name'], score=score)
        db.session.add(player)
        db.session.commit()
        savedscore = score
        return redirect(url_for('gameover'))


@app.route('/gameover')
def gameover():

    return render_template('result.html', score=score)


@app.route('/scores')
def scores():
    global savedscore
    db.update(Score)
    allscores = []
    for i in range(Score.query.count() + 1):
            if Score.query.get(i) != None:
                allscores.append(str(Score.query.get(i)))
    scorelist = allscores
    scorelist = sorted(scorelist, reverse=True, key=lambda x: x[-3:])

    return render_template('scores.html', scorelist=scorelist, player=player)


if __name__ == '__main__':
    app.run()
