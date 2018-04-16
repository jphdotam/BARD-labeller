from settings.settings import settings

class Protocol:
    def __init__(self, name):
        self.name = name
        self.protocol = settings[name]
        self.type = self.protocol['type']
        self.ranges = self.protocol['ranges']
        self.markers = self.protocol['markers']