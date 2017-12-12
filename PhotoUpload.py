from flask import Flask, render_template
import firebase_admin
from firebase import firebase
from firebase_admin import credentials, db

cred = credentials.Certificate('cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopproject-f5214.firebaseio.com/'
})
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run()

