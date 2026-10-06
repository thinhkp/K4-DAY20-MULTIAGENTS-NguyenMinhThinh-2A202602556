# Lab Report: Self evolving Agentic

## 1. Student and configuration

- Name: Nguyen Minh Thinh
- Student ID: 2A202602556
- Provider/model for the formal learning runs: Groq OpenAI-compatible API, `openai/gpt-oss-20b`; temperature 0; `recursion_limit` 60. The API key is stored only in the ignored local `.env` file.
- Deep Agents: 0.7.21; Python 3.14.4 in the project WSL environment (Ubuntu on Windows).
- Formal runs: 9 learning-task runs (3 tasks ? 3 conditions), plus one curator invocation. No evaluation-task runs; no `hypotheses` commit or `freeze` tag.
- The table below includes only the consistent GPT-OSS 20B learning runs. Different-model probes are kept under `results/pilot-*` and excluded from the comparison.

## 2. Hypotheses (draft, written before any evaluation runs)

- H1 (subagents vs baseline): I expect subagents can improve partial scores on multi-step tasks by separating exploration, implementation, and review, but may use more tokens due to delegation and context transfer. This follows the subagent roles and delegation overhead described in `GUIDE.md`.
- H2 (skills-auto vs baseline): I expect generated skills may improve recurring process conventions, but may not reliably fix task-specific technical errors and may overfit. The curator can only learn from feedback and traces in the learning set (`guides/pseudocode/04_curator.md`).
- H3 (learning vs evaluation): I expect evaluation scores to be lower because evaluation tasks use new data and add a convention not present in their learning pair (`README.md`, section 2.2).

These hypotheses were written before any evaluation run. No evaluation task, evaluation trace, or evaluation checker has been opened. I will commit this pre-evaluation report as `hypotheses` and tag the current generated skills before running evaluation tasks.

## 3. Deep Agents orientation (Part 0.3)

1. The default agent exposes file tools (`ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`), the shell tool `execute`, and the subagent tool `task`.
2. The `task` tool launches an ephemeral subagent for complex multi-step work. Delegation is stateless by default, so the main agent should pass the relevant instructions and paths in its message.
3. The `task` tool description says it launches an ephemeral subagent for a complex, multi-step task. The `execute` tool description says it executes a shell command in an isolated sandbox and returns combined output with the exit code. The default system prompt printed by `scripts/tour.py` is empty.

## 4. Baseline and error taxonomy (Part 2.2)

The formal baseline runs are in `results/baseline/`. `code-learn` scored 0/10. Its trace shows only directory listing and file reads; it does not show a code edit, shell/test command, or verification. The `rule_type_hints`, `rule_regression_tests`, and `rule_changelog` checks all failed (group E: organization conventions). The `visible_suite_passes` and implementation checks failed; because the trace contains no test run or verification, these are consistent with group B. The `tests_not_modified` check also failed, but the trace does not expose an action explaining that result, so I cannot confidently attribute its cause.

The `data-learn` run ended with a Groq `tool_use_failed` error while parsing the model's shell-tool arguments. The `logs-learn` run made only three tool calls, all visible in its trace as reads; it produced no `errors.json`. Per the guide, provider failures are infrastructure failures, not agent failures, so I exclude the `data-learn` error from the taxonomy and do not treat either run as evidence about the task-solving skill of the agent.

| Task | Failed check / outcome | Group | Evidence |
|---|---|---|---|
| `code-learn` | `rule_type_hints`, `rule_regression_tests`, `rule_changelog` | E | All three `rule_` checks failed in `results/baseline/code-learn/run.json`. |
| `code-learn` | `visible_suite_passes` and implementation checks | B / G | `trace.md` shows file reads only; no edit, test execution, or result verification. |
| `code-learn` | `tests_not_modified` | Unclear | The checker failed this constraint, but the trace does not show the action that triggered it. |
| `data-learn` | Tool-call JSON parse error | Infrastructure | `run.json` records `OpenAIInvalidRequestError`; not counted as an agent error. |
| `logs-learn` | Required output missing | B / G | Trace shows reads of the README and log file, but no shell call or output write. |

The three convention checks are the clearest recurring pattern in the only baseline run that completed without a provider error. This is too little evidence to claim they are the majority failure mode across tasks.

## 5. `subagents` condition (Part 2.3)

Three distinct subagents are implemented in `src/lab/subagents.py`: `explorer` (read-only inspection), `implementer` (focused edits), and `reviewer` (read-only review). The formal `subagents` learning runs all recorded `subagent_calls: 0`. The `code-learn` trace shows inspection calls but no `task` delegation. The `data-learn` and `logs-learn` runs ended in tool-call parsing errors before delegation.

Mean recorded tokens were 9,190 per run for `subagents` and 12,131 for `baseline`, but both conditions scored 0 on all three tasks, and the subagents condition made no delegation calls. The lower token count therefore reflects incomplete runs and is not evidence that delegation is more efficient.

## 6. Self-evolving skills (Part 3)

`python -m lab.curator` generated three skills from baseline learning feedback. They were not manually edited:

| Skill | General or task-specific? | Quality review | Length and description |
|---|---|---|---|
| `docstring-compliance-check` | General | Correct checklist: read specification, test behavior, fix and re-run tests. | 20 lines; description matches its use. |
| `type-hint-enforcement` | General, prompted by a code-task convention | Mostly correct. The optional `mypy` step may add work when that tool is unavailable. | 18 lines; description identifies public-function annotation work. |
| `regression-test-and-changelog-maintenance` | More specific to this lab's code-task conventions | Correct for the convention feedback; the fixed filenames and changelog format reduce generality. | 20 lines; description accurately describes when to use it. |

The formal `skills-auto` learning runs all failed before any tool call; `skills_read` is 0/3. Therefore these runs provide no evidence that the agent read or followed the skills. The curator generated valid-looking learning skills, but their effect has not been measured.

## 7. Comparison results (Parts 4.3 and 4.4)

`report/table.md` was generated by `python -m lab.compare` from the nine consistent GPT-OSS 20B learning runs. It is a **partial table**: evaluation rows are absent, and the zeros include provider failures and incomplete agent runs. It is not a completed comparison.

| Task | baseline | subagents | skills-auto |
|---|---:|---:|---:|
| code-learn | 0/10 | 0/10 | 0/10 |
| data-learn | 0/8 | 0/8 | 0/8 |
| logs-learn | 0/9 | 0/9 | 0/9 |
| Mean score - learning tasks | 0.00 | 0.00 | 0.00 |
| Mean score - evaluation tasks | - | - | - |
| Mean tokens per run | 12,131 | 9,190 | 8,454 |
| Runs that read a skill | 0/3 | 0/3 | 0/3 |

No freeze verification has been attempted because no `freeze` tag exists.

## 8. Analysis

1. **Learning/evaluation score changes:** all formal learning scores are 0. No evaluation runs exist, so there is no measured transfer result.
2. **Technical vs. convention checks:** in baseline `code-learn`, the breakdown is 0/7 non-`rule_` checks and 0/3 `rule_` checks. The trace indicates the agent stopped after inspection. The data/log task records are affected by provider/tool failures, so the all-zero table should not be read as a clean comparison of agent quality.
3. **Skill use:** the formal `skills-auto` runs have `skills_read: 0` and no tool calls; the skill files were not read in those runs.
4. **Tokens and delegation:** mean tokens are shown in the table. `subagent_calls` is 0 in every formal run, so the value of delegation cannot be estimated. Score-per-token is also not informative when every recorded score is 0 and some calls failed at the provider layer.
5. **Leakage/overfitting:** no evaluation task or result was opened before the freeze stage. The three curator outputs contain general process advice and learning-set convention details; there is not enough evaluation evidence to judge transfer or overfitting.
6. **Before/after freeze variation:** not measured; no frozen run exists.

### Provider and model diagnostics

The formal model `openai/gpt-oss-20b` completed a simple tool-call probe, but its task runs frequently returned malformed shell-tool arguments or stopped after reading files. A separate Qwen `qwen/qwen3.8-27b` probe produced a better `code-learn` result (6/10, 44,855 tokens, 311.2 seconds), but subsequent data/log prompts exceeded the account's 7,000 input-tokens-per-minute on-demand limit. A GPT-OSS 120B probe called an unregistered `exec` tool and was rejected. These different-model probes are retained under `results/pilot-*` and excluded from the main table; mixing them would make the comparison inconsistent.

## 9. Limitations and validity

1. The task set has only three task families, one learning/evaluation pair each.
2. Each formal condition/task has one run; model sampling and tool behavior can cause substantial noise.
3. The accessible GPT-OSS 20B model did not reliably execute the lab's shell tools; several data/log runs failed at Groq's tool-call parser.
4. Qwen's prompt size exceeded the account's on-demand ITPM limit for two task families. Completing the full comparison with that model requires a higher Groq tier or another endpoint with sufficient limits.
5. No evaluation runs, frozen skill runs, or freeze verification exist, so no claim about generalization, overfitting, or skill benefit is supported.
6. The evidence is provider- and model-specific and cannot be generalized to other models.

## 10. Conclusion

The four harness modules are implemented, the 32 offline tests passed in the earlier verification run, and `scripts/tour.py` completed with the fake model. Groq connectivity works, and the curator generated three skills from baseline feedback. However, the available Groq tier/model combination did not produce reliable task runs: recorded scores are all zero, several runs failed in tool-call parsing, skills were not read, and evaluation/freeze steps remain incomplete. The empirical results do not support conclusions about baseline vs. subagents vs. self-evolving skills. A provider/model with sufficient input-token limits and reliable tool-call serialization is needed to complete the evaluation.

## Appendix

- Formal commands run in WSL: `python -m lab.runner --condition baseline --tasks learn`; `python -m lab.runner --condition subagents --tasks learn`; `python -m lab.curator`; `python -m lab.runner --condition skills-auto --tasks learn`; and `python -m lab.compare`.
- Offline verification from the earlier implementation pass: 32 tests passed across `tests/test_01_provided.py` through `tests/test_04_curator.py`; `scripts/tour.py` completed with a fake model.
- `vlearn-intrucd.md` describes a Coordinator/Worker lab, while this repository's `README.md`, `GUIDE.md`, and `RUBRIC.md` define the Self evolving Agentic lab. The implementation follows the checked-out repository's requirements.
- Evaluation runs, freeze tag, freeze verification, final six-task comparison, and optional extension: not completed.

