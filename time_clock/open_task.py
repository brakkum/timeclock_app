from time_clock.config_funcs import get_config_setting
import datetime
import time
import os


class OpenTask:
    def __init__(self, directory, args):
        self.args = args
        self.ticket = self.args.ticket
        self.check_for_underscores()
        self.directory = directory
        self.project = self.args.project if self.args.project else ''
        self.company = self.args.company if self.args.company else ''
        if self.is_strict():
            print('Strict mode, please supply project and company.')
        else:
            self.make_directories()
            self.add_time_to_ticket()
            self.start()

    def is_strict(self):
        if get_config_setting('strict') and (not self.project or not self.company):
            return True
        else:
            return False

    def check_for_underscores(self):
        if '__' in self.ticket:
            self.ticket = self.ticket.replace('__', '_')
        if '_' in self.ticket:
            self.ticket = self.ticket.replace('_', '-')

    def make_directories(self):
        self.make_year_dir()
        self.make_month_dir()
        self.make_day_dir()
        self.day_dir = '{}/{}/{}/{}'.format(self.directory, self.year, self.month, self.today)

    def make_year_dir(self):
        self.year = str(datetime.date.today().year)
        if self.year not in os.listdir(self.directory):
            os.mkdir('{}/{}'.format(self.directory, self.year))

    def make_month_dir(self):
        self.month = str(datetime.date.today().month)
        if self.month not in os.listdir('{}/{}/'.format(self.directory, self.year)):
            os.mkdir('{}/{}/{}'.format(self.directory, self.year, self.month))

    def make_day_dir(self):
        self.today = str(datetime.date.today().day)
        if self.today not in os.listdir('{}/{}/{}'.format(self.directory, self.year, self.month)):
            os.mkdir('{}/{}/{}/{}'.format(self.directory, self.year, self.month, self.today))

    def add_time_to_ticket(self):
        self.ticket += '__{}'.format(datetime.datetime.now().strftime("%I:%M%p").replace(':', '_'))
        self.ticket_path = '{}/{}'.format(self.day_dir, self.ticket)

    def start(self):
        with open('{}/.open'.format(self.directory), 'a') as open_file:
            open_file.write(self.ticket_path + '::')  # path to ticket
            open_file.write(str(int(time.time())) + '::')  # start time
            open_file.write(self.project + '::')  # project
            open_file.write(self.ticket + '::')  # ticket
            open_file.write(self.company + '::')  # company
        print('Started working on {} at {}'.format(self.ticket.split('__')[0], datetime.datetime.now().strftime("%I:%M%p")))
        self.make_archive()

    def make_archive(self):
        archive = open(self.ticket_path, 'w')
        archive.write(str(int(time.time())))
        archive.close()
