import datetime
import os

class Export():
    def __init__(self, directory, args):
        self.directory = directory
        self.args = args
        self.month = self.args.month if self.args.month else datetime.date.today().month
        self.year = self.args.year if self.args.year else datetime.date.today().year
        self.month_dir = '{}/{}/{}'.format(self.directory, self.year, self.month)
        self.hours = self.get_month_total()
        print(self.hours)

    def get_month_total(self):
        days_worked = [x for x in os.listdir(self.month_dir) if x != '.DS_Store']
        seconds = 0
        for days in days_worked:
            day_items = [x for x in os.listdir('{}/{}'.format(self.month_dir, days)) if x != '.DS_Store']
            for items in day_items:
                item = open('{}/{}/{}'.format(self.month_dir, days, items)).readlines()
                start_time = int(item[0])
                end_time = int(item[1])
                seconds += end_time - start_time
        return self.seconds_to_quarter_hours(seconds)

    def seconds_to_quarter_hours(self, seconds):
        hours = seconds / 3600
        quarters = round(hours / .25)
        return quarters * .25
