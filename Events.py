class Events():
    def __init__(self, title,location,category,timestart,timeend,description):
        self.__title = title
        self.__location = location
        self.__category = category
        self.__timestart = timestart
        self.__timeend = timeend
        self.__description = description

    def get_title(self):
        return self.__title

    def get_location(self):
        return self.__location

    def get_category(self):
        return self.__category

    def get_timestart(self):
        return self.__timestart

    def get_timeend(self):
        return self.__timeend

    def get_description(self):
        return self.__description

    def set_title(self, title):
        self.__title = title

    def set_location(self, location):
        self.__location = location

    def set_category(self, category):
        self.__category = category

    def set_timestart(self, timestart):
        self.__timestart = timestart

    def set_timeend(self, timeend):
        self.__timeend = timeend

    def set_description(self, description):
        self.__description = description

