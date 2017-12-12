class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.about_me = ''

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def set_username(self, username):
        self.username = username

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = password

class Edit:
    def __init__(self, username, about_me):
        self.username = username
        self.about_me = about_me

    def get_username(self):
        return self.username

    def get_about_me(self):
        return self.about_me

    def set_username(self, username):
        self.username = username

    def set_about_me(self, about_me):
        self.about_me = about_me




