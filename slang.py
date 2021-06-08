################ Lispy: Scheme Interpreter in Python 3.10

## (c) Peter Norvig, 2010-18; See http://norvig.com/lispy.html
## Ported to Python 3.10 with Pattern Matching by Luciano Ramalho

import operator as op
from collections import ChainMap, deque

################ Parsing: parse, tokenize, and build_ast

def parse(program):
    "Read an s-expression from a string."
    return build_ast(tokenize(program))

def tokenize(s):
    "Convert a string into a sequence of tokens."
    return deque(s.replace('(',' ( ').replace(')',' ) ').split())

def build_ast(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.popleft()
    if '(' == token:
        new_list = []
        while tokens[0] != ')':
            new_list.append(build_ast(tokens))
        tokens.popleft() # drop ')'
        return new_list
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return token

################ Interaction: A REPL

def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        val = evaluate(parse(input(prompt)))
        if val is not None:
            print(sexp(val))

def sexp(exp):
    "Convert a Python object back into an s-expresion string."
    if isinstance(exp, list):
        return '(' + ' '.join(map(sexp, exp)) + ')'
    else:
        return str(exp)

################ evaluate

class Function(object):
    "A user-defined function."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        env =  ChainMap(dict(zip(self.parms, args)), self.env)
        return evaluate(self.body, env)

global_env = {
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
    }

def evaluate(x, env=global_env):
    match x:
        case str():                                   # variable reference
            return env[x]
        case ['if', test, conseq, alt]:               # (if test conseq alt)
            exp = conseq if evaluate(test, env) else alt
            return evaluate(exp, env)
        case ['let', var, exp]:                       # (let var exp)
            env[var] = evaluate(exp, env)
        case ['fun', name, parms, body]:              # (fun name (var...) body)
            fun = Function(parms, body, env)
            env[name] = fun
        case [op, *args]:                             # (op arg...)
            proc = evaluate(op, env)
            values = (evaluate(arg, env) for arg in args)
            return proc(*values)
        case literal if not isinstance(x, list):      # constant literal
            return literal
        case _:
            SyntaxError(f'Invalid syntax: {x!r}')
