"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use when a task requires understanding an unfamiliar repository, data file, "
                "or set of instructions before making changes. Return verified facts and relevant paths; do not edit files."
            ),
            "system_prompt": (
                "You are a repository and data explorer. Inspect only the files and task context named in the delegation. "
                "Report concise, verifiable findings, exact relative paths, relevant constraints, and uncertainties. "
                "Do not change files or invent facts."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when a task needs a focused code or data change that can be completed independently. "
                "Make the requested change, then run only the relevant checks and report their outcomes."
            ),
            "system_prompt": (
                "You are a focused implementation engineer. Follow the delegated requirements and use the smallest "
                "complete change. Inspect relevant files before editing, preserve unrelated work, and run the checks "
                "the delegation requests. Report changed files, commands, results, and any remaining issue."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use after a non-trivial implementation when an independent review can catch requirement gaps, "
                "edge cases, or regressions. Return findings with evidence; do not modify files."
            ),
            "system_prompt": (
                "You are an independent code and result reviewer. Compare the delegated request with the current "
                "changes and relevant checks. Look for correctness issues, missed requirements, and unsafe assumptions. "
                "Do not edit files. List findings first with file paths and concrete evidence; state when you find none."
            ),
        },
    ]
