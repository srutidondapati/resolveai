# ResolveAI Project Plan

## Goal
ResolveAI is a small Python portfolio project that helps debug Python code by combining static analysis, retrieval of similar examples, LLM guidance, controlled patching, and automated verification.

The core principle is simple: the LLM suggests fixes, but Python code and tests decide whether a fix is accepted.

## Scope
This project should stay intentionally small and focused.

In scope:
- A single Python file or small code sample as input.
- Basic AST or static analysis for obvious issues.
- A tiny local knowledge base of prior debugging examples.
- LLM-based diagnosis and fix suggestions.
- Controlled application of one proposed fix at a time.
- Pytest-based verification and retry handling.

Out of scope for the first version:
- Large-scale multi-file refactoring.
- Web UI, authentication, or cloud storage.
- Complex agent orchestration frameworks.
- Support for many languages.

## High-Level Architecture

1. Input Layer
	Accepts a Python source file plus an error message or test failure.

2. Analysis Layer
	Uses Python AST and lightweight static checks to extract useful facts about the code.

3. Retrieval Layer
	Searches a small local knowledge base for similar failures, patterns, and fixes.

4. LLM Layer
	Sends the source code, failure details, static analysis results, and retrieved examples to an LLM.

5. Fix Proposal Layer
	Turns the LLM response into a structured diagnosis and a proposed patch.

6. Execution Layer
	Applies the patch in a controlled way and runs pytest.

7. Verification Layer
	Decides whether the fix succeeded based on test results, not LLM confidence.

8. Retry Layer
	If tests still fail, sends the new failure back to the LLM for a limited number of revision attempts.

9. Reporting Layer
	Produces a final result for the user, including what was fixed or why the fix did not pass.

## Components and Responsibilities

### 1. Input Collector
Responsibilities:
- Receive the target file and failure output.
- Normalize paths and basic metadata.
- Pass a clean task bundle to the rest of the system.

### 2. Static Analyzer
Responsibilities:
- Parse Python code with the AST module.
- Identify functions, classes, imports, and obvious syntax or structure issues.
- Produce a compact summary for the LLM.

### 3. Example Retriever
Responsibilities:
- Search a small local set of debugging examples.
- Return only the most relevant matches.
- Keep the knowledge base simple, such as JSON or markdown entries.

### 4. Prompt Builder
Responsibilities:
- Combine code, error details, analysis output, and examples into one request.
- Ask the LLM for a diagnosis and a concrete patch proposal.
- Keep the prompt structured and repeatable.

### 5. LLM Client
Responsibilities:
- Send requests to the model.
- Receive the proposed diagnosis and fix.
- Never apply changes directly without validation.

### 6. Patch Controller
Responsibilities:
- Convert the proposal into a controlled code change.
- Limit edits to the intended file or region.
- Avoid wide or accidental changes.

### 7. Test Runner
Responsibilities:
- Run pytest after each proposed fix.
- Capture pass/fail output and failure traces.
- Return only the facts needed for the next decision.

### 8. Decision Engine
Responsibilities:
- Check whether tests passed.
- Allow only a small number of retry rounds.
- Stop when the fix works, the budget is exhausted, or the evidence is unclear.

### 9. Result Reporter
Responsibilities:
- Summarize the final diagnosis, fix attempt, and verification outcome.
- Tell the user whether the solution is confirmed by tests.
- Include remaining risks if the fix did not fully succeed.

## Development Phases

### Phase 1: Minimal Prototype
- Accept one Python file and one failure message.
- Extract a simple AST summary.
- Store a few example debugging cases locally.
- Send one prompt to the LLM.
- Print the suggested fix without applying it automatically.

### Phase 2: Controlled Fixing
- Add structured patch generation.
- Apply one fix to the target file.
- Run pytest after the change.
- Capture and report pass/fail results.

### Phase 3: Revision Loop
- Feed new test failures back into the LLM.
- Limit retries to a small fixed number.
- Stop after the limit is reached.

### Phase 4: Polish for Portfolio
- Improve logs and reporting.
- Add a few more retrieval examples.
- Tighten the prompt format.
- Add a couple of small demo cases.

## Success Criteria
- The system can accept a Python file and failure message.
- The system can produce a plausible diagnosis and fix proposal.
- Pytest determines whether the fix is actually correct.
- Retry behavior is limited and predictable.
- The project remains small enough to understand in one sitting.

## Guiding Constraints
- Keep the system simple and explicit.
- Prefer deterministic Python checks over model assumptions.
- Treat the LLM as a helper, not an authority.
- Optimize for clarity over breadth.

## Suggested Final Shape
The final portfolio version should look like a lightweight debugging pipeline, not a full autonomous agent platform. That keeps the project realistic, explainable, and easy to demo.
