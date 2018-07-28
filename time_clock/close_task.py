import os
import time

class CloseTask():
    def __init__(self, directory):
        self.directory = directory
        self.contents = self.open_file()
        self.parse_contents()
        self.archive()
        self.clear_open_file()

    def open_file(self):
        open_file = open('{}/.open'.format(self.directory), 'r')
        contents = open_file.read().split('::')
        open_file.close()
        return contents

    def parse_contents(self):
        self.file_path = self.contents[0]
        self.start_time = self.contents[1]
        self.project = self.contents[2]
        self.ticket = self.contents[3]
        self.company = self.contents[4]

    def archive(self):
        ticket_file = open(self.file_path, 'a')
        ticket_file.write('\n' + str(int(time.time())))
        ticket_file.write('\np' + self.project)
        ticket_file.write('\nt' + self.ticket)
        ticket_file.write('\nc\n' + self.company)
        ticket_file.close()

    def clear_open_file(self):
        os.remove('{}/.open'.format(self.directory))
        print('Ticket {} closed.'.format(self.ticket))
