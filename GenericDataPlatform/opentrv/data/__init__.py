class Record(object):
    def __init__(self, name, value, unit=None, topic=None):
        # TODO: add timestamp
        self.name = name
        self.value = value
        self.unit = unit
        self.topic = topic

class Topic(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def path(self, sep='/'):
        if self.parent is None:
            return self.name
        else:
            return sep.join([self.parent.path(), self.name])