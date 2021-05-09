#!/usr/bin/env python3
import os.path as path


class Plugin:
    def __init__(self, incoming=False, options=None, verbose=False):
        self.incoming = incoming
        self.len = 16
        if options is not None:
            if 'length' in options.keys():
                self.len = int(options['length'])

    def execute(self, data):
        # http://code.activestate.com/recipes/142812-hex-dumper/
        result = []
        digits = 2
        for i in range(0, len(data), self.len):
            s = data[i:i + self.len]
            hexa = ' '.join(['%0*X' % (digits, x) for x in s])
            text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
            result.append("%04X   %-*s   %s" % (i, self.len * (digits + 1), hexa, text))
        print(">>>" if not self.incoming else "<<<")
        print("\n".join(result))
        return data