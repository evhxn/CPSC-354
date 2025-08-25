# History of Programming Languages

## Early History of Programming Languages

(for those with an interest in history and/or philosophy)

The early history of programming languages was driven by mathematicians, logicians and philosophers. A great way to explore it is the Stanford Encyclopedia of Philosophy (SEP). I link articles that feature some of the early researchers in programming languages who will appear in our course such as Church, Turing, and Curry and logicians and mathematicians for whom we do not have time such as Dedekind, Peano, Russell, Hilbert, Brouwer, Goedel, Gentzen. The articles can get quite technical but just reading the introductions gives an idea of the broader questions and developments. A nice project could be to arrange the topics and protagonists of these articles into a timeline and then sketch a short history of the most important ideas and how they hang together.

- [The Modern History of Computing](https://plato.stanford.edu/entries/computing-history/)  
- [Dedekind](https://plato.stanford.edu/entries/dedekind-foundations/) and [The Early Development of Set Theory](https://plato.stanford.edu/entries/settheory-early/)
- [Russell's Paradox](https://plato.stanford.edu/entries/russell-paradox/) and [Self-Reference](https://plato.stanford.edu/entries/self-reference/)
- [Hilbert's Program](https://plato.stanford.edu/entries/hilbert-program/) and [The Development of Proof Theory](https://plato.stanford.edu/entries/proof-theory-development/)
- [Brouwer](https://plato.stanford.edu/entries/brouwer/) and [Constructive Mathematics](https://plato.stanford.edu/entries/mathematics-constructive/)
- [Alan Turing](https://plato.stanford.edu/entries/turing/) and [Turing Machines](https://plato.stanford.edu/entries/turing-machine/)
- [The Lambda Calculus](https://plato.stanford.edu/entries/lambda-calculus/) and [The Church-Turing Thesis](https://plato.stanford.edu/entries/church-turing/)
- [Recursive Functions](https://plato.stanford.edu/entries/recursive-functions/) and [Kurt Gödel](https://plato.stanford.edu/entries/goedel/) and [Incompleteness Theorems](https://plato.stanford.edu/entries/goedel-incompleteness/)
- [Combinatory Logic](https://plato.stanford.edu/entries/logic-combinatory/) and [Computability and Complexity](https://plato.stanford.edu/entries/computability/)
- [Church's Type Theory](https://plato.stanford.edu/entries/type-theory-church/) and [Type Theory](https://plato.stanford.edu/entries/type-theory/)
- [Paradoxes and Contemporary Logic](https://plato.stanford.edu/entries/paradoxes-contemporary-logic/)
- [Logic and Artificial Intelligence](https://plato.stanford.edu/entries/logic-ai/) and [Automated Reasoning](https://plato.stanford.edu/entries/reasoning-automated/)
- [Computational Linguistics](https://plato.stanford.edu/entries/computational-linguistics/)  and [Typelogical Grammar](https://plato.stanford.edu/entries/typelogical-grammar/)
- [Propositional Dynamic Logic](https://plato.stanford.edu/entries/logic-dynamic/) and [Temporal Logic](https://plato.stanford.edu/entries/logic-temporal/)
- [Proof Theory](https://plato.stanford.edu/entries/proof-theory/) and [Proof-Theoretic Semantics](https://plato.stanford.edu/entries/proof-theoretic-semantics/)
- [The Hole Argument](https://plato.stanford.edu/entries/spacetime-holearg/#PreInv) and [Symmetry and Symmetry Breaking](https://plato.stanford.edu/entries/symmetry-breaking/)

Get in touch if you want to hear more about how these articles are related to this course.

Our course will explore the ramifications of these early developments in the area of programming languages, in particular with respect to designing programming languages and building interpreters. Another important area of theoretical computer science branching off from the early fundamentamental [^typo] discoveries of Turing and others is computational complexity theory and I recommend [Chapter 2 of the book Mathematics and Computation](https://www.math.ias.edu/files/Book-online-Aug0619.pdf#page=1) for a first introduction. While the vast majority of this book is outside the scope of this course, this chapter illustrates well that programming languages and complexity theory flow from the same spring.

I recently became more interested in the **history of variable binding**. In programming, variable binding and capture avoiding substitution was introduced in Church's lambda calculus.  It forms the basis of concepts such as function, method, procedure, scope, local vs global variables, objects and classes, interfaces, etc. In logic, variable binding appears as quantification. A good starting point for the history of quantifiers is Putnam's [Peirce the Logician](https://core.ac.uk/download/pdf/82687196.pdf). We will touch on the importance of quantifiers for computing in a lecture on [capture avoiding substitution](https://hackmd.io/@alexhkurz/SkQzDC6n7#A-programming-example). 


[^typo]: I like this typo too much to correct it ... apologies.

## Modern History of Programming Languages

I would let the modern history of programming languages begin with Fortran and Lisp. Until approximately 1970 it was dominated by the problem of writing efficient parsers and compilers. By 1980, parsing and compiling was well understood and software engineering was born. We will have more time for this part of the history next semester in Compiler Construction. The discussion topics below mostly aim at current developments in programming languages.


## Some Pioneers of Programming Languages 

(this list is very incomplete ... send me your favourite links to add):

  - Documentary about [John von Neumann](https://www.youtube.com/watch?v=Y2jiQXI6nrE) containing footage of the computer JvN had built in the 1940ies. [Adventures of a Mathematician](https://archive.org/details/adventuresofmath0000ulam) is a wonderful book about JvN by Stan Ulam, himself a legendary mathematician.

  - Robin Milner. [Turing Award Lecture](https://dl.acm.org/doi/pdf/10.1145/151233.151240).
  - [Rich Hickey](https://en.wikipedia.org/wiki/Rich_Hickey), the creator of Clojure, says "State is Never Simple" in [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/) at 31m35s and following. The morale is: It is easier not to complect if coding in a functional language. Memorable quotes: "By stateful I mean that every time you ask the same question you get a different answer." "I don't know,I don't want to know." "Represent data by data." "Easy is not simple."

  - [Bjarne Stroustrup](https://en.wikipedia.org/wiki/Bjarne_Stroustrup), the creator of C++, talks about [The Essence of C++](https://www.youtube.com/watch?v=86xWVb4XIyE&feature=emb_rel_err). Historically interesting is also his talk about [The Design of C++](https://www.youtube.com/watch?v=69edOm889V4) from 1994.

  - [Simon Peyton Jones](https://en.wikipedia.org/wiki/Simon_Peyton_Jones), one of the inventors of Haskell, talks about [Functional Programming Languages and the Pursuit of Laziness](https://www.youtube.com/watch?v=SqWDAo1Jnyc). 

  - [Bob Martin](https://en.wikipedia.org/wiki/Robert_C._Martin), one of the inventors of agile computing talks about the [The Future of Programming](https://www.youtube.com/watch?v=ecIWPzGEbFc).

  - [Alan Kay](https://en.wikipedia.org/wiki/Alan_Kay), one of the inventors of personal computing and object-oriented programming, talks about how the invention of personal computing goes back to a project of reforming school education in [Inventing the Future](https://www.youtube.com/watch?v=M6ZHxUwqPVw). "The best way to predict the future is to invent it."
  - [Tony Hoare](https://en.wikipedia.org/wiki/Tony_Hoare): 
    - [1980 Turing Award Lecture](https://dl.acm.org/doi/pdf/10.1145/1283920.1283936) has a lot of interesting anecdotes about Quicksort, Algol, the switch statement, early compilers, operating systems, Hoare logic. Also some valuable general lessons about software engineering. I collected some of my [favourite quotes](hoare-1980-quotes.md).

    - Video: [Null References: The Billion Dollar Mistake](https://www.infoq.com/presentations/Null-References-The-Billion-Dollar-Mistake-Tony-Hoare/) 2009. picks up some of the same themes, but focuses on pointers and memory management, on compile-time vs run-time. "I don't care about the subscript error, I want it to run." (18:00).The discussion around (24:27) about disjoint unions is related to `Maybe` in Haskell and then to abstract syntax trees. Difficulty of proofs of program correctness as an objective measure of the quality of a program language (32:32). Programming language design is driven by the need to fight viruses (37:40). "The virus will find a case that is not likely to arise". "If it hadn't been for the get routine of C, we might have had no malware". (39:25).

  -  The [ACM Turing Award Winner Interview Playlist](https://www.youtube.com/playlist?list=PLn0nrSd4xjjaSLBSzmno-3Ods6FJE9nlO) has some great interviews ... I wish I had found the time to watch them all. 

