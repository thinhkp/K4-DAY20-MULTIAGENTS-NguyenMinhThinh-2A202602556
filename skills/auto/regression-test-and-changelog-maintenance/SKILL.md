---
name: regression-test-and-changelog-maintenance
description: Use this skill after fixing a bug to add a regression test and record the change in the changelog.
---
**Checklist**

1. **Create regression test file**  
   * If `tests/test_regressions.py` does not exist, create it.  
2. **Add a test per bug**  
   * Write a test function that reproduces the bug scenario and asserts the correct behaviour.  
3. **Run the full test suite**  
   * Ensure the new test passes and no other tests fail.  
4. **Update CHANGELOG.md**  
   * Under the `## Unreleased` section, add a bullet:  
     `- fix(<function name>): <short description>`  
   * Include at least three such bullets for the bugs you fixed.  
5. **Verify formatting**  
   * Ensure the changelog follows the project’s style (e.g., bullet list, proper indentation).  
6. **Commit**  
   * Commit the regression tests and the updated changelog together.
