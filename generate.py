# abstraction λx.M
# application M N
# variable    x

import random
import numpy.random as npr

def generate(depth):
    def generate_ast(
        variables   = set(),
        depth       = 0,
        max_depth   = 10,
        force_depth = False,
    ):
        v = random.choice(
            list(variables)
            if len(variables) > 0 else
            'abcdefghijklmnopqrstuvwxyz'
        )
        r = random.random()
        if depth == max_depth: return v
        if force_depth:
            if r < 0.5:
                v = random.choice('abcdefghijklmnopqrstuvwxyz')
                return ('λ', v, generate_ast(variables | {v}, depth + 1, max_depth, force_depth))
            else:
                r = random.random()
                return (
                    generate_ast(variables, depth + 1, max_depth, r <  0.5),
                    generate_ast(variables, depth + 1, max_depth, r >= 0.5),
                )
        else:
            if r < 1/3:
                v = random.choice('abcdefghijklmnopqrstuvwxyz')
                return ('λ', v, generate_ast(variables | {v}, depth + 1, max_depth, force_depth))
            elif r < 2/3:
                r = random.random()
                return (
                    generate_ast(variables, depth + 1, max_depth, r <  0.5),
                    generate_ast(variables, depth + 1, max_depth, r >= 0.5),
                )
            else:
                return v

    def print_ast(ast, merge = False):
        match ast:
            case (f, x):
                ff = print_ast(f)
                xx = print_ast(x)
                if isinstance(f, tuple) and len(f) == 3:
                    ff = '(' + ff + ')'
                if isinstance(x, tuple):
                    xx = '(' + xx + ')'
                return ff + xx
            case ('λ', c, x):
                s = c
                if not merge: s = 'λ' + s
                merge_again = isinstance(x, tuple) and len(x) == 3
                if not merge_again: s = s + '.'
                return s + print_ast(x, merge_again)
            case s:
                return s

    ast = generate_ast(
        max_depth   = depth,
        force_depth = True,
    )
    return print_ast(ast)

if __name__ == '__main__':
    rng = npr.default_rng()
    for n in rng.normal(
        4,  # centre of the distribution
        1,  # standard deviation
        10, # number of expressions to generate
    ):
        print(generate(max(0, round(n))))
