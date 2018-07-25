import re
from sys import maxsize


# перед сравнением строк удаляем лишние пробелы в середине, в начале и в конце
def clear_extra_spaces(s):
    return re.sub(" +", " ", s.strip())


class Project:

    def __init__(self, pid=None, name=None, status=None, inherit=None, view_status=None, description=None):
        self.pid = pid
        self.name = name
        self.status = status
        self.inherit = inherit
        self.view_status = view_status
        self.description = description

    def __repr__(self):
        return "%s: %s (%s, %s, %s)\n" % (self.pid, self.name, self.status, self.view_status, self.description)

    def __eq__(self, other):
        return (self.pid is None or other.pid is None or str(self.pid) == str(other.pid)) and \
               clear_extra_spaces(self.name) == clear_extra_spaces(other.name)

    def pid_or_max(self):
        if self.pid:
            return int(self.pid)
        else:
            return maxsize

    def clean_project(self):
        if self.name is not None:
            self.name = clear_extra_spaces(self.name)
        if self.description is not None:
            self.description = clear_extra_spaces(self.description)
        return self
