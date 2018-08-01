from time_clock.config_funcs import get_config_setting
import datetime
import time
import os


class OpenTask:
    def __init__(self, directory, args):
        self.args = args
        self.ticket = self.args.ticket
        self.directory = directory
        self.project = self.args.project if self.args.project else ''
        self.company = self.args.company if self.args.company else ''
        self.year = str(datetime.date.today().year)
        self.year_dir = '{}/{}'.format(self.directory, self.year)
        self.month = str(datetime.date.today().month)
        self.month_dir = '{}/{}'.format(self.year_dir, self.month)
        self.today = str(datetime.date.today().day)
        self.day_dir = '{}/{}'.format(self.month_dir, self.today)
        self.ticket_path = '{}/{}'.format(self.day_dir, self.ticket)
        self.start_time = datetime.datetime.now().strftime("%I:%M%p")

    def open_new_ticket(self):
        if self.is_strict():
            print('Strict mode, please supply project and company.')
        else:
            self.check_for_underscores()
            self.make_directories()
            self.add_time_to_ticket_filename()
            self.start()

    def is_strict(self):
        return get_config_setting('strict') and (not self.project or not self.company)

    def check_for_underscores(self):
        if '__' in self.ticket:
            new_ticket = self.ticket.replace('__', '_')
            self.ticket_path.replace(self.ticket, new_ticket)
            self.ticket = new_ticket
        if '_' in self.ticket:
            new_ticket = self.ticket.replace('_', '-')
            self.ticket_path.replace(self.ticket, new_ticket)
            self.ticket = new_ticket

    def make_directories(self):
        self.make_year_dir()
        self.make_month_dir()
        self.make_day_dir()

    def make_year_dir(self):
        if self.year not in os.listdir(self.directory):
            os.mkdir(self.year_dir)

    def make_month_dir(self):
        if self.month not in os.listdir(self.year_dir):
            os.mkdir(self.month_dir)

    def make_day_dir(self):
        if self.today not in os.listdir(self.month_dir):
            os.mkdir(self.day_dir)

    def add_time_to_ticket_filename(self):
        self.ticket += '__{}'.format(datetime.datetime.now().strftime("%I:%M%p").replace(':', '_'))

    def start(self):
        with open('{}/.open'.format(self.directory), 'a') as open_file:
            open_file.write(self.ticket_path + '::')       # path to ticket
            open_file.write(str(int(time.time())) + '::')  # start time
            open_file.write(self.project + '::')           # project
            open_file.write(self.ticket + '::')            # ticket
            open_file.write(self.company + '::')           # company
        print('Started working on {} at {}'.format(self.ticket.split('__')[0], self.start_time))
        self.make_archive()

    def make_archive(self):
        archive = open(self.ticket_path, 'w')
        archive.write(str(int(time.time())))
        archive.close()
