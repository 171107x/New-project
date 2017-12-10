class Forum:
    count = 2
    def __init__(self,text,type):
        self.__text = text
        self.__type = type
        self.__class__.count += 1
        # createtime = datetime.now()
        # currenttime = str(createtime.day) + "-" + str(createtime.month) + "-" + str(createtime.year)  # DD-MM-YYYY format


    def get_text(self):
        return self.__text

    def get_type(self):
        return self.__type

    def set_text(self,text):
        self.__text = text

    def set_type(self,type):
        self.__type = type
