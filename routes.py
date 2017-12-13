from flask import Flask, render_template, request, session, redirect, url_for, flash, g
from flask_bootstrap import Bootstrap
from forms import SignupForm, LoginForm, EditForm
from user import User, Edit
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, db
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa
import pyrebase

cred = credentials.Certificate('cred\oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopproject-f5214.firebaseio.com/ '
})

config = {
    'apiKey': "AIzaSyCHVUY5JdL1gqZx7juQQlaIAIB8R76A7ZE",
    'authDomain': "oopproject-f5214.firebaseapp.com",
    'databaseURL': "https://oopproject-f5214.firebaseio.com",
    'projectId': "oopproject-f5214",
    'storageBucket': "oopproject-f5214.appspot.com",
    'messagingSenderId': "294439860189",
    "serviceAccount": 'cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json'
  }




root = db.reference()
app = Flask(__name__)
Bootstrap(app)

app.secret_key = "baby123"


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/texttest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = True
app.config['WHOOSH_BASE']='whoosh'

db2 = SQLAlchemy(app)

class Post(db2.Model):
    __searchable__ = ['title','content']

    id = db2.Column(db2.Integer, primary_key= True)
    title = db2.Column(db2.String(100))
    content = db2.Column(db2.String(1000))

wa.whoosh_index(app,Post)

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('home'))
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:

            return render_template('signup.html', form=form)
        else:
            username = form.username.data
            email = form.email.data
            password = form.password.data
            about_me = form.about_me.data

            user = User(username, email, password, about_me)
            user_db = root.child('userInfo')
            user_db.push({
                'username' : user.get_username(),
                'email': user.get_email(),
                'password': user.get_password(),
                'about_me': about_me
            })

            session['email'] = user.email
            session['username'] = user.username
            session['about_me'] = user.about_me
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    form = LoginForm()

    if request.method == "POST":
        if form.validate() == False:
            error = 'Invalid Username or Password'
            flash(error, 'danger')
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            username = form.username.data
            password = form.password.data

            emailList = []
            usernameList = []
            passList = []

            result = root.child('userInfo').get()

            for users in result:
                emailList.append(result[users]['email'])
                usernameList.append(result[users]['username'])
                passList.append(result[users]['password'])
            attempted_email = request.form['email']
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            if attempted_email in emailList and attempted_username in usernameList and attempted_password in passList:
                session['email'] = form.email.data
                session['username'] = form.username.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login', form=form))

    elif request.method == "GET":
        return render_template("login.html", form=form)

@app.route('/user')
def user():
    if 'username' in session:
        return render_template('userProfile.html')

@app.route('/edit', methods=["GET", "POST"])
def edit():
    form = EditForm(request.form)

    if request.method == 'POST':
        userFire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com')
        allUser = userFire.get('userInfo',None)

        username = session['username']
        email = session['email']

        about_me = form.about_me.data
        password = form.password.data


        for key in allUser:
            print(allUser[key]['username'])
            if username == allUser[key]['username'] and email == allUser[key]['email']:
                userFire.put('userInfo',key,{
                'username': username,
                'email': email,
                'about_me': about_me,
                'password': password
                })
                
            return redirect(url_for('user'))
    return render_template('edit.html', form=form)



@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route("/home")
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("home.html")

@app.route('/photowall')
def upload():
    fire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')
    ref = fire.get('/Images',None)
    pictureList = []
    for key in ref:
        photoLink = ref.get(key)
        pictureList.append(photoLink)
    pictureList.reverse()
    return render_template('photodesign.html',pictureList = pictureList)

@app.route('/search')
def search():
    posts = Post.query.whoosh_search(request.args.get('query')).all()

    return render_template('search2.html', posts=posts)

@app.route("/add", methods=['GET','POST'])
def add():
    if request.method =="POST":
        post = Post(title = request.form['title'], content = request.form['content'])
        db2.session.add(post)
        db2.session.commit()

        return redirect(url_for('search'))

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)
