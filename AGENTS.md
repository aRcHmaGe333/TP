# Agent Rules

- IN CODEX CHAT EXTENSION (VSCODE), USE [] and () STYLE OF LINKING, NAME AND LINK, WITH RELATIVE LINKS ONLY.


MANDATORY EXECUTION RULES:
- Prevent failures (e.g. truncation of requested output); do not only refuse them. Placeholders and fallbacks are not allowed.
- Do not report problems as progress; solve them, rerun, then report.
- Overwrite bad outputs; do not submit known-bad runs.
- Submit only when results are satisfactory (close to 100%) against requirements.
- Satisfy all stated requirements at the same time (prevent regression and include previous requirements alongside the newest ones).
- Never fix one requirement by breaking previously satisfied behavior. Ensure compatibility of your changes with the previous good results. 
- Generate required QA on every run. Manually check the unambiguous data and make sure it matches the desired outcome (output). 
- Perform QA on every run and be aware of it (commit the result to current agent memory). If the result doesn't closely match the required outcome, iterate with precise, targeted, modular changes until it does.
- Locate and inspect the unambiguous data that confirms the output quality yourself and analyze them before submission.
- An attempt is not a result. Only a satisfactory output is a result. Should you require help reaching it, ask for help without presenting failures as notable checkpoints.
---
Restated more clearly:
---
1. Outcome Integrity

Deliver complete, final outputs only.
No truncation, placeholders, or partial fulfillment.
If output is not satisfactory → fix, rerun, replace.

2. Requirement Cohesion

All requirements must be satisfied simultaneously.
Never resolve one requirement by breaking another.
Preserve previously achieved correctness while extending.

3. Failure Handling

Do not report failures as progress.
Detect issues → correct → rerun → then report.
Known-bad outputs must be overwritten, not submitted.

4. Verification (QA Loop)

Perform QA on every run before submission.
Check against clear, objective signals in the output.
If mismatch exists → iterate with targeted fixes until resolved.

5. Iteration Discipline

Each iteration must be precise and minimal.
No random changes; isolate variables and adjust deliberately.
Continue until output is near-complete against all requirements.

6. Completion Rule

An attempt is not a result.
Only validated, requirement-complete output qualifies as a result.

7. Escalation

If progress stalls, request missing data or constraints.
Do not present incomplete work as a milestone.
---


## Local File Links

Use VS Code/Copilot-style markdown links with workspace-relative targets.

Required formats:

- `[label](relative/path/from/workspace/root)`
- `[label (line N)](relative/path/from/workspace/root#LNN)`

Mandatory constraints:

- never use absolute filesystem paths for local file references;
- never use `file://` links;
- never use browser-style URLs for local files;
- never use plain-text file paths when a file reference is intended;
- never mix multiple local-file link styles in one response.

Examples:

- `[AGENTS.md](AGENTS.md)`
- `[README.md](README.md)`
- `[README.md (line 10)](README.md#L10)`

When the relative path is uncertain, ask once or avoid linking rather than improvising.
