from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer('Thisisasecret!')

@app.route('/',methods = ['GET','POST'])
def index():
    token = s.dumps('dummygaranguni@hotmail.com', salt='email-confirm')

    msg = Message('Confirm Email', sender='nypsmartkampung@gmail.com', recipients=['dummygaranguni@hotmail.com'])

    link = url_for('confirm_email', token=token, external=True)

    msg.body = 'Your link is {}'.format(link)

    mail.send(msg)

    return '<h1>The email you entered is {}. The token is {}</h1>'.format('dummygaranguni@hotmail.com', token)

@app.route('/confirmToken/<token>')
def confirm_email(token):
    email = s.loads(token, salt='email-confirm')
    return 'The token works!'

if __name__ == '__main__':
    app.run(debug=True)
