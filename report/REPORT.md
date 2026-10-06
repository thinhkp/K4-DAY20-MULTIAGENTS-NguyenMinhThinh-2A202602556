# Lab Report: Self evolving Agentic

## 1. Student and configuration

- Name: Nguyen Minh Thinh
- Student ID: 2A202602556
- Formal provider/model: Groq OpenAI-compatible API, `openai/gpt-oss-20b`; temperature 0; `recursion_limit` 60. The key is in the ignored local `.env` file and is not recorded here.
- Deep Agents: 0.7.21; Python 3.14.4 in the project WSL environment (Ubuntu on Windows).
- Formal results: 18 task runs (3 conditions ? 6 tasks), plus 3 pre-freeze `skills-auto` learning runs saved under `results/skills-auto-dev/` and one curator invocation. All formal task records are in `results/`.
- Hypotheses commit: `ba6961f` (`hypotheses`). Freeze tag: `a353a04` (`freeze`). `scripts/verify_freeze.py` reports `OK` for all 6 post-freeze skills-auto runs.

## 2. Hypotheses (written before evaluation runs)

- H1 (subagents vs baseline): I expect subagents can improve partial scores on multi-step tasks by separating exploration, implementation, and review, but may use more tokens because of delegation and context transfer. This follows the roles and delegation flow described in `GUIDE.md`.
- H2 (skills-auto vs baseline): I expect generated skills may improve recurring process conventions but may not reliably fix task-specific technical errors and may overfit. The curator can only learn from feedback and traces in the learning set (`guides/pseudocode/04_curator.md`).
- H3 (learning vs evaluation): I expect evaluation scores to be lower because evaluation tasks use new data and add a convention not present in their learning pair (`README.md`, section 2.2).

These hypotheses were committed in `ba6961f` before the `freeze` tag. Evaluation runs and outputs were first examined after the tag was created.

## 3. Deep Agents orientation (Part 0.3)

1. The default agent exposes file tools (`ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`), the shell tool `execute`, and the subagent tool `task`.
2. The `task` tool launches an ephemeral subagent for complex, multi-step work. Delegation is stateless by default, so the main agent should pass the relevant instructions and paths in its message.
3. The `task` tool description says it launches an ephemeral subagent for a complex, multi-step task. The `execute` tool description says it executes a shell command in an isolated sandbox and returns combined output with the exit code. The default system prompt printed by `scripts/tour.py` is empty.

## 4. Baseline and error taxonomy (Part 2.2)

For the learning-set taxonomy, `code-learn` scored 0/10 and `logs-learn` scored 0/9 without a provider error. Their traces show only directory/file reads and no edit, shell/test command, or verification. This is consistent with group B (no verification) and group G (the task was left incomplete). In `code-learn`, `rule_type_hints`, `rule_regression_tests`, and `rule_changelog` also failed (group E: organization conventions). The `tests_not_modified` check failed too, although the trace does not expose the action that caused it, so I cannot confidently classify its cause.

`data-learn` ended with Groq's `tool_use_failed` error while parsing the model's shell-tool arguments. Per the guide, provider failures are infrastructure failures, not agent failures, so that run is excluded from the agent error taxonomy. The failed convention checks are evidence only for the completed `code-learn` run; one task is not enough to claim they dominate across task families.

| Task | Failed check / outcome | Group | Evidence |
|---|---|---|---|
| `code-learn` | `rule_type_hints`, `rule_regression_tests`, `rule_changelog` | E | All three `rule_` checks failed in `results/baseline/code-learn/run.json`. |
| `code-learn` | Visible suite and implementation checks | B / G | Trace contains directory listings and file reads, but no edit, shell/test call, or verification. |
| `code-learn` | `tests_not_modified` | Unclear | Checker failed this constraint, but trace does not show the action that triggered it. |
| `data-learn` | Tool-call JSON parse error | Infrastructure | `run.json` records `OpenAIInvalidRequestError`; not treated as an agent error. |
| `logs-learn` | Required output missing | B / G | Trace shows reads of the README and log file, but no shell call or output write. |

## 5. `subagents` condition (Part 2.3)

Three distinct subagents are implemented in `src/lab/subagents.py`: `explorer` (read-only inspection), `implementer` (focused edits), and `reviewer` (read-only review). All six formal `subagents` runs recorded `subagent_calls: 0`. The `code-learn` trace shows inspection but no `task` delegation; several other runs failed in Groq before a tool call.

The comparison table reports a mean of 10,334 tokens per `subagents` run and 10,419 for `baseline`. Both conditions scored 0 on every task, and no subagent was called. The small token difference reflects incomplete/erroring runs and is not evidence that delegation is more efficient.

## 6. Self-evolving skills (Part 3)

`python -m lab.curator` generated three skills from baseline learning feedback. They were not manually edited:

| Skill | General or task-specific? | Quality review | Length and description |
|---|---|---|---|
| `docstring-compliance-check` | General | Correct checklist: read the specification, test behavior, fix, and re-run tests. | 20 lines; description matches its use. |
| `type-hint-enforcement` | General, prompted by a code-task convention | Mostly correct. The optional `mypy` step may add work when that tool is unavailable. | 18 lines; description identifies public-function annotation work. |
| `regression-test-and-changelog-maintenance` | Specific to this lab's code-task conventions | Correct for the feedback; fixed filenames and changelog format reduce generality. | 20 lines; description accurately describes when to use it. |

The 3 pre-freeze `skills-auto` learning runs and 6 post-freeze runs all have `skills_read: 0`. Their traces/run errors show that the model failed before reading a skill or, in rate-limited cases, before an inference completed. Therefore there is no evidence that the agent followed these skills or that they improved task scores.

## 7. Comparison results (Parts 4.3 and 4.4)

The following table was generated by `python -m lab.compare` from the 18 formal runs. It matches `report/table.md`.

| Task | baseline | subagents | skills-auto |
|---|---:|---:|---:|
| code-learn | 0/10 | 0/10 | 0/10 |
| data-learn | 0/8 | 0/8 | 0/8 |
| logs-learn | 0/9 | 0/9 | 0/9 |
| code-eval | 0/11 | 0/11 | 0/11 |
| data-eval | 0/9 | 0/9 | 0/9 |
| logs-eval | 0/10 | 0/10 | 0/10 |
| **Mean score - learning tasks** | 0.00 | 0.00 | 0.00 |
| **Mean score - evaluation tasks** | 0.00 | 0.00 | 0.00 |
| **Mean tokens per run** | 10,419 | 10,334 | 2,010 |
| **Runs that read a skill** | 0/6 | 0/6 | 0/6 |

Freeze verification passed: all 6 post-freeze `skills-auto` run records use the frozen skill hash, have `skills_modified: false`, and start after the freeze tag. The 2,010-token mean for `skills-auto` includes four calls rejected at the provider's daily token limit with zero reported tokens; it should not be read as an efficiency gain.

## 8. Analysis

1. **Learning/evaluation score changes:** all recorded scores are 0 in all conditions. This gives no evidence of an improvement or a transfer difference; provider errors and incomplete runs prevent a clean agent-quality comparison.
2. **Technical vs. convention checks:** `scripts/check_breakdown.py` reports 0/18 technical and 0/9 house-rule checks for baseline learning, and 0/18 technical and 0/12 house-rule checks for baseline evaluation. For `code-learn` specifically, 0/7 non-`rule_` checks and 0/3 `rule_` checks passed. The trace indicates the agent stopped after inspection. Data/log tasks with parser errors should not be interpreted as ordinary agent failures.
3. **Skill use:** all six final `skills-auto` runs have `skills_read: 0`; traces provide no evidence the agent read or followed any generated skill.
4. **Tokens and delegation:** means are in the table. `subagent_calls` is 0 in every formal run, so delegation's value cannot be estimated. Score per token is not meaningful when every score is 0. The low skills-auto token average is caused partly by four quota-rejected calls with zero usage metadata.
5. **Leakage/overfitting:** hypotheses and skills were frozen before any evaluation run. No evaluation data was used to create the skills. Since the agent never read a skill in the formal runs, this experiment cannot establish transfer or rule out overfitting.
6. **Before/after freeze variation:** learning scores are 0/10, 0/8, and 0/9 both in the pre-freeze development runs and in the final frozen condition. Those equal scores are not evidence of no variation: the runs were incomplete or failed before skill use.

### Provider and model diagnostics

The formal model `openai/gpt-oss-20b` completed a simple tool-call probe, but its task runs frequently returned malformed shell-tool arguments or stopped after reading files. Four of the six final skills-auto calls were rejected at Groq's 200,000 tokens/day on-demand limit. A separate Qwen `qwen/qwen3.8-27b` probe completed `code-learn` at 6/10 (44,855 tokens, 311.2 seconds), but its data/log prompts exceeded the account's 7,000 input-tokens-per-minute limit. A GPT-OSS 120B probe called an unregistered `exec` tool and was rejected. These different-model probes are stored under `results/pilot-*` and excluded from the comparison so all formal conditions use the same model.

## 9. Limitations and validity

1. The task set has only three task families, with one learning/evaluation pair each.
2. Each formal condition/task has one run; model/tool behavior can cause substantial noise.
3. The accessible GPT-OSS 20B model did not reliably serialize shell tool calls, and several tasks stopped without editing or writing output.
4. The Groq on-demand token limits rejected Qwen prompts and four GPT-OSS requests. A higher tier or another endpoint with sufficient limits is needed for a reliable rerun.
5. No formal run read a skill and all task scores are zero, so the experiment cannot support conclusions about self-evolution or generalization.
6. Results are specific to this provider/model configuration and should not be generalized to other models.

## 10. Conclusion

The four harness modules are implemented, the 32 offline tests passed in the earlier verification run, and `scripts/tour.py` completed with the fake model. Groq connectivity works; the curator generated three skills; the pre-evaluation hypotheses commit, freeze tag, and freeze verification are complete. The full result table is present, but all scores are zero and many runs failed at the provider/tool layer. These data do not support a conclusion about baseline vs. subagents vs. self-evolving skills. A more capable, accessible model with reliable tool-call serialization and sufficient token limits is needed for a meaningful rerun.

## Appendix

- Commands run in WSL: `python -m lab.runner --condition baseline --tasks learn`; `python -m lab.runner --condition subagents --tasks learn`; `python -m lab.curator`; `python -m lab.runner --condition skills-auto --tasks learn`; `python -m lab.runner --condition baseline --tasks eval`; `python -m lab.runner --condition subagents --tasks eval`; `python -m lab.runner --condition skills-auto --tasks all`; `python scripts/verify_freeze.py`; `python -m lab.compare`; and `python scripts/check_breakdown.py`.
- Offline verification from the earlier implementation pass: 32 tests passed across `tests/test_01_provided.py` through `tests/test_04_curator.py`; `scripts/tour.py` completed with a fake model.
- `vlearn-intrucd.md` describes a Coordinator/Worker lab, while this repository's `README.md`, `GUIDE.md`, and `RUBRIC.md` define the Self evolving Agentic lab. The implementation follows the checked-out repository's requirements.
- Different-model pilots are not in `report/table.md`. No optional extension was completed.
