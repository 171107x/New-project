from flask import Flask, render_template, request, session, redirect, url_for, flash, g
from flask_bootstrap import Bootstrap
from forms import SignupForm, LoginForm, EditForm, ReviewForm
from user import User, Edit, Review
from firebase import firebase
from Events import Events
from forum import Forum
import firebase_admin
from firebase_admin import credentials, db
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators
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

class eventsForm(Form):
    title = StringField('Title',[validators.Length(min=1, max=150), validators.DataRequired()])
    category = SelectField('Caterories of Events', choices=[('', 'Select'), ('BRIDAL', 'Bridal events '), ('EDUCATIONAL', 'Educational conferencing'),
                                                ('COMMEMORATIVE', 'Commemorative events'), ('CHARITY', 'Charity events')],
                           default='')
    timeStart = SelectField('Start Time', choices=[('', 'Select'), ('7:00AM', '7:00AM'), ('8:00AM', '8:00AM'),
                                               ('9:00AM', '9:00AM'), ('10:00AM', '10:00AM'),
                                               ('11:00AM', '11:00AM'), ('12:00PM', '12:00PM'),
                                               ('1:00PM', '1:00PM'), ('2:00PM', '2:00PM'), ('3:00PM', '3:00PM'),
                                               ('4:00PM', '4:00PM'), ('5:00PM', '5:00PM'), ('6:00PM', '6:00PM'),
                                               ('7:00PM', '7:00PM'), ('8:00PM', '8:00PM'), ('9:00PM', '9:00PM'),
                                               ('10:00PM', '10:00PM')], default='')
    timeEnd = SelectField('End Time', choices=[('', 'Select'), ('7:00AM', '7:00AM'), ('8:00AM', '8:00AM'),
                                               ('9:00AM', '9:00AM'), ('10:00AM', '10:00AM'),
                                               ('11:00AM', '11:00AM'), ('12:00PM', '12:00PM'),
                                               ('1:00PM', '1:00PM'), ('2:00PM', '2:00PM'), ('3:00PM', '3:00PM'),
                                               ('4:00PM', '4:00PM'), ('5:00PM', '5:00PM'), ('6:00PM', '6:00PM'),
                                               ('7:00PM', '7:00PM'), ('8:00PM', '8:00PM'), ('9:00PM', '9:00PM'),
                                               ('10:00PM', '10:00PM')], default='')
    location = StringField('Location of event',[validators.DataRequired()])
    description = TextAreaField('Description of event',[validators.DataRequired()])
    date = StringField('Date of event',[validators.DataRequired()])

class forumForm(Form):
        forumText = TextAreaField('')
        forumType = SelectField(
            choices=[('', 'Select'), ('Food', 'Food'), ('Movies', 'Movies'), ('Childcare', 'Childcare'),
                     ('Eldercare', 'Eldercare'), ('Housekeeping', 'Housekeeping')])

class ForumFilter(Form):
        forumFilter = SelectField(
            choices=[('', 'Select'), ('Food', 'Food'), ('Movies', 'Movies'), ('Childcare', 'Childcare'),
                     ('Eldercare', 'Eldercare'), ('Housekeeping', 'Housekeeping')])

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('home'))
    form = SignupForm(request.form)

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
        form = ReviewForm(request.form)
        if request.method == 'POST' and form.validate():
            title = form.title.data
            review = form.review.data

            userFire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com')
            result = userFire.get('userInfo', None)


            review = Review(title, review)
            review_db = root.child('review')
            review_db.push({
                'title' : review.get_title(),
                'review' : review.get_review(),
                'time' : review.get_date()

                    })
            return redirect(url_for('user'))
        '''
            titleList = []
            reviewList = []

            for i in result:
                if session['username'] == result[key]['username'] and session['email'] == result[key]['email']:
                    titleList.append(result[i]['title'])
                    reviewList.append(result[i]['review'])
            return redirect(url_for('user'))
        '''
        return render_template('userProfile.html', form=form)

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

@app.route('/events',methods=['GET','POST'])
def new():
    form = eventsForm(request.form)
    allE = []
    eventFire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/ ')
    allEvent = eventFire.get('Events', None)
    if request.method == 'POST' and form.validate():
            title = form.title.data
            location = form.location.data
            category = form.category.data
            timestart = form.timeStart.data
            timeend = form.timeEnd.data
            description = form.description.data
            date = form.date.data

            event = Events(title,location,category,timestart,timeend,description,date)
            # This is to make the events name +1
            try:
                count = len(allEvent) +1
            except TypeError:
                count = 1

            # Search from a certain key to print the entire key
            # for key in allEvent:
            #     if allEvent[key]['title'] == 'kenneth is hensum':
            #         print(allEvent[key])

            #If I want to get a certain key(title) from the test2 database
            # for key in allEvent:
            #     if key == 'test2':
            #         print(allEvent[key])
            #
            eventFire.put('Events','number'+str(count),{
                'title': event.get_title(),
                'location': event.get_location(),
                'category': event.get_category(),
                'timeStart': event.get_timestart(),
                'timeEnd': event.get_timeend(),
                'description': event.get_description(),
                'date': event.get_date()
            })
    try:
        for key in allEvent:
            allE.append(allEvent[key])
        allE = reversed(allE)
    except TypeError:
        allE = []

    return render_template('showEvent.html', form=form, allE=allE)

@app.route('/createEvent',methods=['POST','GET'])
def create_forum():
    form = eventsForm(request.form)
    allE = []
    eventFire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/ ')
    allEvent = eventFire.get('Events', None)
    if request.method == 'POST':
        title = form.title.data
        location = form.location.data
        category = form.category.data
        timestart = form.timeStart.data
        timeend = form.timeEnd.data
        description = form.description.data
        date = form.date.data

        event = Events(title, location, category, timestart, timeend, description, date)

        try:
            count = len(allEvent) + 1
        except TypeError:
            count = 1

        eventFire.put('Events', 'number'+str(count), {
            'title': event.get_title(),
            'location': event.get_location(),
            'category': event.get_category(),
            'timeStart': event.get_timestart(),
            'timeEnd': event.get_timeend(),
            'description': event.get_description(),
            'date': event.get_date()
        })

        try:
            for key in allEvent:
                allE.append(allEvent[key])
            allE = reversed(allE)
        except TypeError:
            allE = []

    return render_template('createEvent.html',form=form)

@app.route('/forum', methods=['POST','GET'])
def forum():
    foodList = []
    movieList = []
    elderList = []
    childList = []
    housekeepingList = []
    forumFilter = ForumFilter(request.form)
    choice = forumFilter.forumFilter.data
    fire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')
    result = fire.get('Forum', None)

    for i in result:
        if result[i]['type'] == 'Food':
            foodPlaceholder = []
            foodPlaceholder.append(result[i]['type'])
            foodPlaceholder.append(result[i]['text'])
            foodPlaceholder.append(result[i]['time'])
            foodList.append(foodPlaceholder)

    for i in result:
        if result[i]['type'] == 'Movies':
            moviePlaceholder= []
            moviePlaceholder.append(result[i]['type'])
            moviePlaceholder.append(result[i]['text'])
            moviePlaceholder.append(result[i]['time'])
            movieList.append(moviePlaceholder)

    for i in result:
        if result[i]['type'] == 'Eldercare':
            elderPlaceholder = []
            elderPlaceholder.append(result[i]['type'])
            elderPlaceholder.append(result[i]['text'])
            elderPlaceholder.append(result[i]['time'])
            elderList.append(elderPlaceholder)

    for i in result:
        if result[i]['type'] == 'Housekeeping':
            housePlaceholder = []
            housePlaceholder.append(result[i]['type'])
            housePlaceholder.append(result[i]['text'])
            housePlaceholder.append(result[i]['time'])
            housekeepingList.append(housePlaceholder)

    for i in result:
        if result[i]['type'] == 'Childcare':
            childPlaceholder = []
            childPlaceholder.append(result[i]['type'])
            childPlaceholder.append(result[i]['text'])
            childPlaceholder.append(result[i]['time'])
            childList.append(childPlaceholder)

    forumList = []
    for key in result:
        keyList = []
        keyList.append(result[key]['type'])
        keyList.append(result[key]['text'])
        keyList.append(result[key]['time'])
        forumList.append(keyList)
    if choice == 'Food':
        forumList = foodList
    elif choice == 'Movies':
        forumList = movieList
    elif choice == 'Childcare':
        forumList = childList
    elif choice == 'Eldercare':
        forumList = elderList
    elif choice == 'Housekeeping':
        forumList = housekeepingList
    forumList.reverse()
    return render_template('forumdesign.html',forumList = forumList ,forumFilter = forumFilter)

@app.route('/postForum',methods=['POST','GET'])
def post_forum():
    form = forumForm(request.form)
    if request.method == 'POST':
        text = form.forumText.data
        type = form.forumType.data

        newForum = Forum(text,type)
        newForum_db = root.child('Forum')
        newForum_db.push(
            {



            'text' : newForum.get_text(),
            'type' : newForum.get_type(),
            'time' : newForum.get_date()

        })

        return redirect(url_for('forum'))
    return render_template('postForum.html',form=form)


@app.route('/map')
def camera():
    return render_template('map.html')

if __name__ == "__main__":
    app.run(debug=True)
