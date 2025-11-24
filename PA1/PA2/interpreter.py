import sys
import os
from lark import Lark, Transformer

# read grammar
with open("grammar.lark") as f:
    _GRAMMAR = f.read()
parser = Lark(_GRAMMAR, parser="lalr")


# ast builder
class LambdaCalculusTransformer(Transformer):
    def var(self, args):
        # variable
        return ('var', str(args[0]))

    def lam(self, args):
        # lambda abstraction
        name = str(args[0])
        body = args[1]
        return ('lam', name, body)

    def app(self, args):
        # application
        return ('app', args[0], args[1])


# pretty printer
def linearize(t):
    tag = t[0]
    if tag == 'var':
        return t[1]
    if tag == 'lam':
        return f"(\\{t[1]}.{linearize(t[2])})"
    if tag == 'app':
        f = t[1]
        a = t[2]
        f_str = linearize(f)
        a_str = linearize(a)
        # add parens where needed
        if f[0] == 'lam':
            f_str = f"({f_str})"
        if a[0] in ('lam', 'app'):
            a_str = f"({a_str})"
        return f"{f_str} {a_str}"
    # should not happen
    return "?"


# free vars
def free_vars(t):
    tag = t[0]
    if tag == 'var':
        return {t[1]}
    if tag == 'lam':
        return free_vars(t[2]) - {t[1]}
    if tag == 'app':
        return free_vars(t[1]) | free_vars(t[2])
    return set()


# fresh names
class NameGen:
    def __init__(self):
        self.c = 0

    def fresh(self, used):
        # generate x1, x2, x3, ... not in used
        while True:
            self.c += 1
            name = f"x{self.c}"
            if name not in used:
                return name


ng = NameGen()


# capture avoiding substitution
def substitute(t, name, rep):
    tag = t[0]

    # variable
    if tag == 'var':
        if t[1] == name:
            return rep
        return t

    # lambda abstraction
    if tag == 'lam':
        v, body = t[1], t[2]

        # bound variable shadows name
        if v == name:
            return t

        # avoid capture
        if v in free_vars(rep):
            used = free_vars(body) | free_vars(rep) | {name, v}
            fresh_v = ng.fresh(used)
            renamed_body = substitute(body, v, ('var', fresh_v))
            return ('lam', fresh_v, substitute(renamed_body, name, rep))

        return ('lam', v, substitute(body, name, rep))

    # application
    if tag == 'app':
        return (
            'app',
            substitute(t[1], name, rep),
            substitute(t[2], name, rep),
        )

    return t


# one normal-order reduction step
def step(t):
    tag = t[0]

    # variables are already in normal form
    if tag == 'var':
        return t, False

    # reduce under lambda (needed for full normalisation)
    if tag == 'lam':
        body, did = step(t[2])
        if did:
            return ('lam', t[1], body), True
        return t, False

    # application
    if tag == 'app':
        f, a = t[1], t[2]

        # outermost beta-redex
        if f[0] == 'lam':
            param = f[1]
            body = f[2]
            return substitute(body, param, a), True

        # otherwise reduce the function first
        new_f, did = step(f)
        if did:
            return ('app', new_f, a), True

        # finally reduce the argument
        new_a, did = step(a)
        if did:
            return ('app', f, new_a), True

        return t, False

    return t, False


# repeat steps until normal form
def evaluate(t):
    while True:
        t2, did = step(t)
        if not did:
            return t2
        t = t2


# parse + eval one expression
def interpret_expr(src):
    cst = parser.parse(src)
    ast = LambdaCalculusTransformer().transform(cst)
    out = evaluate(ast)
    return linearize(out)


# cli
def main():
    if len(sys.argv) != 2:
        print('usage: interpreter.py "(\\x.x) a" or interpreter.py file.lc')
        sys.exit(1)

    arg = sys.argv[1]

    if os.path.isfile(arg):
        with open(arg) as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]
        for i, line in enumerate(lines):
            result = interpret_expr(line)
            # one result per line, no extra junk
            end = "" if i == len(lines) - 1 else "\n"
            print(result, end=end)
    else:
        print(interpret_expr(arg))


if __name__ == "__main__":
    main()
