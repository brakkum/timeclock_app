import datetime
import os


class Export:
    def __init__(self, directory, args):
        self.directory = directory
        self.args = args
        self.month = self.args.month if self.args.month else datetime.date.today().month
        self.year = self.args.year if self.args.year else datetime.date.today().year
        self.month_dir = '{}/{}/{}'.format(self.directory, self.year, self.month)
        self.project = self.args.project if self.args.project else None
        self.ticket = self.args.ticket if self.args.ticket else None
        self.company = self.args.company if self.args.company else None
        self.data = {}

    def output_data(self):
        grand_total = 0
        if self.data:
            for company in self.data:
                print('{:-^50}'.format(''))
                print('{:-^50}'.format(' Company: ' + company + ' '))
                print('{:-^50}'.format(''))
                company_total = 0
                for project in self.data[company]:
                    print('{:15}{:^35s}'.format('', 'Project {}'.format(project)))
                    project_total = 0
                    print('{:>50}'.format('-' * 36))
                    for ticket in self.data[company][project]:
                        ticket_time = self.seconds_to_quarter_hours(self.data[company][project][ticket])
                        print('{0:>42s}: {1:^6.2f}'.format(ticket, ticket_time))
                        project_total += ticket_time
                    print('{:>50}'.format('-' * 36))
                    print('{:15}{:^35s}'.format('', 'Project: {}\n'.format(project_total)))
                    company_total += project_total
                print('{:^50}'.format(company + ' total: ' + str(company_total)))
                grand_total += company_total
            print('{:-^50}'.format(''))
            print('{:|^50}'.format(' Grand total: ' + str(grand_total) + ' '))
            print('{:-^50}'.format(''))
        else:
            print('No matches found.')

    def strip_beginning_and_end(self, chunk):
        return chunk[1:].strip().split('__')[0]

    def structure_data(self, data):
        company = self.strip_beginning_and_end(data[4])
        if not company:
            company = 'none'
        project = self.strip_beginning_and_end(data[2])
        if not project:
            project = 'none'
        ticket = self.strip_beginning_and_end(data[3])
        if not ticket:
            ticket = 'none'
        ticket_time = int(data[1].strip()) - int(data[0].strip())
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

    def get_records(self):
        if self.ticket and '__' in self.ticket:
            self.ticket = self.ticket.replace('__', '_')
        if self.ticket and '_' in self.ticket:
            self.ticket = self.ticket.replace('_', '-')
        try:
            days_worked = [x for x in os.listdir(self.month_dir) if x != '.DS_Store']
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
            self.output_data()
        except:
            print('That month has no records')

    def seconds_to_quarter_hours(self, seconds):
        return round((seconds / 3600) / .25) * .25
