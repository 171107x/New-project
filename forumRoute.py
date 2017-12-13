from flask import Flask, render_template, request, redirect, url_for
from forum import Forum
import firebase_admin
from firebase_admin import credentials, db
from firebase import firebase
from wtforms import Form,StringField, TextAreaField, RadioField, SelectField

cred = credentials.Certificate( 'cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopproject-f5214.firebaseio.com/'
})

root = db.reference()

app = Flask(__name__)


class forumForm(Form):
    forumText = TextAreaField('')
    forumType = SelectField(choices=[('','Select'),('Food','Food'),('Movies','Movies'),('Childcare','Childcare'),('Eldercare','Eldercare'),('Housekeeping','Housekeeping')])


class ForumFilter(Form):
    forumFilter = SelectField(choices=[('','Select'),('Food','Food'),('Movies','Movies'),('Childcare','Childcare'),('Eldercare','Eldercare'),('Housekeeping','Housekeeping')])


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
    return render_template('forum.html',forumList = forumList ,forumFilter = forumFilter)

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
#inside the parent need to have a child if not the parent will disappear
