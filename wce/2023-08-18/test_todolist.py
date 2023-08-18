import pytest

from todolist import TodoList


class TestTodoList:

    def test_todo_add(self):
        _todo = TodoList()
        _todo.add('test')
        assert _todo.size == 1

    def test_todo_add_multiple(self):
        _todo = TodoList()
        _todo.add('test')
        _todo.add('test2')
        assert _todo.size == 2
