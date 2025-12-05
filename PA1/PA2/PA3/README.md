# CPSC-354 Assignment 3: Functional Programming Language Interpreter

**Student:** Ethan  
**Course:** CPSC-354 Programming Languages, Spring 2025

## Overview

This project implements a complete functional programming language interpreter with lambda calculus, arithmetic operations, conditionals, recursive functions, and list processing. The language supports lazy evaluation (call-by-name) and includes powerful features like `letrec` for recursion and list operations for functional data structures.

## Features Implemented

### Milestone 1: Lambda Calculus + Arithmetic
- ✅ Lambda abstraction (`\x.expr`)
- ✅ Function application (left-associative)
- ✅ Arithmetic operators: `+`, `-`, `*`, unary `-`
- ✅ Proper operator precedence
- ✅ Lazy evaluation (no reduction under lambda)
- ✅ Call-by-name semantics

### Milestone 2: Conditionals + Let + Recursion
- ✅ If-then-else conditionals
- ✅ Comparison operators: `==`, `<=`
- ✅ Let bindings with proper variable shadowing
- ✅ Recursive functions via `letrec`
- ✅ Fixed-point combinator (`fix`)

### Milestone 3: Lists + Sequencing
- ✅ Empty list (`#`)
- ✅ Cons operator (`:`) for list construction
- ✅ List destructors: `hd` (head), `tl` (tail)
- ✅ Structural equality for lists
- ✅ Sequential composition (`;;`)
- ✅ Complex recursive list functions (map, insertion sort)

## Files

- **`grammar.lark`** - Complete Lark grammar defining syntax and operator precedence
- **`interpreter.py`** - Main interpreter implementation with parser, evaluator, and pretty-printer
- **`interpreter_test.py`** - Comprehensive test suite covering all milestones

## Usage

### Running the Interpreter

**From command line:**
```bash
python3 interpreter.py "(\x.x + 1) 5"
# Output: 6.0
```

**From a file:**
```bash
python3 interpreter.py test.lc
```

**Interactive testing:**
```bash
python3 interpreter_test.py
```

## Example Programs

### Factorial
```
letrec f = \x. if x==0 then 1 else x * f(x-1) in f 5
// Output: 120.0
```

### Fibonacci
```
letrec fib = \n. 
    if n==0 then 0 else 
        if n==1 then 1 else
            fib(n-2)+fib(n-1)
in fib 10
// Output: 55.0
```

### Insertion Sort
```
letrec insert = \x.\xs.
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
sort (5 : 3 : 4 : 3 : 1 : #)
// Output: (1.0 : (3.0 : (3.0 : (4.0 : (5.0 : #)))))
```

## Operator Precedence

From loosest to tightest binding:

1. Sequencing (`;;`)
2. Lambda (`\x.expr`), Let (`let`), Letrec (`letrec`), If-then-else
3. Comparison (`==`, `<=`)
4. Addition/Subtraction (`+`, `-`)
5. Multiplication (`*`)
6. Unary minus (`-`)
7. Fix (`fix`)
8. Function application
9. List operations (`hd`, `tl`)
10. Cons (`:`)
11. Atoms (variables, numbers, `#`, parentheses)

## Implementation Details

### Evaluation Strategy
- **Lazy evaluation**: Expressions under lambda are not evaluated
- **Call-by-name**: Arguments are substituted unevaluated into function bodies
- **Normal order reduction**: Leftmost-outermost redex is reduced first

### Key Design Decisions
1. **Precedence handling**: Application binds tighter than cons (`:`) to allow `f 1:2` to parse as `f (1:2)`
2. **List equality**: Structural comparison recursively checks head and tail
3. **Cons evaluation**: Both head and tail are fully evaluated before cons becomes a value
4. **Step limit**: Set to 500,000 to handle complex recursive functions like insertion sort

### Capture-Avoiding Substitution
The interpreter implements proper α-conversion to avoid variable capture:
```
(\x.\y.x) → (\x.\Var1.x)  // when substituting y
```

## Test Results

All tests passing:
- ✅ Milestone 1: 10/10 required + additional tests
- ✅ Milestone 2: 16/16 required + additional tests  
- ✅ Milestone 3: 28/28 required + insertion sort

Total: **54+ tests passing**

## Technical Specifications

- **Language**: Python 3
- **Parser**: Lark (LALR parser)
- **Evaluation**: Small-step operational semantics
- **Step limit**: 500,000 (configurable in `interpreter.py`)

## Known Limitations

1. **No type checking**: The interpreter will attempt to evaluate ill-typed expressions
2. **Performance**: Complex recursive functions may be slow due to lazy evaluation overhead
3. **Error messages**: Limited error reporting for syntax or runtime errors

## References

- Course lectures on Lambda Calculus and Fixed-Point Combinator
- Assignment specifications for Milestones 1, 2, and 3
- Lark parser documentation

## Acknowledgments
---

*This project demonstrates a complete implementation of a functional programming language interpreter with lazy evaluation, recursive functions, and list processing capabilities.*
