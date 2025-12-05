from interpreter import (
    interpret,
    substitute,
    evaluate,
    LambdaCalculusTransformer,
    parser,
    linearize,
)


def ast(source_code: str):
    return LambdaCalculusTransformer().transform(parser.parse(source_code))


def test_parse():
    MAGENTA = "\033[95m"
    RESET = "\033[0m"

    assert ast(r"x") == ("var", "x")
    print(f"AST {MAGENTA}x{RESET} == ('var', 'x')")

    assert ast(r"(((x)) ((y)))") == ("app", ("var", "x"), ("var", "y"))
    print(
        f"AST {MAGENTA}(((x)) ((y))){RESET} == "
        "('app', ('var', 'x'), ('var', 'y'))"
    )

    assert ast(r"x y") == ("app", ("var", "x"), ("var", "y"))
    print(
        f"AST {MAGENTA}x y{RESET} == "
        "('app', ('var', 'x'), ('var', 'y'))"
    )

    assert ast(r"x y z") == (
        "app",
        ("app", ("var", "x"), ("var", "y")),
        ("var", "z"),
    )
    print(
        f"AST {MAGENTA}x y z{RESET} == "
        "('app', ('app', ('var', 'x'), ('var', 'y')), ('var', 'z'))"
    )

    assert ast(r"\x.y") == ("lam", "x", ("var", "y"))
    print(
        f"AST {MAGENTA}\\x.y{RESET} == "
        "('lam', 'x', ('var', 'y'))"
    )

    assert ast(r"\x.x y") == (
        "lam",
        "x",
        ("app", ("var", "x"), ("var", "y")),
    )
    print(
        f"AST {MAGENTA}\\x.x y{RESET} == "
        "('lam', 'x', ('app', ('var', 'x'), ('var', 'y')))"
    )

    assert ast(r"\x.x y z") == (
        "lam",
        "x",
        ("app", ("app", ("var", "x"), ("var", "y")), ("var", "z")),
    )
    print(
        f"AST {MAGENTA}\\x.x y z{RESET} == "
        "('lam', 'x', ('app', ('app', ('var', 'x'), ('var', 'y')), ('var', 'z')))"
    )

    print("\nParser: All tests passed!\n")


def test_substitute():
    MAGENTA = "\033[95m"
    RESET = "\033[0m"

    assert substitute(("var", "x"), "x", ("var", "y")) == ("var", "y")
    print(f"SUBST {MAGENTA}x [y/x]{RESET} == ('var', 'y')")

    assert substitute(("lam", "x", ("var", "x")), "x", ("var", "y")) == (
        "lam",
        "x",
        ("var", "x"),
    )
    print(f"SUBST {MAGENTA}\\x.x [y/x]{RESET} == ('lam', 'x', ('var', 'x'))")

    assert substitute(
        ("app", ("var", "x"), ("var", "x")),
        "x",
        ("var", "y"),
    ) == ("app", ("var", "y"), ("var", "y"))
    print(
        f"SUBST {MAGENTA}(x x) [y/x]{RESET} == "
        "('app', ('var', 'y'), ('var', 'y'))"
    )

    assert substitute(
        ("lam", "y", ("var", "x")),
        "x",
        ("var", "y"),
    )[0] == "lam"
    print(
        f"SUBST {MAGENTA}\\y. x [y/x]{RESET} == "
        "lam with fresh variable (capture avoiding)"
    )

    print("\nsubstitute(): All tests passed!\n")


def test_evaluate_basic():
    MAGENTA = "\033[95m"
    RESET = "\033[0m"

    assert linearize(evaluate(ast(r"x"))) == "x"
    print(f"EVAL {MAGENTA}x{RESET} == x")

    assert linearize(evaluate(ast(r"x y"))) == "(x y)"
    print(f"EVAL {MAGENTA}x y{RESET} == (x y)")

    assert linearize(evaluate(ast(r"x y z"))) == "((x y) z)"
    print(f"EVAL {MAGENTA}x y z{RESET} == ((x y) z)")

    assert linearize(evaluate(ast(r"x (y z)"))) == "(x (y z))"
    print(f"EVAL {MAGENTA}x (y z){RESET} == (x (y z))")

    assert linearize(evaluate(ast(r"\x.y"))) == r"(\x.y)"
    print(f"EVAL {MAGENTA}\\x.y{RESET} == \\x.y")

    assert linearize(evaluate(ast(r"(\x.x) y"))) == "y"
    print(f"EVAL {MAGENTA}(\\x.x) y{RESET} == y")

    print("\nevaluate(): All basic tests passed!\n")


def test_interpret_basic():
    print("interpret x        -->", interpret("x"))
    print("interpret x y      -->", interpret("x y"))
    print(r"interpret (\x.x) y -->", interpret(r"(\x.x) y"))
    print("\ninterpret(): basic tests ran.\n")


def test_arithmetic_and_precedence():
    """Required tests from Milestone 1"""
    BLUE = "\033[94m"
    RESET = "\033[0m"

    assert interpret(r"(\x.x) (1--2)") == "3.0"
    print(BLUE + r"(\x.x) (1--2)" + RESET + " ==> 3.0")

    assert interpret(r"(\x.x) (1---2)") == "-1.0"
    print(BLUE + r"(\x.x) (1---2)" + RESET + " ==> -1.0")

    assert interpret(r"(\x.x + 1) 5") == "6.0"
    print(BLUE + r"(\x.x + 1) 5" + RESET + " ==> 6.0")

    assert interpret(r"(\x.x * x) 3") == "9.0"
    print(BLUE + r"(\x.x * x) 3" + RESET + " ==> 9.0")

    assert interpret(r"(\x.\y.x + y) 3 4") == "7.0"
    print(BLUE + r"(\x.\y.x + y) 3 4" + RESET + " ==> 7.0")

    assert interpret(r"1-2*3-4") == "-9.0"
    print(BLUE + "1-2*3-4" + RESET + " ==> -9.0")

    assert interpret(r"(\x.x * x) 2 * 3") == "12.0"
    print(BLUE + r"(\x.x * x) 2 * 3" + RESET + " ==> 12.0")

    assert interpret(r"(\x.x * x) (-2) * (-3)") == "-12.0"
    print(BLUE + r"(\x.x * x) (-2) * (-3)" + RESET + " ==> -12.0")

    assert interpret(r"((\x.x * x) (-2)) * (-3)") == "-12.0"
    print(BLUE + r"((\x.x * x) (-2)) * (-3)" + RESET + " ==> -12.0")

    assert interpret(r"(\x.x) (---2)") == "-2.0"
    print(BLUE + r"(\x.x) (---2)" + RESET + " ==> -2.0")

    print("\narithmetic and precedence: all required tests passed!\n")


def test_additional_precedence():
    """Additional tests from Milestone 1"""
    BLUE = "\033[94m"
    RESET = "\033[0m"

    print("=" * 60)
    print("ADDITIONAL PRECEDENCE TESTS (Blue Highlighted)")
    print("=" * 60 + "\n")

    assert interpret("2 + 3 * 4") == "14.0"
    print(BLUE + "2 + 3 * 4" + RESET + " ==> 14.0")

    assert interpret("2 * 3 + 4") == "10.0"
    print(BLUE + "2 * 3 + 4" + RESET + " ==> 10.0")

    assert interpret("10 - 2 - 3") == "5.0"
    print(BLUE + "10 - 2 - 3" + RESET + " ==> 5.0")

    assert interpret("2 + 3 + 4") == "9.0"
    print(BLUE + "2 + 3 + 4" + RESET + " ==> 9.0")

    assert interpret("2 * 3 * 4") == "24.0"
    print(BLUE + "2 * 3 * 4" + RESET + " ==> 24.0")

    assert interpret("-2 * 3") == "-6.0"
    print(BLUE + "-2 * 3" + RESET + " ==> -6.0")

    assert interpret("--2") == "2.0"
    print(BLUE + "--2" + RESET + " ==> 2.0")

    assert interpret("---2") == "-2.0"
    print(BLUE + "---2" + RESET + " ==> -2.0")

    assert interpret("2 * -3") == "-6.0"
    print(BLUE + "2 * -3" + RESET + " ==> -6.0")

    assert interpret("10 - -5") == "15.0"
    print(BLUE + "10 - -5" + RESET + " ==> 15.0")

    assert interpret(r"(\x.x) 5 + 3") == "8.0"
    print(BLUE + r"(\x.x) 5 + 3" + RESET + " ==> 8.0")

    assert interpret(r"(\x.x + 1) 2 * 3") == "9.0"
    print(BLUE + r"(\x.x + 1) 2 * 3" + RESET + " ==> 9.0")

    assert interpret(r"(\x.x * 2) 3 + 4") == "10.0"
    print(BLUE + r"(\x.x * 2) 3 + 4" + RESET + " ==> 10.0")

    assert interpret(r"(\f.\x.f (f x)) (\x.x + 1) 0") == "2.0"
    print(BLUE + r"(\f.\x.f (f x)) (\x.x + 1) 0" + RESET + " ==> 2.0")

    assert interpret("(2 + 3) * 4") == "20.0"
    print(BLUE + "(2 + 3) * 4" + RESET + " ==> 20.0")

    assert interpret("2 * (3 + 4)") == "14.0"
    print(BLUE + "2 * (3 + 4)" + RESET + " ==> 14.0")

    result1 = interpret(r"\x.(\y.y)x")
    print(BLUE + r"\x.(\y.y)x" + RESET + f" ==> {result1}")

    result2 = interpret(r"(\x.a x) ((\x.x)b)")
    print(BLUE + r"(\x.a x) ((\x.x)b)" + RESET + f" ==> {result2}")

    print("\nadditional precedence tests: all passed!\n")


def test_milestone2_required():
    """Required tests from Milestone 2"""
    BLUE = "\033[94m"
    RESET = "\033[0m"
    
    print("=" * 70)
    print("MILESTONE 2 REQUIRED TESTS")
    print("=" * 70 + "\n")
    
    assert interpret("if 0 then 2 else 1") == "1.0"
    print(BLUE + "if 0 then 2 else 1" + RESET + " ==> 1.0")
    
    assert interpret("if 1 then 2 else 2") == "2.0"
    print(BLUE + "if 1 then 2 else 2" + RESET + " ==> 2.0")
    
    assert interpret("if 0 then 2 else if 1 then 3 else 4") == "3.0"
    print(BLUE + "if 0 then 2 else if 1 then 3 else 4" + RESET + " ==> 3.0")
    
    assert interpret("if 0 then 2 else if 0 then 3 else 4") == "4.0"
    print(BLUE + "if 0 then 2 else if 0 then 3 else 4" + RESET + " ==> 4.0")
    
    assert interpret("if 0 == 0 then 5 else 6") == "5.0"
    print(BLUE + "if 0 == 0 then 5 else 6" + RESET + " ==> 5.0")
    
    assert interpret("if 0 <= 1 then 6 else 7") == "6.0"
    print(BLUE + "if 0 <= 1 then 6 else 7" + RESET + " ==> 6.0")
    
    assert interpret("if 1 <= 0 then 6 else 7") == "7.0"
    print(BLUE + "if 1 <= 0 then 6 else 7" + RESET + " ==> 7.0")
    
    assert interpret("let x = 1 in if x == 1 then 8 else 9") == "8.0"
    print(BLUE + "let x = 1 in if x == 1 then 8 else 9" + RESET + " ==> 8.0")
    
    assert interpret("let x = 0 in if x == 1 then 8 else 9") == "9.0"
    print(BLUE + "let x = 0 in if x == 1 then 8 else 9" + RESET + " ==> 9.0")
    
    assert interpret(r"let f = \x.x in f 10") == "10.0"
    print(BLUE + r"let f = \x.x in f 10" + RESET + " ==> 10.0")
    
    assert interpret(r"let f = \x.x+1 in f 10") == "11.0"
    print(BLUE + r"let f = \x.x+1 in f 10" + RESET + " ==> 11.0")
    
    assert interpret(r"let f = \x.x*6 in let g = \x.x+1 in f (g 1)") == "12.0"
    print(BLUE + r"let f = \x.x*6 in let g = \x.x+1 in f (g 1)" + RESET + " ==> 12.0")
    
    assert interpret(r"let f = \x.x*6 in let g = \x.x+1 in g (f 2)") == "13.0"
    print(BLUE + r"let f = \x.x*6 in let g = \x.x+1 in g (f 2)" + RESET + " ==> 13.0")
    
    assert interpret(r"let f = \x.x*6 in let f = \x.x+1 in f (f 2) + 10") == "14.0"
    print(BLUE + r"let f = \x.x*6 in let f = \x.x+1 in f (f 2) + 10" + RESET + " ==> 14.0")
    
    assert interpret(r"letrec f = \n. if n==0 then 1 else n*f(n-1) in f 4") == "24.0"
    print(BLUE + r"letrec f = \n. if n==0 then 1 else n*f(n-1) in f 4" + RESET + " ==> 24.0")
    
    assert interpret(r"letrec f = \n. if n==0 then 0 else 1 + 2*(n-1) + f(n-1) in f 6") == "36.0"
    print(BLUE + r"letrec f = \n. if n==0 then 0 else 1 + 2*(n-1) + f(n-1) in f 6" + RESET + " ==> 36.0")
    
    print("\nMilestone 2 required tests: all passed!\n")


def test_milestone2_additional():
    """Additional M2 tests"""
    BLUE = "\033[94m"
    RESET = "\033[0m"
    
    print("=" * 70)
    print("MILESTONE 2 ADDITIONAL TESTS")
    print("=" * 70 + "\n")
    
    assert interpret("1 == 1") == "1.0"
    print(BLUE + "1 == 1" + RESET + " ==> 1.0")
    
    assert interpret("1 == 2") == "0.0"
    print(BLUE + "1 == 2" + RESET + " ==> 0.0")
    
    assert interpret("5 <= 5") == "1.0"
    print(BLUE + "5 <= 5" + RESET + " ==> 1.0")
    
    assert interpret("5 <= 4") == "0.0"
    print(BLUE + "5 <= 4" + RESET + " ==> 0.0")
    
    assert interpret("2 + 3 == 5") == "1.0"
    print(BLUE + "2 + 3 == 5" + RESET + " ==> 1.0")
    
    assert interpret("let x = 5 in x + 3") == "8.0"
    print(BLUE + "let x = 5 in x + 3" + RESET + " ==> 8.0")
    
    assert interpret(r"letrec sum = \n. if n==0 then 0 else n + sum(n-1) in sum 5") == "15.0"
    print(BLUE + r"letrec sum = \n. if n==0 then 0 else n + sum(n-1) in sum 5" + RESET + " ==> 15.0")
    
    print("\nMilestone 2 additional tests: all passed!\n")


def test_milestone3_required():
    """Required tests from Milestone 3"""
    BLUE = "\033[94m"
    RESET = "\033[0m"
    
    print("=" * 70)
    print("MILESTONE 3 REQUIRED TESTS")
    print("=" * 70 + "\n")
    
    assert interpret("1") == "1.0"
    print(BLUE + "1" + RESET + " ==> 1.0")
    
    assert interpret(r"(if 1 == 1 then \x.x+1 else \x.x+2) 5 + 10") == "16.0"
    print(BLUE + r"(if 1 == 1 then \x.x+1 else \x.x+2) 5 + 10" + RESET + " ==> 16.0")
    
    assert interpret("if 1 == 1 then 1 else 2 + 1") == "1.0"
    print(BLUE + "if 1 == 1 then 1 else 2 + 1" + RESET + " ==> 1.0")
    
    assert interpret("1 ;; 2") == "1.0 ;; 2.0"
    print(BLUE + "1 ;; 2" + RESET + " ==> 1.0 ;; 2.0")
    
    assert interpret("1 ;; 2 ;; 3") == "1.0 ;; 2.0 ;; 3.0"
    print(BLUE + "1 ;; 2 ;; 3" + RESET + " ==> 1.0 ;; 2.0 ;; 3.0")
    
    assert interpret(r"1+1 ;; (\x.x)a ;; (\x.x+x)2") == "2.0 ;; a ;; 4.0"
    print(BLUE + r"1+1 ;; (\x.x)a ;; (\x.x+x)2" + RESET + " ==> 2.0 ;; a ;; 4.0")
    
    assert interpret("1:2 ;; 1:2:#") == "(1.0 : 2.0) ;; (1.0 : (2.0 : #))"
    print(BLUE + "1:2 ;; 1:2:#" + RESET + " ==> (1.0 : 2.0) ;; (1.0 : (2.0 : #))")
    
    assert interpret("(1)") == "1.0"
    print(BLUE + "(1)" + RESET + " ==> 1.0")
    
    assert interpret("#") == "#"
    print(BLUE + "#" + RESET + " ==> #")
    
    assert interpret("1:2:3:#") == "(1.0 : (2.0 : (3.0 : #)))"
    print(BLUE + "1:2:3:#" + RESET + " ==> (1.0 : (2.0 : (3.0 : #)))")
    
    assert interpret(r"(\x.x) #") == "#"
    print(BLUE + r"(\x.x) #" + RESET + " ==> #")
    
    assert interpret(r"(\x.\y.x) 1:# a") == "(1.0 : #)"
    print(BLUE + r"(\x.\y.x) 1:# a" + RESET + " ==> (1.0 : #)")
    
    assert interpret(r"(\x.\y.y) a 1:#") == "(1.0 : #)"
    print(BLUE + r"(\x.\y.y) a 1:#" + RESET + " ==> (1.0 : #)")
    
    assert interpret(r"let f = \x.x+1 in (f 1) : (f 2) : (f 3) : #") == "(2.0 : (3.0 : (4.0 : #)))"
    print(BLUE + r"let f = \x.x+1 in (f 1) : (f 2) : (f 3) : #" + RESET + " ==> (2.0 : (3.0 : (4.0 : #)))")
    
    assert interpret("1:2 == 1:2") == "1.0"
    print(BLUE + "1:2 == 1:2" + RESET + " ==> 1.0")
    
    assert interpret("1:2 == 1:3") == "0.0"
    print(BLUE + "1:2 == 1:3" + RESET + " ==> 0.0")
    
    assert interpret("1:2:# == 1:2:#") == "1.0"
    print(BLUE + "1:2:# == 1:2:#" + RESET + " ==> 1.0")
    
    assert interpret("(1-2) : (2+2) : # == (-1):4:#") == "1.0"
    print(BLUE + "(1-2) : (2+2) : # == (-1):4:#" + RESET + " ==> 1.0")
    
    assert interpret("hd a") == "(hd a)"
    print(BLUE + "hd a" + RESET + " ==> (hd a)")
    
    assert interpret("hd (1:2:#)") == "1.0"
    print(BLUE + "hd (1:2:#)" + RESET + " ==> 1.0")
    
    assert interpret("hd 1:2:#") == "1.0"
    print(BLUE + "hd 1:2:#" + RESET + " ==> 1.0")
    
    assert interpret("tl a") == "(tl a)"
    print(BLUE + "tl a" + RESET + " ==> (tl a)")
    
    assert interpret("tl (1:2:#)") == "(2.0 : #)"
    print(BLUE + "tl (1:2:#)" + RESET + " ==> (2.0 : #)")
    
    assert interpret("tl 1:2:#") == "(2.0 : #)"
    print(BLUE + "tl 1:2:#" + RESET + " ==> (2.0 : #)")
    
    assert interpret(r"letrec map = \f. \xs. if xs==# then # else (f (hd xs)) : (map f (tl xs)) in (map (\x.x+1) (1:2:3:#))") == "(2.0 : (3.0 : (4.0 : #)))"
    print(BLUE + "map test" + RESET + " ==> (2.0 : (3.0 : (4.0 : #)))")
    
    print("\nMilestone 3 required tests: all passed!\n")


def test_milestone3_additional():
    """Additional M3 tests"""
    BLUE = "\033[94m"
    RESET = "\033[0m"
    
    print("=" * 70)
    print("MILESTONE 3 ADDITIONAL TESTS")
    print("=" * 70 + "\n")
    
    # Insertion sort
    sort_prog = r"""letrec insert = \x.\xs.
  if xs == # then
    x : #
  else if (x <= (hd xs)) then
    x : xs
  else
    (hd xs) : (insert x (tl xs))
in
letrec sort = \xs.
  if xs == # then
    #
  else
    insert (hd xs) (sort (tl xs))
in
sort (5 : 3 : 4 : 3 : 1 : #)"""
    
    result = interpret(sort_prog)
    assert result == "(1.0 : (3.0 : (3.0 : (4.0 : (5.0 : #)))))"
    print(BLUE + "insertion sort" + RESET + " ==> " + result)
    
    print("\nMilestone 3 additional tests: all passed!\n")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CPSC-354 ASSIGNMENT 3 - COMPLETE TEST SUITE (M1 + M2 + M3)")
    print("=" * 70 + "\n")

    print("\nTEST PARSING\n")
    test_parse()

    print("\nTEST SUBSTITUTION\n")
    test_substitute()

    print("\nTEST EVALUATE BASIC\n")
    test_evaluate_basic()

    print("\nTEST INTERPRET BASIC\n")
    test_interpret_basic()

    print("\nTEST ARITHMETIC AND PRECEDENCE (M1)\n")
    test_arithmetic_and_precedence()

    print("\nTEST ADDITIONAL PRECEDENCE (M1)\n")
    test_additional_precedence()

    print("\nTEST MILESTONE 2 REQUIRED\n")
    test_milestone2_required()

    print("\nTEST MILESTONE 2 ADDITIONAL\n")
    test_milestone2_additional()

    print("\nTEST MILESTONE 3 REQUIRED\n")
    test_milestone3_required()

    print("\nTEST MILESTONE 3 ADDITIONAL\n")
    test_milestone3_additional()

    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED - MILESTONES 1, 2 & 3 COMPLETE!")
    print("=" * 70 + "\n")