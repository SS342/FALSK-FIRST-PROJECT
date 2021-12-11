# python 3.10
# inst: allelleo
# Добавить шаблон Base.html - have
# Подключить стиили Bootstrap - have
# добавтить создание статей для админа
# протестировать добовление видео - have 
# создать базу данных со статьями и коментариями - have
# создание блога - no!
# pages ^ home - have
#         home/admin - have 
#         home/admin/create-blog-post - nooo
#         home/admin/create-course
#         blog-all-post - noo
#         blog/article/<int:id>
#         course-all-post
#         course/article/<int:id>

         
import flask
from flask import Flask, render_template
from flask import request as flask_request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///allelleo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Admins(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name : str = db.Column(db.String(150), nullable=False)
    email : str = db.Column(db.String(100), nullable=False)
    password : str = db.Column(db.String(35), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    
    def __repr__(self):
        return '<User %r>' % self.id


class Courses(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name : str = db.Column(db.String(150), nullable=False)
    intro : str = db.Column(db.String(200), nullable=False)
    article : str = db.Column(db.Text(), nullable=False)
    URL : str = db.Column(db.String(500), nullable=True)
    Home_work : str = db.Column(db.Text(), nullable=True)

    def __init__(self, name, intro, article, URL=None, Home_work=None):
        self.name = name
        self.intro = intro
        self.article = article
        self.URL = URL
        self.Home_work = Home_work
    
    def __repr__(self):
        return '<User %r>' % self.id

HTML_PAGE = str

def user_is_admin(name, email, password):
    ADMS = Admins.query.order_by(Admins.id.desc()).all()
    for admin in ADMS:
        if admin.name == name and admin.email == email and admin.password == password:
            return True
        else:
            return False

@app.route('/')
@app.route('/home')
def home() -> HTML_PAGE:
    return render_template("home.html") 


@app.route('/blog')
def blog() -> HTML_PAGE:
    return render_template("blog.html")


@app.route('/home/admin')
def admin_enter() -> HTML_PAGE:
    return render_template("admin.html")


# home/admin/allelleo/swipe2005ov@gmail.com/allelleo3425
@app.route("/home/admin/<string:name>/<string:email>/<string:password>")
def admin(name, email, password) -> HTML_PAGE:
    if user_is_admin(name=name, email=email, password=password):
         return render_template("admin-panel.html", name=name, email=email, password=password)
    else:
        return render_template("except.html", except_message="Вы не администратор")


@app.route("/home/admin/<string:name>/<string:email>/<string:password>/create-article-post")
def create_article_post(name, email, password) -> HTML_PAGE:
    if user_is_admin(name=name, email=email, password=password):
        return render_template("create-article-post.html", name=name, email=email, password=password)
    else:
        return render_template("except.html", except_message="Вы не администратор")


if __name__ == "__main__":
    app.run(debug=True)