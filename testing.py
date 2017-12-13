from flask import Flask, render_template, redirect, url_for, request, flash,session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators
import firebase_admin
from Events import Events
from firebase_admin import credentials,db
from firebase import firebase
cred = credentials.Certificate('./cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopproject-f5214.firebaseio.com/ '
})
root = db.reference()
app = Flask(__name__)

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
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)

# DB ROOT
# event_db = root.child('Events')
# event_db.push({
#     'title': event.get_title(),
#     'location': event.get_location(),
#     'category': event.get_category(),
#     'timeStart': event.get_timestart(),
#     'timeEnd': event.get_timeend(),
#     'description': event.get_description(),
# })
