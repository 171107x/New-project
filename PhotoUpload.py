from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def photoupload():
    return render_template('indexPU.html')

if __name__ == '__main__':
    app.run()
