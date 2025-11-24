import sys
import os
from lark import Lark, Transformer

# read grammar
parser = Lark(open("grammar.lark").read(), parser="lalr")

# ast builder
class LambdaCalculusTransformer(Transformer):
    def var(self, args):
        return ('var', str(args[0]))

    def lam(self, args):
        return ('lam', str(args[0]), args[1])

    def app(self, args):
        # initial application node as given by the parser
        return ('app', args[0], args[1])


# pretty printer
def linearize(t, top=True):
    tag = t[0]

    if tag == 'var':
        return t[1]

    if tag == 'lam':
        body = linearize(t[2], top=False)
        s = f"(\\{t[1]}.{body})"
        return s if top else s

    if tag == 'app':
        f = linearize(t[1], top=False)
        a = linearize(t[2], top=False)
        s = f"{f} {a}"
        return s if top else f"({s})"

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
        while True:
            self.c += 1
            x = f"x{self.c}"
            if x not in used:
                return x


ng = NameGen()


# capture avoiding substitution
def substitute(t, name, rep):
    tag = t[0]

    if tag == 'var':
        return rep if t[1] == name else t

    if tag == 'lam':
        v, body = t[1], t[2]
        if v == name:
            # bound variable shadows the name we want to replace
            return t
        if v in free_vars(rep):
            # avoid capture by renaming
            used = free_vars(body) | free_vars(rep) | {v, name}
            fresh = ng.fresh(used)
            renamed = substitute(body, v, ('var', fresh))
            return ('lam', fresh, substitute(renamed, name, rep))
        return ('lam', v, substitute(body, name, rep))

    if tag == 'app':
        return ('app',
                substitute(t[1], name, rep),
                substitute(t[2], name, rep))

    return t


# normalize application: make it LEFT-associative
#
# Example:
#   app(a, app(b, app(c, d)))  ==>  app(app(app(a, b), c), d)
#   (\x.\y.x) a b              ==>  ((\x.\y.x) a) b
def normalize_applications(t):
    tag = t[0]

    if tag == 'app':
        nodes = []

        def collect(u):
            if u[0] == 'app':
                collect(u[1])
                collect(u[2])
            else:
                # recursively normalize inside non-app nodes
                nodes.append(normalize_applications(u))

        collect(t)

        # build left-nested application chain
        res = nodes[0]
        for arg in nodes[1:]:
            res = ('app', res, arg)
        return res

    if tag == 'lam':
        return ('lam', t[1], normalize_applications(t[2]))

    # variable or other
    return t


# ONE NORMAL-ORDER STEP
def step(t):
    tag = t[0]

    # variable – no reduction
    if tag == 'var':
        return t, False

    # lambda – reduce body
    if tag == 'lam':
        body, changed = step(t[2])
        return ('lam', t[1], body), changed

    # application
    if tag == 'app':
        f, a = t[1], t[2]

        # CASE 1: beta-reduction
        if f[0] == 'lam':
            v, body = f[1], f[2]
            return substitute(body, v, a), True

        # CASE 2: reduce function first
        new_f, changed = step(f)
        if changed:
            return ('app', new_f, a), True

        # CASE 3: reduce argument
        new_a, changed = step(a)
        return ('app', f, new_a), changed

    return t, False


MAX_STEPS = 10000  # safety limit to detect non-terminating terms


# repeat until no more reductions or we hit the step limit
def evaluate(t):
    changed = True
    steps = 0
    while changed and steps < MAX_STEPS:
        t, changed = step(t)
        steps += 1

    if changed:
        # still reducible but we hit the limit: treat as non-terminating
        raise RuntimeError("non-terminating")

    return t


# run interpreter
def interpret(src):
    cst = parser.parse(src)
    ast = LambdaCalculusTransformer().transform(cst)

    # fix associativity of application
    ast = normalize_applications(ast)

    try:
        out = evaluate(ast)
        return linearize(out, top=True)
    except RuntimeError:
        # requested behaviour for non-terminating terms
        return "<non-terminating>"


# cli
def main():
    if len(sys.argv) != 2:
        print('usage: interpreter.py "<expr>" or interpreter.py file.lc')
        sys.exit(1)

    arg = sys.argv[1]

    if os.path.isfile(arg):
        src = open(arg).read()
    else:
        src = arg

    print(interpret(src))


if __name__ == "__main__":
    main()
