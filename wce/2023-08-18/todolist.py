
class TodoList:

    def __init__(self):
        self._size = 0
        self._items = []
        self._dones = []

    def push(self, item: str):
        self._size += 1
        self._items.append(item)
        self._dones.append(False)

    def pop(self, index: int) -> str:
        self._size -= 1
        self._dones.pop(index)
        return self._items.pop(index)

    def list_todo(self) -> list:
        return [self._items[i] for i in range(self._size) if not self._dones[i]]

    def make_done(self, index: int):
        self._dones[index] = True

    def is_done(self, index: int) -> bool:
        return self._dones[index]

    def list_done(self) -> list:
        return [self._items[i] for i in range(self._size) if self._dones[i]]

    @property
    def size(self):
        return self._size
