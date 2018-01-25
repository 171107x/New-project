from flask import Flask, make_response, render_template
app = Flask(__name__)
import firebase_admin
from firebase import firebase
from firebase_admin import credentials, db
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import StringIO
import random
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
# import plotly
# import plotly.plotly as py
# import plotly.graph_objs as go
#fB creds
cred = credentials.Certificate('cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopproject-f5214.firebaseio.com/ '
})
fireS = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')
root = db.reference()
#plotly creds
# plotly.tools.set_credentials_file(username='kinnif', api_key='J19CuzqRnpFYYD1SBEiK')

@app.route('/graphStats')
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

    label = ['North','East','South','West']
    statsCount = [
        northCount,
        westCount,
        eastCount,
        southCount
    ]

    index = np.arange(len(label))

    def plot_bargraph():
        plt.bar(index,statsCount)
        plt.xlabel('Number of users',fontsize = 5)
        plt.ylabel('Location of users',fontsize = 5)
        plt.xticks(index,label,fontsize=5,rotation=30)
        plt.title('Numbers of users in Smart Kampung')
        plt.savefig('graphStats.png')



    plot_bargraph()
    # fig = plot_bargraph()
    # canvas = FigureCanvas(fig)
    # png_output = StringIO()
    # canvas.print_png(png_output)
    # response = make_response(png_output.getvalue())
    # response.headers['Content-Type'] = 'image/png'
    # return response
    #     data = [go.Bar(
    #             x = ['North','South','East','West'],
    #             y = [northCount,southCount,eastCount,westCount]
    #         )]
    #
    # py.iplot(data,filename='basic-bar')

    return render_template("home.html")

if __name__ == "__main__":
    app.run()