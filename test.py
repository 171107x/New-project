from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import SignupForm, LoginForm
from user import User
import firebase_admin
from firebase import firebase
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

@app.route('/login', methods=["GET","POST"])
def login():
    error = ''
    form = LoginForm(request.form)
    try:
        usernameDriver=[]
        passwordDriver=[]
        usernameComm=[]
        passwordComm=[]
        if request.method == "POST":

            fireD = firebase.FirebaseApplication("https://oopp-85102.firebaseio.com/ ")
            for key in fireD.get("regDriver", None):
                fireDat = fireD.get("regDriver", key)

                usernameDriver.append( fireDat["username"])
                passwordDriver.append(fireDat["pass"])
            fireC = firebase.FirebaseApplication("https://oopp-85102.firebaseio.com/ ")
            for key in fireC.get("regComm", None):
                fireDat = fireC.get("regComm", key)

                usernameComm.append(fireDat["username"])
                passwordComm.append(fireDat["pass"])
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            # flash(attempted_username)
            # flash(attempted_password)


            if attempted_username in usernameDriver and attempted_password in passwordDriver:
                session['logged_in'] = True
                return redirect(url_for('jobs'))
            elif attempted_username in usernameComm and attempted_password in passwordComm:
                session['logged_in'] = True

                return redirect(url_for('morning_ride'))
            else:
                error = "Invalid credentials. Try Again."
            print(usernameDriver)
        return render_template("login.html", error=error,form=form)

    except Exception as e:
        # flash(e)
        return render_template("login.html", error=error,form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))