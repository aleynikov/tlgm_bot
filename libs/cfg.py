import os
import ConfigParser

class Cfg:
    def __init__(self, filename):
        self.config = ConfigParser.RawConfigParser()
        self.path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../cfg')
        # read config
        self.config.read("%s/%s.cfg" % (self.path, filename))

    def get(self, section, option):
        if self.config.has_section(section):
            if self.config.has_option(section, option):
                return self.config.get(section, option)

        return None

    def get_sections(self):
        return self.config.sections()

    def get_options(self, section):
        if self.config.has_section(section):
            return self.config.options(section)
        else:
            return None
