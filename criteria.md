# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Most of the questions in this corpus are practical and specific, but one or two
are harder because the answer is spread across a small number of campus policy
or advising documents. I set the target at 4 of 5 so the system has to retrieve
relevant evidence in the normal cases without requiring perfect performance on
the one topic that is naturally less common in the corpus.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
This corpus is built around short, direct advice posts and policy docs, so the
answer should be traceable to a specific file rather than a generic summary. I
picked 5 of 5 because the pipeline is designed to retrieve chunks and then
ground the response in those source documents, and if a response does not name
any file, it is not doing the core job the project is meant to do.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
The distance values in my cutoff test showed a clean split: the in-scope
questions stayed below 0.6, while the out-of-scope questions all sat above 0.78.
That gap made 4 of 5 a realistic and meaningful target because the gate is meant
to reject clearly unrelated questions without blocking actual campus-life answers.

---

## 4. Something about your chunks

At least 4 of 5 sampled chunks read as a complete thought, with no sentence
cut in half at either end.

**Why this target:**
My campus_life corpus is mostly short advice posts and policy notes, so a good
chunk has to preserve one idea without chopping a sentence in the middle. The
100/50 split keeps each chunk coherent while still allowing a little overlap
between adjacent thoughts, and the samples in my README show the same topic
staying together within a single source document.

---

## 5. Your choice

For at least 4 of my 5 answerable questions, the final answer includes a
concrete fact that matches the source document rather than a vague summary.

**Why this target:**
I care most about groundedness: the system can name a file and still be wrong
if it paraphrases the wrong idea. In this corpus, the strongest answers are the
ones that reflect a specific policy, deadline, or recommendation from the
actual document, so this checks that the answer is based on the source rather
than just sounding relevant.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
