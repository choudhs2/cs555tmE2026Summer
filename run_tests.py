import unittest
import sys


def main():
    # Discover and run all tests in the 'Unittests' folder matching '*.py'
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="UnitTests", pattern="*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    with open("test_summary.txt", "w") as f:
        f.write("Test Summary\n")
        f.write(f"Tests run:  {result.testsRun}\n")
        f.write(f"Passed:     {result.testsRun - len(result.failures) - len(result.errors)}\n")
        f.write(f"Failures:   {len(result.failures)}\n")
        f.write(f"Errors:     {len(result.errors)}\n")
        f.write(f"Overall result: {'PASS' if result.wasSuccessful() else 'FAIL'}\n")

    # Exit with code 1 if tests failed, so CI/CD or other tools detect the failure
    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()
