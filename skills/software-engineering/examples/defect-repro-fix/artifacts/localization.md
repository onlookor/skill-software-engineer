---
evidence_kind: direct
files:
  - calc.py
estimated_touched_files: 1
estimated_diff_lines: 2
---

`add()` 的实现把加法写成了减法；失败栈直接指向 `calc.py` 的 `return` 语句，
故标 `direct`。
