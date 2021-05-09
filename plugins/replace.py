import os

class Plugin:
    def __init__(self, incoming=False, options=None, verbose=False):
        self.search = None
        self.replace = None
        self.filename = None
        self.separator = ":::"

        if(options is not None):
            if 'search' in options.keys():
                self.search = options['search'].encode() if isinstance(options['search'], str) else options['search']
            if 'replace' in options.keys():
                self.replace = options['replace'].encode() if isinstance(options['replace'], str) else options['replace']
            if 'file' in options.keys():
                self.filename = options['file'].encode() if isinstance(options['file'], str) else options['file']
                try:
                    open(self.filename)
                except IOError as ioe:
                    print("Error opening %s: %s" % (self.filename, ioe.strerror))
                    self.filename = None
            if 'separator' in options.keys():
                self.separator = options['separator'].encode() if isinstance(options['seperator'], str) else options['seperator']


    def execute(self, data):
        pairs = []  # list of (search, replace) tuples
        if self.search is not None and self.replace is not None:
            pairs.append((self.search, self.replace))

        if self.filename is not None:
            for line in open(self.filename).readlines():
                try:
                    search, replace = line.split(self.separator, 1)
                    pairs.append((bytes(search.strip(), 'ascii'), bytes(replace.strip(), 'ascii')))
                except ValueError:
                    pass
        for search, replace in pairs:
            data = data.replace(search, replace)
        return data
    
    def help(self):
        print("HELP HERE")
