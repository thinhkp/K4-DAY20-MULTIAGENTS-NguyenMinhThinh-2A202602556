---
name: docstring-compliance-check
description: Use this skill when you need to verify that a function’s implementation matches its docstring specification.
---
**Checklist**

1. **Read the docstring**  
   * Identify the function’s purpose, input parameters, return value, and any side‑effects or exceptions.  
2. **Translate spec to tests**  
   * Write unit tests that exercise all described behaviours, including edge cases.  
3. **Run the tests**  
   * If any test fails, the implementation does not comply.  
4. **Fix the implementation**  
   * Adjust code until all tests pass.  
5. **Re‑run tests**  
   * Confirm that the function now satisfies the docstring.  
6. **Document the fix**  
   * Add a brief comment or note if the change was non‑obvious.  
7. **Commit**  
   * Ensure the new tests are committed alongside the code change.
