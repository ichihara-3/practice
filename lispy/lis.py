# coding: utf-8
# ((Pythonで) 書く (Lisp) インタプリタ) を参考。
# http://www.aoky.net/articles/peter_norvig/lispy.htm
#
# original: (How to Write a (Lisp) Interpreter (in Python))
# http://norvig.com/lispy.html

import math
import operator as op
import sys


isa = isinstance
Symbol = str


class Env(dict):

    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self._outer = outer

    def find(self, var):
        return self if var in self else self._outer.find(var)


def add_globals(env):

    env.update(vars(math))
    env.update(
        {
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
            'not': op.not_, '>': op.gt, '<': op.lt, '>=': op.ge,
            '<=': op.le, '=': op.eq, 'equal?': op.eq, 
            'eq?': op.is_, 'car': lambda x: x[0], 
            'cdr': lambda x: x[1:], 'append': op.add,
            'list': lambda *x: list(x), 
            'list?': lambda x: isa(x, list),
            'null?': lambda x: x==[],
            'symbol?': lambda x: isa(x, Symbol)
        }
    )
    return env

global_env = add_globals(Env())


def eval(x, env=global_env):
    if isa(x, Symbol):
        return env.find(x)[x]
    elif not isa(x, list):
        return x
    elif x[0] == 'quote':
        _, exp = x
        return exp
    elif x[0] == 'if':
        _, test, conseq, alt = x
        return eval(conseq if eval(test, env) else alt, env)
    elif x[0] == 'set!':
        _, var, exp = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'define':
        _, var, exp = x
        env[var] = eval(exp, env)
    elif x[0] == 'lambda':
        _, vars, exp = x
        return lambda *args: eval(exp, Env(vars, args, env))
    elif x[0] == 'begin':
        for exp in x[1:]:
            val = eval(exp, env)
        return val
    else:
        exps = [eval(exp, env) for exp in x]
        proc = exps.pop(0)
        return proc(*exps)


def read(s):
    return read_from(tokenize(s))

parse = read


def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()


def read_from(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from(tokens))
        # pop off ')'
        tokens.pop(0)
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def to_string(exp):
    return '({})'.format(' '.join(map(to_string, exp))) if isa(exp, list) else str(exp)



prompt = 'lis.py> '


def repl():
    while True:
        val = input(prompt)
        print(to_string(eval(parse(val))))


if __name__ == '__main__':
    repl()
