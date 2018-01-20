@app.route('/edit', methods=["GET", "POST"])
def edit():
    form = EditForm(request.form)

    if request.method == 'POST':
        userFire = firebase.FirebaseApplication('https://oopproject-f5214.firebaseio.com')
        allUser = userFire.get('userInfo',None)

        username = session['username']
        email = session['email']

        about_me = form.about_me.data
        password = form.password.data


        for key in allUser:
            print(allUser[key]['username'])
            if username == allUser[key]['username'] and email == allUser[key]['email']:
                user_db = root.child('userInfo',key)
                user_db.update({
                'about_me': about_me,
                'password': password
                })

            return redirect(url_for('user/<username>'))
    return render_template('edit.html', form=form)
