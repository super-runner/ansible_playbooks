#!/usr/bin/python3

def surround_by_quote(a_list):
    return ['"%s"' %x for x in a_list]

class FilterModule(object):
    def filters(self):
        return {'surround_by_quote': surround_by_quote}

if __name__ == '__main__':
  print ("{}".format(surround_by_quote(['jason','becky'])))

