from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from forms import SignupForm, LoginForm, EditForm, ReviewForm, EmailForm, PasswordForm
from user import User, Edit, Review
from firebase import firebase
from Events import Events
from tipv2 import  Tip, Entry
from recipeform import  Details, Recipe
from forum import Forum
import firebase_admin
from firebase_admin import credentials, db
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators
import pygal
from flask_socketio import SocketIO, emit
import random
import jwt
from geopy.geocoders import Nominatim
import datetime
from werkzeug.utils import secure_filename
from geopy.exc import GeocoderTimedOut

fireS = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')
cred = credentials.Certificate('./cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
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
app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer('Thisisasecret!')
Bootstrap(app)

app.secret_key = "baby123"
socketio = SocketIO( app )



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

class PhotoFilter(Form):
    photoFilter = SelectField(choices=[('','Select'),
                                       ('Bridal','Bridal'),
                                       ('Educational','Educational'),
                                       ('Commemorative','Commemorative'),
                                       ('Charity','Charity'),
                                       ('Food','Food'),
                                       ('Others','Others')])

class forumForm(Form):
        forumText = TextAreaField('')
        forumType = SelectField(
            choices=[('', 'Select'), ('Food', 'Food'), ('Movies', 'Movies'), ('Childcare', 'Childcare'),
                     ('Eldercare', 'Eldercare'), ('Housekeeping', 'Housekeeping')])

class ForumFilter(Form):
        forumFilter = SelectField(
            choices=[('', 'Select'), ('Food', 'Food'), ('Movies', 'Movies'), ('Childcare', 'Childcare'),
                     ('Eldercare', 'Eldercare'), ('Housekeeping', 'Housekeeping')])

class Tipsform(Form):
    housekeeping_tips = TextAreaField('Tips')
    name_tips = StringField("name")

class responseForm(Form):
    responseText = StringField("Please try to refrain from aggressive responses")

class RecycleForm(Form):
    recycleDay = SelectField('',
        choices=[('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),
                 ('Friday','Friday'),('Saturday','Saturday'),('Sunday','Sunday') ])
    recycleTime = SelectField('' ,
        choices=[('Morning','Morning'),('Afternoon','Afternoon'),('Evening','Evening')]
    )

class Response:
    def __init__(self,response):
        self.__responseText = response

    def get_response(self):
        return self.__responseText

class Tips():
    def __init__(self, name, tips):
        self.__name = name
        self.__tips = tips
        self.__pubid = ''


    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_tips(self,):
        return self.__tips

    def set_tips(self,tips):
        self.__tips=tips

    def get_pubid(self):
        return self.__pubid

    def set_pubid(self, pubid):
        self.__pubid = pubid

class addForm(Form):
    contentText = TextAreaField('')
    titleText = TextAreaField('')

class Content:
    def __init__(self,tText,text):
        self.__titleText = tText
        self.__contentText = text

    def get_text(self):
        return self.__contentText

    def get_Ttext(self):
        return self.__titleText


@app.route("/")
def index():
    retrieveCount = fireS.get('recycleCount', None)
    recyclecount = int(retrieveCount['recycleCount'])
    retrieveUser = fireS.get('userInfo',None)
    retrieveEvent = fireS.get('Events',None)
    eventCount = 0
    for key in retrieveEvent:
        eventCount += 1
    userCount = 0
    for key in retrieveUser:
        userCount += 1
    northCount = 0
    westCount = 0
    eastCount = 0
    southCount = 0
    stats = fireS.get('userInfo', None)
    for i in stats:
        if stats[i]['region'] == 'North':
            northCount += 1
        elif stats[i]['region'] == 'West':
            westCount += 1
        elif stats[i]['region'] == 'East':
            eastCount += 1
        elif stats[i]['region'] == 'South':
            southCount += 1

    line_chart = pygal.HorizontalBar()
    line_chart.title = 'Numbers of users in Smart Kampung'
    line_chart.add('North', northCount)
    line_chart.add('East', eastCount)
    line_chart.add('West', westCount)
    line_chart.add('South', southCount)
    graph_data = line_chart.render_data_uri()
    return render_template("index.html",line_chart=graph_data,recyclecount=recyclecount,userCount=userCount,eventCount=eventCount)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            username = form.username.data
            email = form.email.data
            password = form.password.data
            about_me = form.about_me.data
            region = form.region.data

            usernameList = []
            emailList = []
            result = root.child('userInfo').get()

            for users in result:
                usernameList.append(result[users]['username'])
                emailList.append(result[users]['email'])
            if username not in usernameList and email not in emailList:
                user = User(username, email, password, about_me)
                user_db = root.child('userInfo')
                user_db.push({
                    'username' : user.get_username(),
                    'email': user.get_email(),
                    'password': user.get_password(),
                    'about_me': user.get_about_me(),
                    'region' : region,
                    'token' : 0
                })
                token = s.dumps(email, salt='email-confirm')

                msg = Message('Confirm Email', sender='omgnooopython@gmail.com', recipients=[email])

                link = url_for('confirm_email', token=token, _external=True)

                msg.body = 'You have successfully register. Please click on this link to continue {}'.format(link)

                mail.send(msg)

                session['username'] = user.username
                return render_template('register.html', email=email)
            else:
                error = 'Username already exists'
                flash(error, 'danger')
                return redirect(url_for('signup', form=form, error=error))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return render_template("confirm-email.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        username = form.username.data
        password = form.password.data


        usernameList = []
        passList = []
        confPass = []
        result = root.child('userInfo').get()

        for users in result:
            usernameList.append(result[users]['username'])
            passList.append(result[users]['password'])
        attempted_username = request.form['username']
        attempted_password = request.form['password']
        for key in result:
            if username == result[key]['username']:
                confPass.append(result[key]['password'])
        if attempted_username in usernameList and attempted_password in confPass:
            session['username'] = form.username.data
            return redirect(url_for('home'))
        else:
            error = 'Invalid login'
            flash(error, 'danger')
            return redirect(url_for('login', form=form,error=error))

    elif request.method == "GET":
        return render_template("login.html", form=form)


@app.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if request.method == 'POST':
        users = root.child('userInfo').get()
        for user in users:
            if users[user]['email'] == form.email.data:
                email = users[user]['email']

                token = s.dumps(email, salt='recover-key')

                msg = Message('Reset Password', sender='omgnooopython@gmail.com', recipients=[email])

                link = url_for('resetpass', token=token, _external=True)

                msg.body = 'Hi ' + users[user]['username'] + ' Your reset link is {} and expires in 1 day'.format(link)

                mail.send(msg)

                return render_template('reset2.html')
    return render_template('reset.html', form=form)

def passwordgen():
    alphabet = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    length = 12
    password = ''
    for i in range(length):
        char = random.randrange(len(alphabet))
        password = password + alphabet[char]
    return password

@app.route('/resetpass/<token>', methods=['GET', 'POST'])
def resetpass(token):
    try:
        email = s.loads(token, salt='recover-key', max_age=3600)
    except:
        return render_template('404.html')

    password = passwordgen()
    users = root.child('userInfo').get()
    for i in users:
        if users[i]['email'] == email:
            user_db = root.child('userInfo/' + i)
            user_db.update({
                'password': password
            })

    msg = Message('Password Reseted', sender='omgnooopython@gmail.com', recipients=[email])

    msg.body = 'Dear' + users[i]['username'] + 'Your new temporary password is {}'.format(password)
    mail.send(msg)
    return render_template('reset_with_token.html', email=email)



@app.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    if 'username' in session:
        form = ReviewForm(request.form)

        bioList = []
        titleList = []
        timeList = []
        reviewList = []
        posterList = []
        allList = []

        bio = root.child('userInfo').get()
        for key in bio:
            if username == bio[key]['username']:
                bioList.append(bio[key]['about_me'])

        forumList = []
        forum = root.child('Forum').get()
        for key in forum:
            if username == forum[key]['username']:
                forumList.append(forum[key]['username'])

        review = root.child('review').get()
        if review != None:
            for reviews in review:
                if username == review[reviews]['username']:
                    titleList.append(review[reviews]['title'])
                    timeList.append(review[reviews]['time'])
                    reviewList.append(review[reviews]['review'])
                    posterList.append(review[reviews]['poster'])
        titleList.reverse()
        timeList.reverse()
        reviewList.reverse()
        posterList.reverse()
        allList.append(titleList)
        allList.append(reviewList)
        allList.append(posterList)
        allList.append(timeList)


        fire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')
        ref = fire.get('/profilePic', None)
        pictureList = []
        if ref != None:
            for key in ref:
                if username == ref[key]['username'] :
                    pictureList.append(ref[key]['photo'])


        if request.method == 'POST' and form.validate():
            title = form.title.data
            review = form.review.data

            review = Review(title, review)
            review_db = root.child('review')
            review_db.push({
                'username' : username,
                'title' : review.get_title(),
                'review' : review.get_review(),
                'time' : review.get_date(),
                'poster' : session['username']

                    })
            return redirect(url_for('user',username=username))

        return render_template('userProfile.html', form=form, username=username, bioList=bioList,allList=allList,reviewList=len(reviewList),forumList=len(forumList),pictureList=pictureList)

@app.route('/<username>/posts', methods=['GET', 'POST'])
def posts(username):
    if 'username' in session:
        result = root.child('Forum').get()
        postList = []
        for key in result:
            if username == result[key]['username']:
                keyList = []
                keyList.append(result[key]['type'])
                keyList.append(result[key]['text'])
                keyList.append(result[key]['time'])
                keyList.append(result[key]['username'])
                postList.append(keyList)
        postList.reverse()
        return render_template('posts.html', postList=postList, username=username)

@app.route('/settings/profilePic', methods=["GET", "POST"])
def profilePic():

    username = session['username']
    emailList = []
    allUser = root.child('userInfo').get()
    for key in allUser:
        if username == allUser[key]['username']:
            emailList.append(allUser[key]['email'])

    keyPic = []
    userList = []
    picKey = ''
    pictureList = []
    fire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')
    ref = fire.get('/profilePic', None)
    if ref != None:
        for key in ref:
            if username == ref[key]['username']:
                pictureList.append(ref[key]['photo'])

    print(pictureList)

    pic = root.child('profilePic').get()
    for pkey in pic:
        if username == pic[pkey]['username']:
            keyPic.append(pic[pkey]['photo'])
            userList.append(pic[pkey]['username'])
            picKey = pkey
    print(keyPic)
    print(picKey)

    return render_template('test.html', form=form, emailList=emailList, keyPic=keyPic, userList=userList, picKey=picKey, pictureList=pictureList)

@app.route('/settings/password', methods=["GET", "POST"])
def password():
    form = EditForm()

    if request.method == 'POST':
        username = session['username']
        password = form.password.data

        allUser = root.child('userInfo').get()
        user = Edit(password)
        for key in allUser:
            print(allUser[key]['username'])
            if username == allUser[key]['username']:
                user_db = root.child('userInfo/'+key)
                user_db.update({
                'password': user.get_password()
                })

        return redirect(url_for('user', username=username))
    return render_template('password.html', form=form)

@app.route('/settings/account', methods=["GET", "POST"])
def account():
    form = EditForm(request.form)

    username = session['username']
    emailList = []
    allUser = root.child('userInfo').get()
    for key in allUser:
        print(allUser[key]['username'])
        if username == allUser[key]['username']:
            emailList.append(allUser[key]['email'])

    if request.method == 'POST':
        username = session['username']

        about_me = form.about_me.data
        emailList = []

        allUser = root.child('userInfo').get()
        for key in allUser:
            print(allUser[key]['username'])
            if username == allUser[key]['username']:
                user_db = root.child('userInfo/'+key)
                user_db.update({
                'about_me': about_me
                })
                emailList.append(allUser[key]['email'])


        return redirect(url_for('user', username=username, emailList=emailList))
    return render_template('edit.html', form=form, emailList=emailList)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route("/home")
def home():
    if 'username' in session:
        retrieveCount = fireS.get('recycleCount', None)
        recyclecount = int(retrieveCount['recycleCount'])
        retrieveUser = fireS.get('userInfo',None)
        retrieveEvent = fireS.get('Events',None)
        eventCount = 0
        userCount = 0
        for key in retrieveEvent:
            eventCount += 1

        for key in retrieveUser:
            userCount += 1
        print(retrieveUser)
        northCount = 0
        westCount = 0
        eastCount = 0
        southCount = 0
        stats = fireS.get('userInfo', None)
        print(stats)
        for i in stats:
            if stats[i]['region'] == 'North':
                northCount += 1
            elif stats[i]['region'] == 'West':
                westCount += 1
            elif stats[i]['region'] == 'East':
                eastCount += 1
            elif stats[i]['region'] == 'South':
                southCount += 1

        line_chart = pygal.HorizontalBar()
        line_chart.title = 'Numbers of users in Smart Kampung'
        line_chart.add('North', northCount)
        line_chart.add('East', eastCount)
        line_chart.add('West', westCount)
        line_chart.add('South', southCount)
        graph_data = line_chart.render_data_uri()
        return render_template("home.html",line_chart=graph_data,userCount=userCount,eventCount=eventCount,recyclecount=recyclecount)
    return redirect(url_for('login'))

@app.route('/photowall', methods=['GET','POST'])
def upload():
    if 'username' in session:
        allList = []
        bridalList = []
        educationalList = []
        commemorativeList = []
        charityList = []
        foodList = []
        othersList = []
        photoFilter = PhotoFilter(request.form)
        choice = photoFilter.photoFilter.data


        bridal = root.child('Images/Bridal').get()
        for image in bridal:
            bridalList.append(bridal[image])
            allList.append(bridal[image])

        educational = root.child('Images/Educational').get()
        for image in educational:
            educationalList.append(educational[image])
            allList.append(educational[image])

        commemorative = root.child('Images/Commemorative').get()
        for image in commemorative:
            commemorativeList.append(commemorative[image])
            allList.append(commemorative[image])

        charity = root.child('Images/Charity').get()
        for image in charity:
            charityList.append(charity[image])
            allList.append(charity[image])

        food = root.child('Images/Food').get()
        for image in food:
            foodList.append(food[image])
            allList.append(food[image])

        others = root.child('Images/Others').get()
        for image in others:
            othersList.append(others[image])
            allList.append(others[image])

        pictureList = []

        if choice == '':
            pictureList = allList

        elif choice == 'Bridal':
            pictureList = bridalList
            pictureList.reverse()

        elif choice == 'Educational':
            pictureList = educationalList
            pictureList.reverse()

        elif choice == 'Commemorative':
            pictureList = commemorativeList
            pictureList.reverse()

        elif choice == 'Charity':
            pictureList = charityList
            pictureList.reverse()

        elif choice == 'Food':
            pictureList = foodList
            pictureList.reverse()

        elif choice == 'Others':
            pictureList = othersList
            pictureList.reverse()



        # for key in ref:
        #     photoLink = ref.get(key)
        #     pictureList.append(photoLink)
        # pictureList.reverse()

        return render_template('photodesign.html',pictureList = pictureList,photoFilter = photoFilter)
    return redirect(url_for('index'))


@app.route('/photoupload', methods=['GET','POST'])
def uploads():
    if 'username' in session:
        form = PhotoFilter(request.form)
        choice = form.photoFilter.data
        fire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')
        ref = fire.get('/Images',None)
        refx = root.child('ImageFilter')
        refy = refx.get()
        print(refy)
        xd = list(refy)
        if choice == 'Bridal':
            refx.set({
                'Bridal': 1
            })
        elif choice == 'Charity':
            refx.set({
                'Charity': 1
            })
        elif choice == 'Commemorative':
            refx.set({
                'Commemorative': 1
            })
        elif choice == 'Educational':
            refx.set({
                'Educational': 1
            })
        elif choice == 'Food':
            refx.set({
                'Food': 1
            })
        elif choice == 'Others':
            refx.set({
                'Others': 1
            })
        elif choice == 'Select':
            refx.set({
                'Others':1
            })
        pictureList = []
        for key in ref:
            photoLink = ref.get(key)
            pictureList.append(photoLink)
        pictureList.reverse()

        return render_template('photoupload.html',pictureList = pictureList, form = form, refy=refy)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET','POST'])
def search():
    sr = root.child('Content')
    sg = sr.get()
    resultList = []
    searchedItem = "Null"
    resultList.append(searchedItem)
    if request.method == 'POST':
        resultList.pop()
        term = request.form["query"]
        for key in sg:
            term = term.lower()
            checkTitle = sg[key]['title'].lower()
            checkContent = sg[key]['contents'].lower()
            if term in checkTitle or term in checkContent:
                containerList = []
                searchedTitle = sg[key]['title']
                searchedContent = sg[key]['contents']
                containerList.append(searchedTitle)
                containerList.append(searchedContent)
                resultList.append(containerList)
            elif term not in checkContent and term not in checkTitle:
                searchedItem = "Empty"
    return render_template('search2.html',resultList = resultList)

@app.route("/add", methods=['GET','POST'])
def add():
    form = addForm(request.form)
    if request.method =="POST":
        title= form.titleText.data
        text = form.contentText.data
        newContent = Content(title,text)
        newContent_db = root.child('Content')
        newContent_db.push(
            {
                'title': newContent.get_Ttext(),
                'contents' : newContent.get_text()
            })
        return redirect(url_for('search'))

    return render_template("add.html",form=form)


@app.route('/events',methods=['GET','POST'])
def new():
    if 'username' in session:
        form = eventsForm(request.form)
        allE = []
        eventFire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/ ')
        allEvent = eventFire.get('Events', None)
        # if request.method == 'POST':

            # for key in allEvent:
            #     xd = allEvent[key]['interested'] + 1
            #     root.child('Events/' + key).update({'interested': xd})

        class locationEvent:
            def __init__(self,latList,lngList):
                self.latList = latList
                self.lngList = lngList

        retrieveEvent = root.child('Events')
        retrieveEvent2 = retrieveEvent.get()
        locationList = []
        for key in retrieveEvent2:
            # print("this is title" + title)
            l0cation = retrieveEvent2[key]['location']
            locationList.append(l0cation)


        latlongList = []
        geolocater = Nominatim(timeout=60)
        for niggers in locationList:
            try:
                location = geolocater.geocode(niggers)
                genericList = []
                genericList.append(location.latitude)
                genericList.append(location.longitude)
                latlongList.append(genericList)
            except GeocoderTimedOut as e:
                print("Error: geocode failed on input %s with message %s" % (niggers, e.msg))
    #     events = (
    #     locationEvent(latList,lngList)
    # )

        try:
            for key in allEvent:
                allE.append(allEvent[key])
        except TypeError:
            allE = []

        i = 0
        for key in allE:
            key['map'] = latlongList[i][0]
            i += 1

        revEvent = []
        for key in allE:
            revEvent.insert(0,key)
        print(allE)
        print(revEvent)
        try:
            count = len(allEvent) + 1
        except TypeError:
            count = 1
        return render_template('showEvent.html', form=form,count=count,latlongList=latlongList,revEvent=revEvent)
    return redirect(url_for('index'))

@app.route('/showInterest/<eventName>')
def asdasd(eventName):
    if 'username' in session:
        eventName = eventName
        currEventr = root.child('Events')
        currEventg = currEventr.get()
        for key in currEventg:
            if currEventg[key]['title'] == eventName:
                intEventr = root.child('Events/'+ key)
                intEventg = intEventr.get()
                count = intEventg['interested']
                intEventr.update({
                    'interested': count+1
                })
                eventid = key

        theEventr = root.child('Events/' + eventid + '/going')
        theEventg = theEventr.get()
        try:
            count = len(theEventg)
        except:
            count = 0

        theEventr.update({
            count: session['username']
        })

        return render_template('showInterest.html/')

@app.route('/createEvent',methods=['POST','GET'])
def create_event():
    if 'username' in session:
        form = eventsForm(request.form)
        if request.method == 'POST' and form.validate():
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
                    'date': event.get_date(),
                    'username': session['username'],
                    'datetime':event.get_currenttime(),
                    'interested': 0,

                })

                try:
                    for key in allEvent:
                        allE.append(allEvent[key])
                    allE = reversed(allE)
                except TypeError:
                    allE = []
        return render_template('createEvent.html',form=form,username='username')
    return redirect(url_for('index'))

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
            foodPlaceholder.append(result[i]['username'])
            foodPlaceholder.append(result[i]['response'])
            foodPlaceholder.append(result[i]['count'])
            foodList.append(foodPlaceholder)

    for i in result:
        if result[i]['type'] == 'Movies':
            moviePlaceholder= []
            moviePlaceholder.append(result[i]['type'])
            moviePlaceholder.append(result[i]['text'])
            moviePlaceholder.append(result[i]['time'])
            moviePlaceholder.append(result[i]['username'])
            moviePlaceholder.append(result[i]['response'])
            moviePlaceholder.append(result[i]['count'])
            movieList.append(moviePlaceholder)

    for i in result:
        if result[i]['type'] == 'Eldercare':
            elderPlaceholder = []
            elderPlaceholder.append(result[i]['type'])
            elderPlaceholder.append(result[i]['text'])
            elderPlaceholder.append(result[i]['time'])
            elderPlaceholder.append(result[i]['username'])
            elderPlaceholder.append(result[i]['response'])
            elderPlaceholder.append(result[i]['count'])
            elderList.append(elderPlaceholder)

    for i in result:
        if result[i]['type'] == 'Housekeeping':
            housePlaceholder = []
            housePlaceholder.append(result[i]['type'])
            housePlaceholder.append(result[i]['text'])
            housePlaceholder.append(result[i]['time'])
            housePlaceholder.append(result[i]['username'])
            housePlaceholder.append(result[i]['response'])
            housePlaceholder.append(result[i]['count'])
            housekeepingList.append(housePlaceholder)

    for i in result:
        if result[i]['type'] == 'Childcare':
            childPlaceholder = []
            childPlaceholder.append(result[i]['type'])
            childPlaceholder.append(result[i]['text'])
            childPlaceholder.append(result[i]['time'])
            childPlaceholder.append(result[i]['username'])
            childPlaceholder.append(result[i]['response'])
            childPlaceholder.append(result[i]['count'])
            childList.append(childPlaceholder)

    forumList = []
    for key in result:
        keyList = []
        keyList.append(result[key]['type'])
        keyList.append(result[key]['text'])
        keyList.append(result[key]['time'])
        keyList.append(result[key]['username'])
        keyList.append(result[key]['response'])
        keyList.append(result[key]['count'])
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
    if 'username' in session:
        form = forumForm(request.form)
        retrieve_forum_count = root.child('forumCount').get()
        forumCount = int(retrieve_forum_count['forumCount'])
        if request.method == 'POST':
            text = form.forumText.data
            type = form.forumType.data
            newForum = Forum(text,type)
            increaseCount = forumCount + 1
            newCount = root.child('forumCount/forumCount').set(increaseCount)
            newForum_db = root.child('Forum')
            newForum_db.push(
                {


                'count' : str(increaseCount),
                'text' : newForum.get_text(),
                'type' : newForum.get_type(),
                'time' : newForum.get_date(),
                'username' : session['username'],
                'response' : {'response':'empty'},
                'responseCount' : 0

            })

            return redirect(url_for('forum'))
        return render_template('postForum.html',form=form)
    else:
        return redirect(url_for('login'))

@app.route('/addResponse/<forumNumber>',methods=['POST','GET'])
def post_response(forumNumber):
    forumPost = forumNumber[5:]
    response = request.form["response"]
    allForumPost = root.child('Forum').get()
    for post in allForumPost:
        checkPost = allForumPost[post]['count']
        responseCount = allForumPost[post]['responseCount']
        newCount = int(responseCount) + 1
        responseString = 'response' + str(newCount)
        if checkPost == forumPost:
            postResponse = root.child('Forum/'+post+'/response')
            postCount = root.child('Forum/'+post)
            postCount.update({
                'responseCount' : newCount,
            })
            postResponse.update({
                responseString: {
           'username': session['username'],
            'response' : response },
            })
            print('CHECK!')
    form = responseForm(request.form)
    if request.method == "POST":
        term = request.form["response"]
        text = form.responseText.data
        newResponse = Response(text)
    return redirect(url_for('forum'))

@app.route('/tips')
def retrieveTip():
    fire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')

    retrival = root.child('Tips').get()
    list = []
    list2=[]
    for i in fire.get('Tips',None):
        firedat=fire.get('Tips',i)
        t=Tips(firedat["name"], firedat["tip"])
        list.append(t.get_name())
        list2.append(t.get_tips())


    return render_template("viewTip.html", retrival= list,retrival2=list2)
@app.route('/map')
def camera():
    return render_template('map.html')


@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404

@app.route('/contact')
def contatpage():
    return render_template('contact.html')

@app.route('/chat')
def hello():
  return render_template( 'chat.html' )

@app.route('/recycle',methods=['POST','GET'])
def recycle():
    if 'username' in session:
        retrieveCount = fireS.get('recycleCount',None)
        retrieveToken = root.child('userInfo')
        retrieveToken2 = retrieveToken.get()
        for i in retrieveToken2:
            if retrieveToken2[i]['username'] == session['username']:
                newToken = retrieveToken2[i]

        form = RecycleForm(request.form)
        if request.method == 'POST':
            recycleDay = form.recycleDay.data
            recycleTime = form.recycleTime.data
            recycleCount = int(retrieveCount['recycleCount']) + 1
            recycleCount_db = root.child('recycleCount')
            recycleCount_db.set({'recycleCount': recycleCount})
            tokenChange_db = root.child('userInfo')
            tokenChange_db2 = tokenChange_db.get()
            for i in tokenChange_db2:
                if tokenChange_db2[i]['username'] == session['username']:
                    tokenGet = root.child('userInfo/'+i)
                    tokenGet.update({'token':1})
            print(tokenChange_db.get())
            # for i in tokenChange_db:


            # tokenChange_db.set({
            #     'token':1,
            #     })
            from twilio.rest import Client
            account_sid = 'AC5091b5762fe17449d4910cb2239e0d5d'  # Found on Twilio Console Dashboard
            auth_token = '122d88ff6abe6566752ddb4b032c72a6'  # Found on Twilio Console Dashboard
            #'+6592351480
            #'+6591783904
            phoneList = ['+6591783904'] #'+6592351480' add sol's number laaaater,
            myPhone = random.choice(phoneList)# Phone number you used to verify your Twilio account+
            myToken = jwt.encode({'Request': 'Test'}, 'thisismysecret')
            TwilioNumber = '+18568884772'  # Phone number given to you by Twilio
            print(myToken)
            link = url_for('confirm_request', myToken=myToken)
            client = Client(account_sid, auth_token)

            client.messages.create(
                to=myPhone,
                from_=TwilioNumber,
                body='Block 649 has requested a recycle request to be on{},{}. To accept the request, click this link "smartkampung.herokuapp.com{}'.format(recycleDay,recycleTime,link))


            return redirect(url_for('recycle'))
        return render_template('recycle.html',form=form, newToken = newToken)
    else:
        return redirect(url_for('login'))

#
@app.route('/form', methods=['POST', 'GET'])
def form():
    entryform = Entry(request.form)
    if request.method == 'POST' and entryform.validate():
        name = entryform.username.data
        tiptype = entryform.tiptype.data
        tip = entryform.tip.data

        tip = Tip(name, tiptype, tip)

        tip_db = root.child('Tips')
        tip_db.push({
            "name": tip.get_name(),
            "type": tip.get_type(),
            "tip": tip.get_tip()
        })
        flash('you have submitted your tips, thanks for sharing', 'success')
    return render_template("entryform.html" ,form=entryform)

@app.route('/tips/elder')
def elder():
    eldertip = root.child("Tips").get()
    list = []
    for i in eldertip:
        eldertips = eldertip[i]  # just add in only, won't die either way1
        if eldertips["type"] == "elder":
            tip = Tip(eldertips["name"], eldertips["type"],eldertips["tip"])
            tip.set_tipid(i)
            list.append(tip)
    return render_template("elder.html", tip=list)

@app.route('/tips/house')
def house():
    housetip = root.child("Tips").get()
    list = []
    for i in housetip:
        housetips = housetip[i]  # just add in only, won't die either way
        if housetips["type"] == "house":
            tip = Tip(housetips["name"], housetips["type"],housetips["tip"])
            tip.set_tipid(i)
            list.append(tip)
    return render_template("house.html", tip=list)

@app.route('/tips/child')
def child():
    childtip = root.child("Tips").get()
    list = []
    for i in childtip:
        childtips = childtip[i]  # just add in only, won't die either way
        if childtips["type"] == "child":
            tip = Tip(childtips["name"], childtips["type"],childtips["tip"])
            tip.set_tipid(i)
            list.append(tip)
    return render_template("child.html", tip=list)

@app.route('/Recipe' , methods=['POST','GET'])
def recipe():
    form = Recipe(request.form)
    if request.method == 'POST' and form.validate():
        user = form.username.data
        recipeName = form.recipeName.data
        recipeDetails = form.recipeDetails.data

        recipe = Details(user,recipeName,recipeDetails)
        recipe_db = root.child('Details')
        recipe_db.push({
            "name": recipe.get_user(),
            "Recipe_name": recipe.get_recipeName(),
            "Recipe_Details": recipe.get_recipeDetails(),
    })
        flash('you have submitted your recipe, thanks for sharing', 'success')
        print(user)
        return redirect(url_for('Recipe'))
    return render_template('RecipeForm.html', form=form)

@app.route('/viewRecipe')
def retrieveDetails():

    retrival = root.child('Details').get()
    list = []
    list2 = []
    list3 = []
    for i in retrival:

        t = Details(retrival[i]['name'], retrival[i]['Recipe_name'], retrival[i]['Recipe_Details'])
        list.append(t.get_user())
        list2.append(t.get_recipeName())
        list3.append(t.get_recipeDetails())
    return render_template("viewRecipe.html", retrival=list, retrival2=list2, retrival3=list3)

@app.route('/confirm/<myToken>')
def confirm_request(myToken):
    check_dict = jwt.decode(myToken,'thisismysecret')
    print(check_dict)
    print(myToken)
    if check_dict['Request'] == 'Test':
        tokenChange_db = root.child('userInfo')
        tokenCheck = tokenChange_db.get()
        for i in tokenCheck:
            tokenValue = root.child('userInfo/'+i)
            tokenValue.update({
                'token': 0,
            })
    return render_template('map.html')#change to model for phone


def messagereceived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messagereceived())

if __name__ == "__main__":
    socketio.run(app, debug=True)

if __name__ == "__main__":
    app.run(port='80')

