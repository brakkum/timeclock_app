import datetime
import os

class Export():
    def __init__(self, directory, args):
        self.directory = directory
        self.args = args
        self.set_options()
        self.get_records()
        self.output_data()

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
        self.data = {}

    def output_data(self):
        print(self.data)

    def structure_data(self, data):
        # data[0, 1].strip data[2, 3][1:].strip() data[4][1:].strip()
        company = data[4][1:].strip()
        if company == '':
            company = 'none'
        project = data[2][1:].strip()
        if project == '':
            project = 'none'
        ticket = data[3][1:].strip().split('__')[0]
        if ticket == '':
            ticket = 'none'
        start_time = int(data[0].strip())
        end_time = int(data[1].strip())
        ticket_time = end_time - start_time
        ticket_entry = {ticket: ticket_time}
        project_entry = {project: ticket_entry}

        if company in self.data:
            if project in self.data[company]:
                if ticket in self.data[company][project]:
                    # ticket is here, add to total
                    self.data[company][project][ticket] += ticket_time
                else:
                    # ticket not here yet
                    self.data[company][project][ticket] = ticket_time
            else:
                # project not here yet
                self.data[company][project] = ticket_entry
        else:
            # company not here yet
            self.data[company] = project_entry

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
                    self.structure_data(item)
        except:
            print('That month has no records')

    def seconds_to_quarter_hours(self, seconds):
        hours = seconds / 3600
        quarters = round(hours / .25)
        return quarters * .25
