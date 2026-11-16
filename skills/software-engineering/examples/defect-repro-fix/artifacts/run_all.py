"""既有测试入口：逐个按路径加载 tests/ 下的测试文件。

隔离模式下不使用 `unittest discover`，避免依赖包结构与 -m 形式。
"""
import importlib.util
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    suite = unittest.TestSuite()
    tests_dir = os.path.join(ROOT, "tests")
    for filename in sorted(os.listdir(tests_dir)):
        if filename.startswith("test_") and filename.endswith(".py"):
            module = load(os.path.join(tests_dir, filename), filename[:-3])
            suite.addTests(unittest.TestLoader().loadTestsFromModule(module))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
