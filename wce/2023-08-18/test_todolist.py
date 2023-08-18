import pytest

from todolist import TodoList


class TestTodoList:

    def test_push(self):
        todo = TodoList()
        todo.push('test')
        assert todo.size == 1
        todos = todo.list_todo()
        assert len(todos) == 1
        assert todos[0] == 'test'

    def test_push_multiple(self):
        todo = TodoList()
        todo.push('test')
        todo.push('test2')
        assert todo.size == 2
        todos = todo.list_todo()
        assert len(todos) == 2
        assert todos[0] == 'test'

    def test_pop(self):
        todo = TodoList()
        todo.push('test')
        assert todo.pop(0) == 'test'

    def test_make_done(self):
        todo = TodoList()
        todo.push('test')
        todo.make_done(0)
        assert todo.is_done(0)

    def test_list_done(self):
        todo = TodoList()
        todo.push('test')
        todo.make_done(0)
        assert todo.list_done() == ['test']

    def test_list_todo(self):
        todo = TodoList()
        todo.push('test')
        todo.make_done(0)
        assert todo.list_todo() == []
