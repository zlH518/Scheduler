import os

class CPrintl():
    def __init__(self, logName) -> None:
        self.log_file = logName
        if os.path.dirname(logName) != '' and not os.path.exists(os.path.dirname(logName)):
            os.makedirs(os.path.dirname(logName))

    def __call__(self, *args):
        print(*args)
        print(*args, file=open(self.log_file, 'a'))

    def clear(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)