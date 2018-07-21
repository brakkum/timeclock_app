import datetime
import time
import os

class TaskManager():
    def __init__(self, ticket, directory):
        self.ticket = ticket
        self.directory = directory
        self.year = str(datetime.date.today().year)
        self.make_year_dir()
        self.today = str(datetime.date.today())
        self.make_day_dir()

    def make_year_dir(self):
        if self.year not in os.listdir(self.directory):
            os.mkdir('{}/{}'.format(self.directory, self.year))

    def make_day_dir(self):
        if self.today not in os.listdir('{}/{}'.format(self.directory, self.year)):
            os.mkdir('{}/{}/{}'.format(self.directory, self.year, self.today))
