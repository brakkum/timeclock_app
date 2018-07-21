import os
import time

class CloseTask():
    def __init__(self, directory):
        self.directory = directory
        self.contents = self.open_file()
        self.file_path = self.contents[0]
        self.start_time = self.contents[1]
        self.archive()
        self.clear_open()

    def open_file(self):
        open_file = open('{}/.open'.format(self.directory), 'r')
        contents = open_file.read().split('::')
        open_file.close()
        return contents

    def archive(self):
        ticket_file = open(self.file_path, 'a')
        ticket_file.write('\n' + str(int(time.time())))
        ticket_file.close()

    def clear_open(self):
        os.remove('{}/.open'.format(self.directory))