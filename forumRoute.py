from flask import Flask, render_template, request, redirect, url_for
from forum import Forum
import firebase_admin
from firebase_admin import credentials, db
from firebase import firebase
from wtforms import Form,StringField, TextAreaField, RadioField, SelectField

cred = credentials.Certificate('cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopproject-f5214.firebaseio.com/'
})

root = db.reference()

app = Flask(__name__)


class forumForm(Form):
    forumText = TextAreaField('')
    forumType = SelectField(choices=[('','Select'),('Food','Food'),('Movies','Movies'),('Childcare','Childcare'),('Eldercare','Eldercare'),('Housekeeping','Housekeeping')])


@app.route('/forum', methods=['POST','GET'])
def forum():
    formA = forumForm(request.form)
    fire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')
    result = fire.get('Forum', None)
    if request.method == 'POST':
        text = formA.forumText.data
        type = formA.forumType.data

        newForum = Forum(text,type)
        newForum_db = root.child('Forum')
        newForum_db.push(
            {



            'text' : newForum.get_text(),
            'type' : newForum.get_type()

        })
        return redirect(url_for('forum'))
    return render_template('forum.html',form=formA,result=result)

if __name__ == "__main__":
    app.run(debug=True)
#inside the parent need to have a child if not the parent will disappear
