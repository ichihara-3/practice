import unittest
from todolist import TodoList


class TestTodoList(unittest.TestCase):

    def test_todo_nothing(self):
        todlist = TodoList()
