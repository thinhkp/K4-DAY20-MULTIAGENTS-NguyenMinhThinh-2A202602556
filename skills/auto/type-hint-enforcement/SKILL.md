---
name: type-hint-enforcement
description: Use this skill to add missing type annotations to all public functions in a module.
---
**Checklist**

1. **Scan the module**  
   * List all functions whose names do not start with `_`.  
2. **Check annotations**  
   * For each function, verify that every parameter and the return value have type hints.  
3. **Add missing hints**  
   * Use `typing` primitives (`int`, `str`, `float`, `List`, `Dict`, etc.) or custom types as appropriate.  
4. **Run a static type checker**  
   * Execute `mypy` or similar to confirm no missing annotations remain.  
5. **Update documentation**  
   * If the function’s signature changes, update the docstring accordingly.  
6. **Commit**  
   * Commit the annotated code and any updated docs.
