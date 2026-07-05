import unittest
import sys


def main():
    # Discover and run all tests in the 'Unittests' folder matching '*.py'
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="Unittests", pattern="*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with code 1 if tests failed, so CI/CD or other tools detect the failure
    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()
