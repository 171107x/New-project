from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, db
firebase = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')


cred = credentials.Certificate('cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopproject-f5214.firebaseio.com/'
})

root = db.reference()


app = Flask(__name__)

class Tipsform(Form):
    housekeeping_tips = TextAreaField('Tips')
    name_tips = StringField("name")

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

@app.route('/form' , methods=['POST','GET'])
def form():
    form = Tipsform(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name_tips.data
        tips = form.housekeeping_tips.data

        tip = Tips(name,tips)

        tip_db =root.child('Tips')
        tip_db.push({
            "name": tip.get_name(),
            "tips": tip.get_tips()
        })
        print(name)
        return redirect('form')
    return render_template('form.html', form=form)

@app.route('/viewTip')
def retrieveTip():


    retrival = root.child('Tips').get()
    list = []
    list2=[]
    for i in firebase.get('Tips',None):
        firedat=firebase.get('Tips',i)
        t=Tips(firedat["name"], firedat["tips"])
        list.append(t.get_name())
        list2.append(t.get_tips())


    return render_template("viewTip.html", retrival= list,retrival2=list2)
#    result = firebase.post('/viewTip', "Tips", None)
#   print(result)


# result = db.post("/form",{"test: one"} )
if __name__ == '__main__':
    app.secret_key="something"
    app.run(debug=True)
