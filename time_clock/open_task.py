from time_clock.config_funcs import get_config_setting
import datetime
import time
import os

class OpenTask():
    def __init__(self, directory, args):
        self.args = args
        self.ticket = self.args.ticket
        if '__' in self.ticket:
            self.ticket = self.ticket.replace('__', '_')
        if '_' in self.ticket:
            self.ticket = self.ticket.replace('_', '-')
        self.directory = directory
        self.project = self.args.project if self.args.project else ''
        self.company = self.args.company if self.args.company else ''
        if get_config_setting('strict') and (not self.args.project or not self.args.company):
            print('Strict mode, please supply project and company.')
            return
        self.make_directories()
        self.make_unique_ticket()
        self.start()

    def make_directories(self):
        self.year = str(datetime.date.today().year)
        self.make_year_dir()
        self.month = str(datetime.date.today().month)
        self.make_month_dir()
        self.today = str(datetime.date.today().day)
        self.make_day_dir()
        self.day_dir = '{}/{}/{}/{}'.format(self.directory, self.year, self.month, self.today)

    def make_year_dir(self):
        if self.year not in os.listdir(self.directory):
            os.mkdir('{}/{}'.format(self.directory, self.year))

    def make_month_dir(self):
        if self.month not in os.listdir('{}/{}/'.format(self.directory, self.year)):
            os.mkdir('{}/{}/{}'.format(self.directory, self.year, self.month))

    def make_day_dir(self):
        if self.today not in os.listdir('{}/{}/{}'.format(self.directory, self.year, self.month)):
            os.mkdir('{}/{}/{}/{}'.format(self.directory, self.year, self.month, self.today))

    def make_unique_ticket(self):
        if self.ticket in os.listdir(self.day_dir):
            self.ticket += '__{}'.format(datetime.datetime.now().strftime("%I:%M%p").replace(':', '_'))
        self.ticket_path = '{}/{}'.format(self.day_dir, self.ticket)

    def start(self):
        open_file = open('{}/.open'.format(self.directory), 'a')
        open_file.write(self.ticket_path + '::') #path to ticket
        open_file.write(str(int(time.time())) + '::') #time
        open_file.write(self.project + '::') # project
        open_file.write(self.ticket + '::') # ticket
        open_file.write(self.company + '::') # company
        open_file.close()
        print('Started working on {} at {}'.format(self.ticket, datetime.datetime.now().strftime("%I:%M%p")))
        self.make_archive()

    def make_archive(self):
        archive = open(self.ticket_path, 'w')
        archive.write(str(int(time.time())))
        archive.close()