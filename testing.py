from flask import Flask, render_template, redirect, url_for, request, flash,session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators
import firebase_admin
from Events import Events
from firebase_admin import credentials,db
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
    timeStart = SelectField('Start Time', choices=[('', 'Select'), ('Morn7:00', '7:00AM'), ('Morn8:00', '8:00AM'), ('Morn9:00', '9:00AM'), ('Morn10:00', '10:00AM'), ('Morn11:00', '11:00AM'), ('Aft12:00', '12:00PM'),
                         ('Aft1:00', '1:00PM'),('Aft2:00', '2:00PM'),('Aft3:00', '3:00PM'),('Aft4:00', '4:00PM'),('Aft5:00', '5:00PM'),('Eve6:00', '6:00PM'),('Eve7:00', '7:00PM'),('Eve8:00', '8:00PM'),('Night9:00','9:00PM'),('Night10:00','10:00PM')], default='')
    timeEnd = SelectField('End Time', choices=[('', 'Select'), ('Morn7:00', '7:00AM'), ('Morn8:00', '8:00AM'),
                                               ('Morn9:00', '9:00AM'), ('Morn10:00', '10:00AM'),
                                               ('Morn11:00', '11:00AM'), ('Aft12:00', '12:00PM'),
                                               ('Aft1:00', '1:00PM'), ('Aft2:00', '2:00PM'), ('Aft3:00', '3:00PM'),
                                               ('Aft4:00', '4:00PM'), ('Aft5:00', '5:00PM'), ('Eve6:00', '6:00PM'),
                                               ('Eve7:00', '7:00PM'), ('Eve8:00', '8:00PM'), ('Night9:00', '9:00PM'),
                                               ('Night10:00', '10:00PM')], default='')
    location = StringField('Location of event',[validators.DataRequired()])
    description = StringField('Description of event',[validators.DataRequired()])

@app.route('/events',methods=['GET','POST'])
def new():
    form = eventsForm(request.form)
    if request.method == 'POST' and form.validate():
            title = form.title.data
            location = form.location.data
            category = form.category.data
            timestart = form.timeStart.data
            timeend = form.timeEnd.data
            description = form.description.data

            event = Events(title,location,category,timestart,timeend,description)

    event_db = root.child('Events')
    event_db.push({
        'title': event.get_title(),
        'location': event.get_location(),
        'category': event.get_category(),
        'timeStart': event.get_timestart(),
        'timeEnd': event.get_timeend(),
        'description': event.get_description(),
    })

    return render_template('event.html', form=form)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
