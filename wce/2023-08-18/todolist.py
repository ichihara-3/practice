
class TodoList:

    def __init__(self):
        self._size = 0

    def add(self, item):
        self._size += 1

    @property
    def size(self):
        return self._size
