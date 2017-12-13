from datetime import datetime


class Forum:
    count = 2


    def __init__(self, text, type):
        self.__text = text
        self.__type = type
        self.__class__.count += 1
        self.createTime = datetime.now()
        self.currentTime = str(self.createTime.day) + "-" + str(self.createTime.month) + "-" + str(self.createTime.year) # DD-MM-YYYY format


    def get_text(self):
        return self.__text

    def get_type(self):
        return self.__type

    def set_text(self,text):
        self.__text = text

    def set_type(self,type):
        self.__type = type

    def get_date(self):
        return self.currentTime
