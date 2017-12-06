from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import SignupForm, LoginForm
from user import User
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate('cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopproject-f5214.firebaseio.com/ '
})


app = Flask(__name__)
Bootstrap(app)

app.secret_key = "baby123"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data

            user = User(first_name, last_name, email, password)
            user_db = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com')
            user_db.put('userInfo','userS',{
                'first_name': user.get_first_name(),
                'last_name': user.get_last_name(),
                'email': user.get_email(),
                'password': user.get_password()
            })

            session['email'] = user.email
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

fireS = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com')
result = fireS.get('userInfo','userS')
print(result)
@app.route("/login", methods=["GET", "POST"])
def login():
    if 'email' in session:
        return redirect(url_for('home'))
    form = LoginForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            if email == result['email'] and password == result['password']:
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))

    elif request.method == "GET":
        return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route("/home")
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
