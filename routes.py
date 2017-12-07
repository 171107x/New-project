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
fireS = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com')

root = db.reference()
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
            user_db = root.child('userInfo')
            user_db.push({
                'first_name': user.get_first_name(),
                'last_name': user.get_last_name(),
                'email': user.get_email(),
                'password': user.get_password()
            })

            session['email'] = user.email
            session['name'] = user.first_name
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

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

            emailList = []
            passList = []

            result = root.child('userInfo').get()

            for users in result:
                emailList.append(result[users]['email'])
                passList.append(result[users]['password'])
            attempted_email = request.form['email']
            attempted_password = request.form['password']
            if attempted_email in emailList and attempted_password in passList:
                session['email'] = form.email.data
                session['name'] = result[users]['first_name']
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))

    elif request.method == "GET":
        return render_template("login.html", form=form)

@app.route('/user')
def user():
    if 'email' in session:
        return render_template('userProfile.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('index'))


@app.route("/home")
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
