from flask import Flask, render_template, request, session, redirect, url_for
import firebase_admin
from firebase import firebase
from firebase_admin import credentials, db
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
#fB creds
cred = credentials.Certificate('cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopproject-f5214.firebaseio.com/ '
})
fireS = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')
root = db.reference()
#plotly creds
plotly.tools.set_credentials_file(username='kinnif', api_key='J19CuzqRnpFYYD1SBEiK')

def printStats():
    northCount = 0
    westCount = 0
    eastCount = 0
    southCount = 0
    stats = fireS.get('userInfo', None)
    print(stats)
    for i in stats:
        if stats[i]['region']== 'North':
             northCount += 1
        elif stats[i]['region'] == 'West':
             westCount += 1
        elif stats[i]['region'] == 'East':
             eastCount += 1
        elif stats[i]['region'] == 'South':
             southCount += 1

        data = [go.Bar(
                x = ['North','South','East','West'],
                y = [northCount,southCount,eastCount,westCount]
            )]

    py.iplot(data,filename='basic-bar')

printStats()