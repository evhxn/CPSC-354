# A Comparison of Programming Languages

(work-in-progress)

<!--(latest version may be [here](https://hackmd.io/@alexhkurz/rkurYAVMye))-->

In order to better understand the design decisions behind our language LambdaF, we make a comparison of insertion sort in different programming languages.

The main points we want to make are the following.

- LambdaF is mainstream. Similar code can be written in most modern programming languages.
- LambdaF only *looks* weird because we were looking for the smallest fragment that allows us to implement interesting algorithms in a natural style. 
- Of course, our two design criteria, **simplicity** and **naturality**, pull in opposite directions, so the particular compromise we ended up with can be critiqued. 
- All proposals for improvement are welcome, but take the following into account.
    - Simplicity does not so much refer to "simple to look at" but rather to "simple to implement". (A semester is short.)
    - [Simple does not mean easy](https://www.youtube.com/watch?v=SxdOUGdseq4). Simple is the opposite of complex. Easy means familiar. 

## LambdaF

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
 sort (4 : 3 : 2 : 1 : #)
```

## OCaml

OCaml is a multi-paradigm language that influenced the design of LambdaF.

You can run the OCaml code below in the browser at [https://try.ocamlpro.com/](https://try.ocamlpro.com/).

### Idiomatically

This is how one might write insertion sort in OCaml:

```ocaml
let rec insert x xs =
 match xs with
 | [] -> [x]
 | hd::tl -> 
     if x <= hd then 
       x :: xs
     else 
       hd :: (insert x tl)

let rec sort xs =
  match xs with
  | [] -> []
  | hd::tl -> insert hd (sort tl)

let exp = sort [4; 3; 2; 1]
```

### In LambdaF Style

To simplify LambdaF 
- we didn't add pattern matching,
- we didn't add syntactic sugar for lists. 

Removing pattern matching and syntactic sugar for lists from the program above, insertion sort in OCaml becomes nearly identical to insertion sort in LambdaF:

```ocaml
let rec insert = fun x -> fun xs ->
  if xs = [] then
    x :: []
  else if (x <= (List.hd xs)) then
    x :: xs
  else
    (List.hd xs) :: (insert x (List.tl xs))

let rec sort = fun xs ->
  if xs = [] then
    []
  else
    insert (List.hd xs) (sort (List.tl xs)) 

let exp = sort (4 :: 3 :: 2 :: 1 :: [])
```

The differences are minor now. We have `#` where OCaml has `[]`, we have `:` where OCaml has `::`, we have `letrec` where OCaml has `let rec`, we have `hd` where OCaml has `List.hd`. (Ask if you want to know why we made those decisions.)

## Python

[Run online](https://www.programiz.com/online-compiler/2c2hVWK8igq1X)

```python
insert = lambda x, xs: [x] if xs == [] else ([x] + xs if x <= xs[0] else [xs[0]] + insert(x, xs[1:])) 

sort = lambda xs: [] if xs == [] else insert(xs[0], sort(xs[1:]))

exp = sort([4, 3, 2, 1])
print(exp) 
```

## JavaScript

[Run online](https://www.programiz.com/online-compiler/9WvDZzz013A4g)

```javascript
const insert = x => xs => {
  if (xs.length === 0) {
    return [x]
  } else if (x <= xs[0]) {
    return [x, ...xs]
  } else {
    return [xs[0], ...insert(x)(xs.slice(1))]
  }
}

const sort = xs => {
  if (xs.length === 0) {
    return []
  } else {
    return insert(xs[0])(sort(xs.slice(1)))
  }
}

// Test the function
const exp = sort([4, 3, 2, 1])
console.log(exp)
```

## Rust

[Run in Playground](https://play.rust-lang.org/?version=stable&mode=debug&edition=2021&gist=12cfd53017ed866ae4ca2c3eedc1fc02)

```rust
fn insert<T: Ord + Clone>(x: T, xs: Vec<T>) -> Vec<T> {
    if xs.is_empty() {
        vec![x]
    } else if x <= xs[0] {
        [vec![x], xs].concat()
    } else {
        [vec![xs[0].clone()], insert(x, xs[1..].to_vec())].concat()
    }
}

fn sort<T: Ord + Clone>(xs: Vec<T>) -> Vec<T> {
    if xs.is_empty() {
        vec![]
    } else {
        insert(xs[0].clone(), sort(xs[1..].to_vec()))
    }
}

fn main() {
    let result = sort(vec![4, 3, 2, 1]);
    println!("{:?}", result);
}
```

## Scala

[Run online](https://onecompiler.com/scala/42yj42y8c)

```scala
def insert(x: Int, xs: List[Int]): List[Int] = xs match {
  case Nil => List(x) // Base case: empty list
  case hd :: tl =>
    if (x <= hd) x :: xs // Insert x before the head
    else hd :: insert(x, tl) // Recursively process the tail
}

def sort(xs: List[Int]): List[Int] = xs match {
  case Nil => Nil // Base case: empty list
  case hd :: tl => insert(hd, sort(tl)) // Sort the tail and insert the head
}

// Test the function
val exp = sort(List(4, 3, 2, 1))
println(exp) // Output: List(1, 2, 3, 4)
```

## Lean
[Run online](https://live.lean-lang.org/#codez=CYUwZgBAlgdgziATgFwgLggOQIasEmEEAMlHKjvkSWbgFAA+EAHgDQQDaAuhALwB87jDvSasAnugyi4PXjQjRIjCIBMiCOOQALEDDnymEtQam6QAGwS754tBlgIU+4zVCQ7SZFAD2MAMqeHGMSkWLgQBEHUyMKcMuxCDEo2TNJ80PDu+gAUbihevv6ojHAAlDQ0AMQgAG7Ypmn2Ht5+DmwALMwAzMwATMwAjBxAA)
```lean
def insert : Nat → List Nat → List Nat
| x, [] => [x]
| x, y :: ys =>
  if x ≤ y then
    x :: y :: ys
  else
    y :: insert x ys

def insertionSort : List Nat → List Nat
| [] => []
| x :: xs => insert x (insertionSort xs)

#eval insertionSort [4,3,2,1]
```

## Racket
[Run online](https://onecompiler.com/racket/42yj368ve)

```racket
#lang racket

(define (insert x xs)
  (match xs
    ['() (list x)]                              ; Base case: empty list
    [(cons hd tl)                               ; Split into head and tail
     (if (<= x hd)
         (cons x xs)                            ; Insert x before the head
         (cons hd (insert x tl)))]))            ; Recursively process the tail
         
(define (sort xs)
  (match xs
    ['() '()]                                   ; Base case: empty list
    [(cons hd tl)                               ; Split into head and tail
     (insert hd (sort tl))]))                   ; Sort the tail and insert the head

;; Test the function
(define exp (sort '(4 3 2 1)))
(displayln exp)                                 ; Output: '(1 2 3 4)
```