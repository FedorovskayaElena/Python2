from model.project import Project
import random
import string


def random_string(postfix, maxlen):
    s = "".join([random.choice(string.ascii_letters + string.digits + " "*6) for i in range(random.randrange(maxlen))])
    return s + postfix


statuses = ['development', 'release', 'stable', 'obsolete']
inherits = [False, True]
view_statuses = ['public', 'private']


testdata = [Project(name="Тестовое имя", description="Тестовое описание",
                    status=statuses[1], inherit=inherits[1], view_status=view_statuses[1])] + \
           [Project(name=random_string("name", 20), description=random_string("header", 40),
                    status=random.choice(statuses), inherit=random.choice(inherits),
                    view_status=random.choice(view_statuses)) for i in range(0, 5)]

