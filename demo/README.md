# KI-Workflower – Public Demo Case Study

## Evidence before release

A small software change can raise a surprising number of questions.

This case study starts with an existing measurement-data exporter. It reads CSV data and produces a text report. At first, the task sounds straightforward:

> **Add a JSON export without unintentionally changing existing data, precision, ordering, or current program behavior.**

This is exactly where KI-Workflower comes in: how can a change be implemented without unintentionally affecting existing behavior?

A new feature alone is not enough. In the end, it should be clear whether the agreed requirements were actually met, which risks were checked, and whether the existing behavior remained intact.

This case study therefore does not expose the internal mechanics of KI-Workflower. It shows what should be externally verifiable: decisions, effects, and evidence.

## 1. Try first, decide second

Before the actual change was implemented, one simple question came first:

How can measurement values and timestamps be carried into the new JSON export without changing their meaning?

A small Proof of Concept (PoC) was used as a focused technical experiment.

It showed:

- A straightforward `float`-based round trip did not preserve decimal values reliably enough.
- A decimal-preserving approach passed the comparison.
- The tested timestamp handling preserved the intended time information.

That had an immediate consequence: the `float` approach was rejected for measurement values before implementation began.

That is what a PoC is for. It should not merely confirm afterwards what has already been built. It should reveal early enough whether a technical idea actually holds up.

Here, the experiment changed the later solution.

## 2. What does “the change works” actually mean?

“Add a JSON export” describes a function. That is not yet enough for a reliable acceptance decision.

The functional expectations were therefore translated with QFD – Quality Function Deployment – into concrete, testable characteristics.

For this change, that included:

- The JSON structure must be valid.
- Every record must be transferred completely and exactly once.
- Decimal values must retain their value faithfully.
- Timestamps must retain their time meaning.
- The existing text report must continue to behave exactly as before.
- Invalid input must not be accepted silently.

A general change request was thus turned into specific questions that each required a verifiable answer.

## 3. Naming risks is not enough

The next question was what could go wrong.

The risk register considered, among other things:

- Records could be lost or duplicated.
- Numeric values could change unnoticed.
- Time information could change meaning.
- The existing text report could be affected by the extension.
- Invalid input could accidentally be treated as valid.

The important point is that the risks were not merely listed. Each relevant risk was linked to a concrete control.

That made it clearer before implementation what would later have to be checked.

## 4. One additional question that had been missing

The Mini-FMEA – a compact Failure Mode and Effects Analysis – went one step further.

It asked not only, “What can go wrong?” but also, “Which specific failure situation might we still be overlooking?”

One case stood out:

> An incomplete export could incorrectly be treated as successful.

That case was not yet covered sufficiently by the existing test plan.

The consequence was concrete:

- one additional risk,
- one additional test condition,
- one additional acceptance criterion.

The Mini-FMEA therefore did not remain paperwork. It changed the test plan.

## 5. What had to be demonstrated before completion

Seven acceptance criteria were in place at the end:

1. valid JSON structure,
2. complete transfer of every record exactly once,
3. preservation of decimal values,
4. preservation of time meaning,
5. preservation of existing text behavior,
6. invalid input is not accepted silently,
7. an incomplete export must not produce a false success state.

The seventh criterion did not exist at the beginning. It emerged from the preceding failure analysis.

That matters in this case study: the methods were not described afterwards around a desired result. They already had visible effects on what subsequently had to be tested.

## 6. Do not test only what is new

When existing software is changed, it is not enough to ask whether the new feature works.

An equally important question is:

**What was this change specifically not allowed to alter?**

Before implementation, the permitted change scope and the protected existing state were therefore defined.

The later non-loss check also examined:

- the agreed change scope,
- the protected baseline,
- the existing text behavior,
- possible unintended changes outside the intended area.

The non-loss check therefore adds a second perspective to ordinary functional testing: not only “Is the new behavior there?” but also “Is the existing behavior still what it is supposed to be?”

## 7. Eleven green tests – and still not finished

After the first implementation, everything initially looked good.

Eleven tests passed. The JSON output, decimal preservation, existing text behavior, protected baseline, and agreed change scope also showed no detected deviation.

At that point, it would have been easy to say: done.

This is where the evidence chain became important.

When requirements, risks, tests, and results were compared, one already required point for the new JSON path was still not explicitly demonstrated: How does the program behave when given invalid input?

No program defect had been discovered. Something else was missing: **explicit evidence for a failure case that had already been required**.

One more test was therefore added for exactly that case.

The result afterwards:

- 12 out of 12 tests passed,
- the tested JSON failure case ended with an error status,
- no JSON output file was produced,
- the related acceptance criterion was now explicitly demonstrated.

For me, this is the key point of the demo:

> **Green tests alone do not tell you whether everything that had previously been defined as necessary was actually tested.**

It is not the number of green tests that decides completion. The question is whether the required evidence exists for the agreed requirements and risks. KI-Workflower therefore shifts attention from merely running tests to the relationship between requirements and evidence.

**Evidence instead of a success count:** A test is not valuable because it is green. It is valuable because it is tied to a concrete **acceptance criterion**.

## 8. Finally, check the executable reality again

In addition to the functional evidence chain, technical completion checks were carried out at the end.

They covered:

- Python syntax and compilability,
- the complete test suite,
- the valid JSON reference,
- the real text report as a regression check,
- the real JSON output.

All five checks passed.

The completion decision therefore did not rest only on individual test statements. It also included checks against the actually executable final state.

## 9. What “FEUERFEST” means here

The term **FEUERFEST** is not meant to suggest that software can be guaranteed to be error-free.

It means something narrower and verifiable:

> **FEUERFEST is a demonstrated project state within a previously defined verification and evidence scope.**

For this demo, that status could therefore only be assigned at the end – after the previously defined conditions had actually been checked.

The verified state was:

- Acceptance criteria: **7/7 PASS**
- Risk controls: **6/6 PASS**
- Mini-FMEA measures: **5/5 PASS**
- Test suite: **12/12 PASS**
- Non-loss check: **PASS**
- Technical checks: **5/5 PASS**
- Completion status: **FEUERFEST**

The term is therefore not the claim. It is the summary of a demonstrated state.

## 10. What I want to show with this small demo

The software change was deliberately kept small. What matters here is not the size of the program, but the chain of effects created by the individual steps.

The PoC prevented an unsuitable technical approach from simply being carried forward.

QFD turned general expectations into concrete, testable characteristics.

The risk register connected possible failures with specific controls.

The Mini-FMEA revealed a failure scenario that actually expanded the test plan.

The non-loss check focused on what the change had to leave untouched.

And the evidence chain ultimately showed why eleven successful tests were still not enough.

Only after the missing evidence had been added and the technical completion checks had passed was the agreed verification and evidence scope complete.

To prevent **test results and the actual quality objective from drifting apart**, KI-Workflower shifts the perspective from

**“The coding agent says: done.”**

to

**“For the verified project state, there is traceable evidence explaining why it can be considered done.”**

## 11. The question behind KI-Workflower

In the end, the whole case study comes down to one simple question:

> **What proves that a specific requirement is actually fulfilled in the verified project state?**

Green tests are a means to an end. Only their deliberate connection to requirements and risks turns them into reliable evidence. KI-Workflower therefore does not ask this question only at the end; it builds it into the development process from the beginning.

**Publication notice**

This case study describes selected public principles, results, and evidence from KI-Workflower. The complete methodology and the internal implementation of the verification and evidence layer are not part of this publication.
