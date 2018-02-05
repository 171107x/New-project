from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, RadioField, validators
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, db
#firebase = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')


#cred = credentials.Certificate('./cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
#default_app = firebase_admin.initialize_app(cred, {
#    'databaseURL': 'https://oopproject-f5214.firebaseio.com/'
#})




app = Flask(__name__)

class Entry(Form):
    username = StringField("Username",
    [validators.Length(min=1, max=150),
    validators.DataRequired()])
    tiptype = RadioField("Tip Type",choices=[("elder","Eldercare"),("child","Childcare"),("house","housekeeping")])
    tip = TextAreaField('Tip',[validators.DataRequired()])

class Tip:
    def __init__(self,name,type,tip):
        self.__name = name
        self.__type = type
        self.__tip = tip
        self.__tipid = ""

    def get_name(self):
        return self.__name
    def set_name(self,name):
        self.__name = name
    def get_type(self):
        return self.__type
    def set_type(self,type):
         self.__type = type
    def get_tip(self):
        return self.__tip
    def set_tip(self,tip):
        self.__tip= tip
    def get_tipid(self):
        return self.__tipid
    def set_tipid(self,tipid):
        self.__tipid = tipid

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


if __name__ == '__main__':
    app.secret_key="something"
    app.run(debug=True)