import os
import time


class CloseTask:
    def __init__(self, directory):
        self.directory = directory

    def close(self):
        contents = self.open_file()
        self.parse_contents(contents)

    def open_file(self):
        with open('{}/.open'.format(self.directory), 'r') as open_file:
            return open_file.read().split('::')

    def parse_contents(self, contents):
        file_path = contents[0]
        project = contents[2]
        ticket = contents[3]
        company = contents[4]
        self.archive(file_path, project, ticket, company)

    def archive(self, file_path, project, ticket, company):
        with open(file_path, 'a') as ticket_file:
            ticket_file.write('\n' + str(int(time.time())))
            ticket_file.write('\np' + project)
            ticket_file.write('\nt' + ticket)
            ticket_file.write('\nc' + company + '\n')
        self.clear_open_file(ticket)

    def clear_open_file(self, ticket):
        os.remove('{}/.open'.format(self.directory))
        print('Ticket {} closed.'.format(ticket.split('__')[0]))
