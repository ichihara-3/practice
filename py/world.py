# coding: utf-8

class country(object):

    def __init__(self, capital=''):
        self.name=self.__class__.__name__
        self.capital=capital

class Japan(country):

    def __init__(self):
        super(Japan, self).__init__(capital='Tokyo')

if __name__ == '__main__':
    jp = Japan()
    print(jp.name)
    print(jp.capital)
