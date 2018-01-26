def generate():
    alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    length = 12
    password = ''

    for i in range(length):
        char = random.randrange(len(alphabet))
        password += alphabet[char]
    return password


password = generate()
print(password)
users = root.child('userInfo').get()
tempuser = ''
for user in users:
    if users[user]['email'] == email:
        user_db = root.child('userInfo/' + user)
        user_db.update({
            'password': password

        })
        tempuser = user
        break

msg = Message('Reset Password', sender='nypsmartkampung@gmail.com', recipients='email')
msg.body = 'Hi ' + users[tempuser]['username'] + '\n Your new temporary password is {}'.format(password)
mail.send(msg)
return '<p> check your email</p>'
