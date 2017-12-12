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
    return render_template('photodesign.html', pictureList = pictureList)

if __name__ == '__main__':
    app.run()


# @app.route('/', methods=['POST','GET'])
# def forum():
#     fire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')
#     ref = fire.reference('dinosaurs')
#     snapshot = ref.order_by_child('height').get()
#     for key, val in snapshot.items():
#         print('{0} was {1} meters tall'.format(key, val))
#
#     if request.method == 'POST':
#         text = formA.forumText.data
#         type = formA.forumType.data
#
#         newForum = Forum(text,type)
#         newForum_db = root.child('Forum')
#         newForum_db.push(
#             {
#
#
#
#             'text' : newForum.get_text(),
#             'type' : newForum.get_type()
#
#         })
#         return redirect(url_for('forum'))