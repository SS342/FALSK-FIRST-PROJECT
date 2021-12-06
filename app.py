# python 3.10
# inst: allelleo
# python -m pip install flask
# python -m pip install flask_sqlalchemy

import flask
from flask import url_for, Flask, render_template, redirect
from flask import request as flask_request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from settings import Info

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///alelleo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
DataBase = SQLAlchemy(app)


class Article(DataBase.Model):
    id = DataBase.Column(DataBase.Integer, primary_key=True)
    title : str = DataBase.Column(DataBase.String(100), nullable=False)
    intro : str = DataBase.Column(DataBase.String(300), nullable=False)
    text : str = DataBase.Column(DataBase.Text, nullable=False)
    date  = DataBase.Column(DataBase.DateTime, default=datetime.utcnow)

    def __init__(self, title, intro, text):
        self.title = title
        self.intro = intro
        self.text = text

    def __repr__(self):
        return '<Article> %r' %self.id


class User(DataBase.Model):
    id = DataBase.Column(DataBase.Integer, primary_key=True)
    username = DataBase.Column(DataBase.String(80), unique=True)
    email = DataBase.Column(DataBase.String(120), unique=True)
    password = DataBase.Column(DataBase.String(50), nullable=False)
    

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


def login_user(username, email, password):
    try:
        user = User(username=username, email=email, password=password)
        DataBase.session.add(user)
        DataBase.session.commit()
        return redirect('/home')
    except Exception as e:
        return f"Errrrrror : {str(e)}"

def cheak_user(username, email, password):
    try:
        Users = User.query.order_by(User.id.desc()).all()
        for i  in range(len(Users)):
            if Users[i].username == username and Users[i].email == email and Users[i].password == password:
                return True
    except Exception as e:
        print(str(e))
        return False

@app.route('/')
@app.route('/home')
def index() -> Info().HTML_PAGE:
    return render_template('home.html')


@app.route('/about')
def about()  -> Info().HTML_PAGE:
    return render_template('about.html')


@app.route('/user/<string:name>/<int:id>')
def user(name : str, id : int):
    return name + " " + str(id) 


@app.route('/create-article', methods = ['POST' , 'GET'])
def create_article()  -> Info().HTML_PAGE:
    if flask_request.method == 'POST':
        
        article = Article(title=flask_request.form['title'], intro=flask_request.form['intro'], text=flask_request.form['text'])

        try:
            DataBase.session.add(article)
            DataBase.session.commit()
            return redirect('/posts')
        except:
            return "Error!"
    else:
        return render_template('create-article.html')


@app.route('/posts')
def posts()  -> Info().HTML_PAGE:
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
     article = Article.query.get(id)
     return render_template('post-detail.html', article=article)


@app.route('/enter', methods = ['POST' , 'GET'])
def enter()  -> Info().HTML_PAGE:
    if flask_request.method == 'POST':
        username = flask_request.form["name"]
        email = flask_request.form["email"]
        password = flask_request.form["password"]
        if cheak_user(username, email, password):
            return redirect('/home')
        else:
            login_user(username, email, password)
            
        return redirect('/home')
    else:
        return render_template('enter.html')


def register(): pass


if __name__ == "__main__":
    app.run(debug=True)