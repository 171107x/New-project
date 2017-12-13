from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField
import firebase_admin
from firebase_admin import credentials, db

cred = red = credentials.Certificate('cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopproject-f5214.firebaseio.com/'
})

class FirebaseHelper:
    def __init__(self):
        self.__root = db.reference()

    def get_db_reference(self):
        return self.__root

