from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/texttest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = True
app.config['WHOOSH_BASE']='whoosh'

db = SQLAlchemy(app)

class Post(db.Model):
    __searchable__ = ['title','content']

    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))

wa.whoosh_index(app,Post)

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('search2.html', posts = posts)

@app.route('/search')
def search():
    posts = Post.query.whoosh_search(request.args.get('query')).all()

    return render_template('search2.html', posts=posts)

@app.route("/add", methods=['GET','POST'])
def add():
    if request.method =="POST":
        post = Post(title = request.form['title'], content = request.form['content'])
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('search'))

    return render_template("add.html")

if __name__ == '__main__':
    app.run(debug=True)