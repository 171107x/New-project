from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField,validators
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, db
#firebase = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com/')


#cred = credentials.Certificate('./cred/oopproject-f5214-firebase-adminsdk-vkzv0-5ab9f1da25.json')
#default_app = firebase_admin.initialize_app(cred, {
#    'databaseURL': 'https://oopproject-f5214.firebaseio.com/'
#})


root = db.reference()


app = Flask(__name__)

class Recipe(Form):
    username = StringField("username",[validators.Length(min=1, max=150),validators.DataRequired()])
    recipeName = StringField('Recipe Name', [validators.DataRequired()])
    recipeDetails = TextAreaField('Recipe Details',[validators.DataRequired()])

class Details:
    def __init__(self,user,recipeName,recipeDetails):
        self.__user = user
        self.__recipeName = recipeName
        self.__recipeDetails = recipeDetails

    def get_user(self):
        return self.__user

    def set_user(self, user):
        self.__user = user

    def get_recipeName(self):
        return self.__recipeName

    def set_recipeName(self, recipeName):
        self.__recipeName = recipeName

    def get_recipeDetails(self):
        return self.__recipeDetails

    def set_recipeDetails(self, recipeDetails):
        self.__recipeDetails = recipeDetails

@app.route('/Recipe' , methods=['POST','GET'])
def form():
    form = Recipe(request.form)
    if request.method == 'POST' and form.validate():
        user = form.username.data
        recipeName = form.recipeName.data
        recipeDetails = form.recipeDetails.data

        recipe = Details(user,recipeName,recipeDetails)
        recipe_db = root.child('Details')
        recipe_db.push({
            "name": recipe.get_user(),
            "Recipe_name": recipe.get_recipeName(),
            "Recipe_Details": recipe.get_recipeDetails(),
    })
        print(user)
        return redirect('Recipe')
    return render_template('Recipeform.html', form=form)

@app.route('/viewRecipe')
def retrieveDetails():

    retrival = root.child('Details').get()
    list = []
    list2 = []
    list3 = []
    for i in retrival:

        t = Details(retrival[i]['name'], retrival[i]['Recipe_name'], retrival[i]['Recipe_Details'])
        list.append(t.get_user())
        list2.append(t.get_recipeName())
        list3.append(t.get_recipeDetails())
    return render_template("viewRecipe.html", retrival=list, retrival2=list2, retrival3=list3)
    #for i in firebase.get('Recipe',None):
    #    firedat=firebase.get('Recipe',i)
    #    t = Recipe(firedat["user"], firedat["recipeName"], firedat["recipeDetails"])
    #   list.append(t.get_user())
    #   list2.append(t.get_recipeName())
    #   list3.append(t.get_recipeDetails())


if __name__ == '__main__':
    app.secret_key = "something"
    app.run(debug=True)


