### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: execute
{"command": "bash -lc \"python - <<'PY'\nprint('test')\nPY\""}

### Tool result
test

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "bash -lc \"pytest -q\""}

### Tool result

==================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py _______________
ImportError while importing test module '/mnt/d/workspace/vinai/.K4-DAY20-MULTIAGENTS-NguyenMinhThinh-2A202602556-lab-bse__ena/workspace/tests/test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../K4-DAY20-MULTIAGENTS-NguyenMinhThinh-2A202602556/tasks/code-eval/workspace/tests/test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ============================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 3.40s

Exit code: 2
[Command failed with exit code 2]

### Tool call: ls
{"depth": 3, "path": ""}

### Tool result
['/.pytest_cache/', '/workspace/']

### Tool call: ls
{"depth": 3, "path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']