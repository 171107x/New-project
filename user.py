from datetime import datetime

class User:
    def __init__(self, username, email, password, about_me):
        self.username = username
        self.email = email
        self.password = password
        self.about_me = about_me

    def get_about_me(self):
        return self.about_me

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

    def set_about_me(self, about_me):
        self.about_me = about_me

class Edit:
    def __init__(self, password):
        self.password = password

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.username = password



class Review:
    def __init__(self, title, review):
        self.title = title
        self.review = review
        self.createTime = datetime.now()
        self.currentTime = str(self.createTime.day) + "-" + str(self.createTime.month) + "-" + str(self.createTime.year)  # DD-MM-YYYY format

    def get_title(self):
        return self.title

    def get_review(self):
        return self.review

    def set_title(self, title):
        self.title = title

    def set_review(self, review):
        self.review = review

    def get_date(self):
        return self.currentTime
