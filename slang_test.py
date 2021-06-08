################ Tests for lis.py

lis_tests = [
    ("(+ 2 2)", 4),
    ("(+ (* 2 100) (* 1 10))", 210),
    ("(if (> 6 5) (+ 1 1) (+ 2 2))", 2),
    ("(if (< 6 5) (+ 1 1) (+ 2 2))", 4),
    ("(let x 3)", None), ("x", 3), ("(+ x x)", 6),
    ("(fun twice (x) (* 2 x))", None), ("(twice 5)", 10),
    ("(fun fact (n) (if (<= n 1) 1 (* n (fact (- n 1)))))", None),
    ("(fact 3)", 6),
    ("(fact 50)", 30414093201713378043612608166064768844377641568960512000000000000),
    ("(fun abs (n) ((if (> n 0) + -) 0 n))", None),
    ]

def test(tests, name=''):
    "For each (exp, expected) test case, see if evaluate(parse(exp)) == expected."
    fails = 0
    for (x, expected) in tests:
        try:
            result = evaluate(parse(x))
            print(x, '=>', sexp(result))
            ok = (result == expected)
        except Exception as e:
            print(x, '=raises=>', type(e).__name__, e)
            ok = isinstance(expected, type) and issubclass(expected, Exception) and isinstance(e, expected)
        if not ok:
            fails += 1
            print('FAIL!!!  Expected', expected)
    print('%s %s: %d out of %d tests fail.' % ('*'*45, name, fails, len(tests)))

if __name__ == '__main__':
    from slang import *
    test(lis_tests, 'lis.py')

