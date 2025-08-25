# Report

The report will be written in $\LaTeX$ (https://www.latex-project.org/). A template for your $\LaTeX$ source file [`report.tex`](report/report.tex) and the compiled [pdf](report/report.pdf). For guidelines see [`report-guidelines.tex`](report/report-guidelines.tex) and the compiled [pdf](report/report-guidelines.pdf) and for Latex examples see [`latex-example.tex`](report/latex-example.tex) and [`latex-example.pdf`](report/latex-example.pdf).

## Teaching Rationale

"*Learning is the process of creating knowledge.*" (Kolb & Kolb)

"*Creativity is just connecting things. When you ask creative people how they did something, they feel a little guilty, because they didn’t really do it, they just saw something. It seemed obvious to them after a while. That’s because they were able to connect experiences they’ve had and synthesize new things.*" (Pentland)

The purpose of the report is to help students to grow from learners of a specified curriculum to independent explorers of a subject area. Accordingly, the report will not only contain solutions to homework (skill drill) but also document the student's own explorations around the theme of the course as well as an essay synthesizing what they learned during their explorations.

## Installing Latex

Our own $\LaTeX$ setup is as follows (all available for Linux, macOS, and Windows):
- [texlive](https://www.tug.org/texlive/) as the $\LaTeX$ distribution
- [VS Code](https://code.visualstudio.com/) as IDE
- [LaTeX-Workshop](https://github.com/James-Yu/LaTeX-Workshop/blob/master/README.md) as VS Code extension, see [Installation guide](https://github.com/James-Yu/LaTeX-Workshop/wiki/Install)
- macOS-specific guide for MacTeX and LaTeX workshop: https://sudorealm.com/blog/how-to-write-latex-documents-with-visual-studio-code-on-mac

For technical troubleshooting, please see the respective Discord channel and/or the office hours.

If you have problems integrating Latex and Github into VSCode, you can run Latex and push to Github via the commandline using `pdflatex report.tex` and `git push`, respectively.

To **test your setup** make sure of the following:

- You have a local folder, say cpsc354 (name doesn't matter for us).
- It has a subfolder `Report` (name matters).
- You copy [`report.tex`](report/report.tex) to your subfolder `Report`.
- You can compile `report.tex` locally and generate `report.pdf`, either via the green play button in VSCode or by typing `pdflatex report.tex` in a terminal.
- You can change `report.tex` (eg put your name), commit and push to Github. If pushing via the VSCode interface fails, try `git push` on the commandline.
- Check that `report.pdf` changed on Github.

## Organization

- You will keep both `report.tex` and `report.pdf` in a personal private GitHub repository. 
- Unless specified otherwise, in the beginning, your repo should only contain the following files
    ```
    .gitignore
    Report/report.pdf
    Report/report.tex
    README.md
    ```
    The README should contain name and email.
- For example, if a homework requires programming, make a subdirectory `src` where you store the relevant program files; if you want to include images in your report, make a subdirectory `img`; etc.
- Always use the same repository for all submissions of the course (get in touch if you think an exception is appropriate).
- Do not name different versions of your report, instead rely on the version control of git.
- Give the instructor access to your private GitHub repo by inviting your instructor (Alexander: [alexhkurz](https://github.com/alexhkurz), Jonathan: [jonweinb](https://github.com/jonweinb)).
- Submission info below.

## Point Distribution

Out of a total of 200 points the report is worth 90 points and divided approximately up as follows. 

- (2 points): Organization of the github repo (respecting naming conventions, etc).
- (4 points): Organization of the report, layout, typesetting.
- (4 points): Quality of writing, style, references.
- (13x2=26 points): 2 points per week for timely submission of homework.
- (13x3=39): 3 points per week for quality of homework in the full report.
- (12 points:) Essay.
- (3 points): Conclusion. 

## Writing of the Report

For organization of the github repo see [Git Best Practices](git-best-practices.md). In particular,
- respect the naming conventions given by the instructor,
- do not put machine-generated files in the repo,
- do not keep different versions of the report.

For organization of the report, layout and typesetting, take your favourite textbooks or scientific articles as examples. In CS, they are more often than not produced with $\LaTeX$. Learning $\LaTeX$ is one of the aims of the course. You will be graded also on your proficiency in $\LaTeX$. See also the comments below.

For quality of writing and style, in addition to common norms on writing in general, also make sure that the technical content is as easy to follow as possible. Learning to learn and document your learning is one of the aims of the course. It is thus expected from to you over the run of the semester explore the subject on your own. Add *interesting* references to the bilbliography and cite them throughout your report. As specified in the assignment, your submission URL should point to your PDF file, so make sure that your .gitignore file does **not** exclude PDF files.

The report should be on the content of the class as well as on your own investigations that you pursue on the topic of the class.  Do not put research on Latex into the report, Latex is just a tool for typesetting.

## Homework

**Deadlines:**
- Weekly deadlines. Most weeks have 2 points upon completion (approx 26 in total). 
    - To make your reports more self-contained, state the homework question before you give your answer. 
    - Deadlines are Sundays at midnight (so the instructor can look at your answers on Mondays).
    - The questions will be discussed Tuesdays in class and you will have an opportunity to improve your answers. 
- Final deadline. Further points are awarded after the final deadline at the end of final examination week:
    - You are expected to improve upon your weekly submissions for the final version of the report. 
    - The full report is due on the Sunday immediately after the Saturday of finals week. 

**Submission:**  After completing the homework, each weak, **submit the URL of your github repo** (containing `report.tex` and `report.pdf`) **via Canvas** before the deadline. Make sure that you **share access** to your private repo **with your instructor**.

**Do not keep different copies of your report in the repo.** During grading, git will be used to verify timestamps and revert to earlier versions.

**Please note:** The name of your repository does not matter, but you will have to adhere strictly to the given conventions of subdirectories and file names. You are using just **one report** for the whole semester in which all your homework goes. You are free to keep parts of the report template in the file, but please comment out the sections that you do not want to see in the actual compiled PDF throughout the semester. (Lines in $\LaTeX$ can be commented out by prepending "%".) 
 
## More on Layout and Typesetting

Good layout and typesetting [^goodLayout]
- makes it as easy as possible for the reader to navigate a document and extract the relevant information; 
- is uniform and even in the sense that it is free from distracing details and "same function" is represented by "same form" (This is known as ["form follows function"](https://en.wikipedia.org/wiki/Form_follows_function). Software engineering has a lot to learn from architecture, see for example [Christopher Alexander](https://en.wikipedia.org/wiki/Christopher_Alexander) who influenced the design of Wikipedia, design patterns in object oriented programming, agile software development, and the [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) architectural style underlying much of the WWW).
- takes a lot of time, polishing the content and presentation[^polishing].

Some concrete examples following from the general principles above:

- Adapt the template in a meaningful way. Don't leave empty sections or trailing "..." in the paper.
- The table of contents should have clickable links (use the $\LaTeX$ package [hyperref](https://ctan.org/pkg/hyperref)).
- Make sure that the way you use whitespace adheres to the principle of "form follows function". In particular, there should be no pages that are largely empty.
- If you use pictures of handwritten solutions, make sure  
    - that your handwritten solutions also show a nice layout and typesetting, and that they fit together in style across the whole report;
    - (if you use paper with lines) that your writing fits into the lines;
    - the pictures show no distracting details such as your fingers, or irrelevant background, or the shadow of your phone, etc;
    - that you do not put the first draft of your answer in the report, but rather carefully rewrite your draft answer to eliminate potential mistakes.[^firstDraft]

Finally, do not change the general layout specified in the template. Do not change the margins or the line spacing. In case of doubt get in touch. 

[^goodLayout]: The grading standards of this course do not aim to be overly strict when it comes to good typesetting, but experience from grading shows that good solutions often correlate with good layout . 

[^polishing]: Note that the human eye is very good at spotting small visual inconsistencies, for example, related to the use of space on a page. While these inconsistencies are not relevant to the content, they can be distracting, since they consume some attention of the reader. In other words, they are relevant to the relationship you as an author are trying to build with the reader.

[^firstDraft]: Mathematics is rather similar to programming in this respect. The first draft is (almost) never correct.

## Lessons from the Group Assignments and Project

Group work is an important part of the course. But we also want to hear from each student individually about what they learned from the group work.

Write 1.5 pages about your individual contributions to the programming group assignments and projects.

Be as technical and detailed as possible. Particularly valuable are *interesting*  examples where you connect concrete technical details with *interesting* general observations or where the theory discussed in the lectures helped with the design or implementation of the project.

Write this section during the semester. This is approximately a quarter of apage per week and the material should come from the work you do anyway. Just keep your eyes open for interesting lessons.

Make sure that you use LaTeX well to structure your writing (eg by using subsections).

## General Remark on Grading

Grading will not only be checking boxes. But as long as students want precise guidelines, grading will always involve some checking of boxes. So please make sure that you take on board the points listed above. Some will seem minor to you (like the ones on typesetting) but experience shows that work that has more carefully crafted form typically also has better content (for example, while improving the typesetting of your report, you will likely spot actual mistakes in the math).

## Teaching Rationale

Self-explaining can have a profound effect on problem-solving, in particular during early knowledge acquision. In particular, self-explanation helps the learner to build their own mental model and to revise it over time. 

Concretely, for your report, it is expected that you keep revising what you wrote during the semester to reflect the progress you make on updating your mental model.

For more on the value of self-explanations see Chapter 6 of Craig Barton, How I Wish I’d Taught Maths, and references therein.
