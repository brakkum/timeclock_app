import datetime
import os

class Export():
    def __init__(self, directory, args):
        self.directory = directory
        self.args = args
        self.set_options()
        self.hours_worked = self.return_hours()
        print(self.hours_worked)

    def set_options(self):
        self.month = self.args.month if self.args.month else datetime.date.today().month
        self.year = self.args.year if self.args.year else datetime.date.today().year
        self.month_dir = '{}/{}/{}'.format(self.directory, self.year, self.month)
        self.project = self.args.project if self.args.project else ''
        self.ticket = self.args.ticket if self.args.ticket else ''


    def return_hours(self):
        if self.project:
            return self.get_project_total()
        elif self.ticket:
            return self.get_ticket_total()
        else:
            return self.get_month_total()

    def get_ticket_total(self):
        seconds = 0
        total_days = [x for x in os.listdir(self.month_dir) if x != '.DS_Store']
        for days in total_days:
            for items in os.listdir('{}/{}'.format(self.month_dir, days)):
                day = open('{}/{}/{}'.format(self.month_dir, days, items), 'r').readlines()
                if day[3].strip('\n').startswith('t{}'.format(self.ticket)):
                    seconds += int(day[1]) - int(day[0])
        return self.seconds_to_quarter_hours(seconds)

    def get_project_total(self):
        seconds = 0
        total_days = [x for x in os.listdir(self.month_dir) if x != '.DS_Store']
        for days in total_days:
            for items in os.listdir('{}/{}'.format(self.month_dir, days)):
                day = open('{}/{}/{}'.format(self.month_dir, days, items), 'r').readlines()
                if day[2].strip('\n') == 'p{}'.format(self.project):
                    seconds += int(day[1]) - int(day[0])
        return self.seconds_to_quarter_hours(seconds)

    def get_month_total(self):
        days_worked = [x for x in os.listdir(self.month_dir) if x != '.DS_Store']
        seconds = 0
        for days in days_worked:
            day_items = [x for x in os.listdir('{}/{}'.format(self.month_dir, days)) if x != '.DS_Store']
            for items in day_items:
                item = open('{}/{}/{}'.format(self.month_dir, days, items)).readlines().rstrip()
                start_time = int(item[0])
                end_time = int(item[1])
                seconds += end_time - start_time
        return self.seconds_to_quarter_hours(seconds)

    def seconds_to_quarter_hours(self, seconds):
        hours = seconds / 3600
        quarters = round(hours / .25)
        return quarters * .25
