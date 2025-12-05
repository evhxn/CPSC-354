import sys
import os
from lark import Lark, Transformer

# Parser

parser = Lark(open("grammar.lark").read(), parser="lalr")


class LambdaCalculusTransformer(Transformer):
    def start(self, args):
        return args[0]

    def var(self, args):
        return ("var", str(args[0]))

    def lam(self, args):
        return ("lam", str(args[0]), args[1])

    def app(self, args):
        return ("app", args[0], args[1])

    def num(self, args):
        return ("num", float(str(args[0])))

    def plus(self, args):
        return ("plus", args[0], args[1])

    def minus(self, args):
        return ("minus", args[0], args[1])

    def times(self, args):
        return ("times", args[0], args[1])

    def neg(self, args):
        return ("neg", args[0])

    def ifexpr(self, args):
        return ("if", args[0], args[1], args[2])

    def eq(self, args):
        return ("eq", args[0], args[1])

    def leq(self, args):
        return ("leq", args[0], args[1])

    def let(self, args):
        return ("let", str(args[0]), args[1], args[2])

    def letrec(self, args):
        return ("letrec", str(args[0]), args[1], args[2])

    def fix(self, args):
        return ("fix", args[0])

    def prog(self, args):
        return ("prog", args[0], args[1])

    def nil(self, args):
        return ("nil",)

    def cons(self, args):
        return ("cons", args[0], args[1])

    def hd(self, args):
        return ("hd", args[0])

    def tl(self, args):
        return ("tl", args[0])


# --------------------------------------------------------------------
# Pretty printer
# --------------------------------------------------------------------

def linearize(t, top=True):
    tag = t[0]

    if tag == "var":
        return t[1]

    if tag == "num":
        return str(t[1])

    if tag == "lam":
        body = linearize(t[2], top=False)
        s = f"(\\{t[1]}.{body})"
        return s

    if tag == "app":
        f = linearize(t[1], top=False)
        a = linearize(t[2], top=False)
        s = f"{f} {a}"
        # Always parenthesize applications to match tests
        return f"({s})"

    if tag == "plus":
        left = linearize(t[1], top=False)
        right = linearize(t[2], top=False)
        s = f"{left} + {right}"
        return f"({s})" if not top else s

    if tag == "minus":
        left = linearize(t[1], top=False)
        right = linearize(t[2], top=False)
        s = f"{left} - {right}"
        return f"({s})" if not top else s

    if tag == "times":
        left = linearize(t[1], top=False)
        right = linearize(t[2], top=False)
        s = f"{left} * {right}"
        return f"({s})" if not top else s

    if tag == "neg":
        inner = linearize(t[1], top=False)
        s = f"-{inner}"
        return s

    if tag == "if":
        cond = linearize(t[1], top=False)
        then_branch = linearize(t[2], top=False)
        else_branch = linearize(t[3], top=False)
        s = f"if {cond} then {then_branch} else {else_branch}"
        return s if top else f"({s})"

    if tag == "eq":
        left = linearize(t[1], top=False)
        right = linearize(t[2], top=False)
        s = f"{left} == {right}"
        return s if top else f"({s})"

    if tag == "leq":
        left = linearize(t[1], top=False)
        right = linearize(t[2], top=False)
        s = f"{left} <= {right}"
        return s if top else f"({s})"

    if tag == "let":
        var_name = t[1]
        value = linearize(t[2], top=False)
        body = linearize(t[3], top=False)
        s = f"let {var_name} = {value} in {body}"
        return s if top else f"({s})"

    if tag == "letrec":
        var_name = t[1]
        value = linearize(t[2], top=False)
        body = linearize(t[3], top=False)
        s = f"letrec {var_name} = {value} in {body}"
        return s if top else f"({s})"

    if tag == "fix":
        inner = linearize(t[1], top=False)
        s = f"fix {inner}"
        return s if top else f"({s})"

    if tag == "prog":
        # Since cons always adds its own parens now, just linearize both sides
        left = linearize(t[1], top=True)
        right = linearize(t[2], top=True)
        return f"{left} ;; {right}"

    if tag == "nil":
        return "#"

    if tag == "cons":
        head = linearize(t[1], top=False)
        tail = linearize(t[2], top=False)
        s = f"{head} : {tail}"
        # Always parenthesize cons expressions
        return f"({s})"

    if tag == "hd":
        inner = linearize(t[1], top=False)
        s = f"hd {inner}"
        # Always parenthesize hd
        return f"({s})"

    if tag == "tl":
        inner = linearize(t[1], top=False)
        s = f"tl {inner}"
        # Always parenthesize tl
        return f"({s})"

    return "?"


# --------------------------------------------------------------------
# Free variables and substitution
# --------------------------------------------------------------------

def free_vars(t):
    tag = t[0]

    if tag == "var":
        return {t[1]}

    if tag == "lam":
        return free_vars(t[2]) - {t[1]}

    if tag == "app":
        return free_vars(t[1]) | free_vars(t[2])

    if tag in ("plus", "minus", "times", "eq", "leq", "cons"):
        return free_vars(t[1]) | free_vars(t[2])

    if tag in ("neg", "hd", "tl"):
        return free_vars(t[1])

    if tag == "if":
        return free_vars(t[1]) | free_vars(t[2]) | free_vars(t[3])

    if tag == "let":
        var_name = t[1]
        return free_vars(t[2]) | (free_vars(t[3]) - {var_name})

    if tag == "letrec":
        var_name = t[1]
        return (free_vars(t[2]) | free_vars(t[3])) - {var_name}

    if tag == "fix":
        return free_vars(t[1])

    if tag == "prog":
        return free_vars(t[1]) | free_vars(t[2])

    if tag in ("num", "nil"):
        return set()

    return set()


class NameGen:
    def __init__(self):
        self.c = 0

    def fresh(self, used):
        while True:
            self.c += 1
            x = f"Var{self.c}"
            if x not in used:
                return x


ng = NameGen()


def substitute(t, name, rep):
    tag = t[0]

    if tag == "var":
        return rep if t[1] == name else t

    if tag == "lam":
        v, body = t[1], t[2]
        if v == name:
            return t
        if v in free_vars(rep):
            used = free_vars(body) | free_vars(rep) | {v, name}
            fresh = ng.fresh(used)
            renamed_body = substitute(body, v, ("var", fresh))
            return ("lam", fresh, substitute(renamed_body, name, rep))
        return ("lam", v, substitute(body, name, rep))

    if tag == "app":
        return (
            "app",
            substitute(t[1], name, rep),
            substitute(t[2], name, rep),
        )

    if tag in ("plus", "minus", "times", "eq", "leq", "cons"):
        return (
            tag,
            substitute(t[1], name, rep),
            substitute(t[2], name, rep),
        )

    if tag in ("neg", "hd", "tl"):
        return (tag, substitute(t[1], name, rep))

    if tag == "if":
        return (
            "if",
            substitute(t[1], name, rep),
            substitute(t[2], name, rep),
            substitute(t[3], name, rep),
        )

    if tag == "let":
        var_name = t[1]
        new_value = substitute(t[2], name, rep)
        if var_name == name:
            # Variable is shadowed
            return ("let", var_name, new_value, t[3])
        if var_name in free_vars(rep):
            # Need to rename to avoid capture
            used = free_vars(t[3]) | free_vars(rep) | {var_name, name}
            fresh = ng.fresh(used)
            renamed_body = substitute(t[3], var_name, ("var", fresh))
            new_body = substitute(renamed_body, name, rep)
            return ("let", fresh, new_value, new_body)
        return ("let", var_name, new_value, substitute(t[3], name, rep))

    if tag == "letrec":
        var_name = t[1]
        if var_name == name:
            # Variable is shadowed
            return t
        if var_name in free_vars(rep):
            # Need to rename to avoid capture
            used = free_vars(t[2]) | free_vars(t[3]) | free_vars(rep) | {var_name, name}
            fresh = ng.fresh(used)
            renamed_value = substitute(t[2], var_name, ("var", fresh))
            renamed_body = substitute(t[3], var_name, ("var", fresh))
            new_value = substitute(renamed_value, name, rep)
            new_body = substitute(renamed_body, name, rep)
            return ("letrec", fresh, new_value, new_body)
        return (
            "letrec",
            var_name,
            substitute(t[2], name, rep),
            substitute(t[3], name, rep),
        )

    if tag == "fix":
        return ("fix", substitute(t[1], name, rep))

    if tag == "prog":
        return (
            "prog",
            substitute(t[1], name, rep),
            substitute(t[2], name, rep),
        )

    # numbers, nil, and others
    return t


# --------------------------------------------------------------------
# Evaluation (normal order, lazy under lambdas)
# --------------------------------------------------------------------

MAX_STEPS = 500000


def values_equal(v1, v2):
    """Check if two values are structurally equal"""
    # Both are numbers
    if v1[0] == "num" and v2[0] == "num":
        return v1[1] == v2[1]
    
    # Both are nil
    if v1[0] == "nil" and v2[0] == "nil":
        return True
    
    # Both are cons
    if v1[0] == "cons" and v2[0] == "cons":
        # Recursively check head and tail
        heads_equal = values_equal(v1[1], v2[1])
        tails_equal = values_equal(v1[2], v2[2])
        return heads_equal and tails_equal
    
    # Different types or other cases
    return False


def step(t):
    tag = t[0]

    # Values that do not reduce
    if tag in ("var", "num", "nil"):
        return t, False

    # Lazy semantics: do not reduce under lambda
    if tag == "lam":
        return t, False

    # Cons is a value (data constructor)
    # We evaluate the head and tail fully
    if tag == "cons":
        head, tail = t[1], t[2]
        
        # Reduce head
        new_head, changed = step(head)
        if changed:
            return ("cons", new_head, tail), True
        
        # Reduce tail
        new_tail, changed = step(tail)
        if changed:
            return ("cons", head, new_tail), True
        
        # Both fully reduced, cons is now a value
        return t, False

    # Application
    if tag == "app":
        f, a = t[1], t[2]

        # Beta-reduction when function is a lambda
        if f[0] == "lam":
            v, body = f[1], f[2]
            return substitute(body, v, a), True

        # Otherwise reduce the function first
        new_f, changed = step(f)
        if changed:
            return ("app", new_f, a), True

        # Then reduce the argument
        new_a, changed = step(a)
        return ("app", f, new_a), changed

    # Binary arithmetic
    if tag in ("plus", "minus", "times"):
        op = tag
        left, right = t[1], t[2]

        # Reduce left
        new_left, changed = step(left)
        if changed:
            return (op, new_left, right), True

        # Reduce right
        new_right, changed = step(right)
        if changed:
            return (op, left, new_right), True

        # Both numeric: perform operation
        if left[0] == "num" and right[0] == "num":
            lv, rv = left[1], right[1]
            if op == "plus":
                val = lv + rv
            elif op == "minus":
                val = lv - rv
            else:  # times
                val = lv * rv
            return ("num", float(val)), True

        return t, False

    # Unary minus
    if tag == "neg":
        inner = t[1]
        new_inner, changed = step(inner)
        if changed:
            return ("neg", new_inner), True
        if inner[0] == "num":
            return ("num", float(-inner[1])), True
        return t, False

    # If-then-else
    if tag == "if":
        cond, then_branch, else_branch = t[1], t[2], t[3]
        
        # Reduce condition first
        new_cond, changed = step(cond)
        if changed:
            return ("if", new_cond, then_branch, else_branch), True
        
        # If condition is a number, branch
        if cond[0] == "num":
            if cond[1] == 1.0:
                return then_branch, True
            elif cond[1] == 0.0:
                return else_branch, True
        
        return t, False

    # Comparison operators
    if tag in ("eq", "leq"):
        left, right = t[1], t[2]
        
        # Reduce left
        new_left, changed = step(left)
        if changed:
            return (tag, new_left, right), True
        
        # Reduce right
        new_right, changed = step(right)
        if changed:
            return (tag, left, new_right), True
        
        # Both reduced - now compare
        if tag == "eq":
            # Use structural equality for all values
            result = 1.0 if values_equal(left, right) else 0.0
            return ("num", result), True
        
        # leq only works on numbers
        if tag == "leq":
            if left[0] == "num" and right[0] == "num":
                result = 1.0 if left[1] <= right[1] else 0.0
                return ("num", result), True
        
        return t, False

    # Let: desugar to application
    # let x = e1 in e2  -->  (\x.e2) e1
    if tag == "let":
        var_name, value, body = t[1], t[2], t[3]
        return ("app", ("lam", var_name, body), value), True

    # Letrec: desugar using fix
    # letrec f = e1 in e2  -->  let f = (fix (\f.e1)) in e2
    if tag == "letrec":
        var_name, value, body = t[1], t[2], t[3]
        fixed_value = ("fix", ("lam", var_name, value))
        return ("let", var_name, fixed_value, body), True

    # Fix: fixed-point combinator
    # fix F  -->  F (fix F)
    if tag == "fix":
        func = t[1]
        
        # Reduce the function first
        new_func, changed = step(func)
        if changed:
            return ("fix", new_func), True
        
        # Only expand fix when the function is a lambda
        # This prevents infinite expansion
        if func[0] == "lam":
            # Apply the reduction: fix F --> F (fix F)
            return ("app", func, ("fix", func)), True
        
        return t, False

    # Prog: evaluate both sides
    if tag == "prog":
        left, right = t[1], t[2]
        
        # Reduce left
        new_left, changed = step(left)
        if changed:
            return ("prog", new_left, right), True
        
        # Reduce right
        new_right, changed = step(right)
        if changed:
            return ("prog", left, new_right), True
        
        # Both reduced
        return t, False

    # Head: hd (a:b) --> a
    if tag == "hd":
        inner = t[1]
        
        # Reduce the argument
        new_inner, changed = step(inner)
        if changed:
            return ("hd", new_inner), True
        
        # If it's a cons, extract head
        if inner[0] == "cons":
            return inner[1], True
        
        return t, False

    # Tail: tl (a:b) --> b
    if tag == "tl":
        inner = t[1]
        
        # Reduce the argument
        new_inner, changed = step(inner)
        if changed:
            return ("tl", new_inner), True
        
        # If it's a cons, extract tail
        if inner[0] == "cons":
            return inner[2], True
        
        return t, False

    return t, False


def evaluate(t):
    changed = True
    steps = 0
    while changed and steps < MAX_STEPS:
        t, changed = step(t)
        steps += 1
    if changed:
        # still reducible but hit step limit
        raise RuntimeError("non-terminating")
    return t


# --------------------------------------------------------------------
# Top-level interface
# --------------------------------------------------------------------

def interpret(src: str) -> str:
    cst = parser.parse(src)
    ast = LambdaCalculusTransformer().transform(cst)
    try:
        out = evaluate(ast)
        return linearize(out, top=True)
    except RuntimeError:
        return "<non-terminating>"


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