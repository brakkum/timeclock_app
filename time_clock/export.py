import datetime
import os

class Export():
    def __init__(self, directory, args):
        self.directory = directory
        self.args = args
        self.set_options()
        self.get_records()

    def set_options(self):
        self.month = self.args.month if self.args.month else datetime.date.today().month
        self.year = self.args.year if self.args.year else datetime.date.today().year
        self.month_dir = '{}/{}/{}'.format(self.directory, self.year, self.month)
        self.project = self.args.project if self.args.project else None
        self.ticket = self.args.ticket if self.args.ticket else None
        self.company = self.args.company if self.args.company else None
        if self.ticket and '__' in self.ticket:
            self.ticket = self.ticket.replace('__', '_')
        if self.ticket and '_' in self.ticket:
            self.ticket = self.ticket.replace('_', '-')

    # TODO Export all outputs table with descriptors
    def get_records(self):
        try:
            days_worked = [x for x in os.listdir(self.month_dir) if x != '.DS_Store']
            seconds = 0
            for days in days_worked:
                day_items = [x for x in os.listdir('{}/{}'.format(self.month_dir, days)) if x != '.DS_Store']
                for items in day_items:
                    item = open('{}/{}/{}'.format(self.month_dir, days, items)).readlines()
                    if self.company:
                        if item[4].strip('\n') == 'c{}'.format(self.company):
                            pass
                        else:
                            continue
                    if self.ticket:
                        if item[3].strip('\n').split('__')[0] == 't{}'.format(self.ticket):
                            pass
                        else:
                            continue
                    if self.project:
                        if item[2].strip('\n') == 'p{}'.format(self.project):
                            pass
                        else:
                            continue
                    seconds += int(item[1]) - int(item[0])
            if seconds == 0:
                print('No time found')
            else:
                print(self.seconds_to_quarter_hours(seconds))
        except:
            print('That month has no records')

    def seconds_to_quarter_hours(self, seconds):
        hours = seconds / 3600
        quarters = round(hours / .25)
        return quarters * .25
