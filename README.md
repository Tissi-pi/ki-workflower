# KI-Workflower

**Evidence before approval.**

> **The coding agent does not decide when the work is done.  
> The verified project state does.**

KI-Workflower is a **tool-independent verification and evidence layer for AI-assisted software development**.

It complements existing development methods and coding agents by systematically linking **requirements, risks, acceptance criteria, verification activities, and concrete evidence**.

## New Thinking | Proven Practices

KI-Workflower applies industry-proven **approaches to quality and risk control** to collaboration with coding agents. These include:

- Proof of Concept (PoC)
- Quality Function Deployment (QFD)
- risk registers
- Mini-FMEA
- explicit acceptance criteria
- traceable verification results

The simplified evidence chain is:

**Requirement → Acceptance criterion → Risk → Verification → Verification result**

This makes one central question transparently answerable at any time:

> **What evidence demonstrates that a specific requirement is actually satisfied in the verified project state?**

## More than “tests passed”

A passed test shows that the conditions covered by that test are satisfied – but not whether unintended changes occurred outside the agreed scope of change.

**KI-Workflower therefore also verifies the agreed scope of change:**

- What was allowed to change?
- What had to remain unchanged?

The **non-loss verification** therefore complements functional evidence by checking whether unintended changes or losses occurred outside the agreed scope of change.

## Methodology before tools

Coding agents and development environments evolve rapidly – the **verification and evidence logic of KI-Workflower is decoupled from them**.

Approval of a project state is not determined by the executing tool, but by the overarching framework of **requirements, acceptance criteria, verification activities, and evidence**.

KI-Workflower therefore treats coding agents as interchangeable components within a stable methodological framework.

## Connecting to existing ecosystems

KI-Workflower is designed to be tool-independent and can complement existing agent-assisted and spec-driven development workflows.

Possible points of integration include **GitHub Spec Kit, OpenSpec, and Kiro**, as well as other agent-assisted development environments.

**KI-Workflower does not replace these systems. It builds on the existing development workflow and, where useful, supplements it with additional quality and risk practices as well as an independent verification and evidence layer.**

## Public scope

This repository deliberately presents only the part of KI-Workflower intended for public release.

Published here are selected conceptual foundations, evidence principles, a small transparent demonstrator, and possible integration approaches.

The complete internal methodology, as well as internal verification, automation, and control mechanisms, are explicitly not part of this public repository.

The aim is to present how KI-Workflower works, what it contributes, and how it can connect to existing workflows without fully disclosing the internal implementation.
