# cs555tmE2026Summer
GEDCOM Parsing and Display Repo for CS555 at Stevens Institute of Technology Summer 2026 semester

By: Shadman Choudhury, Nadia Lara, Derrick Sual

This will take a .ged GEDCOM file and parse it into tags which become individuals and families. It will extend to have these be related to one another and printed using the Python PrettyTables module. Additionally, this data will be validated and output errors in the case of invalid fields, tags, or inputs.

## Setup Instructions

To run this script, you'll need to set up a Python virtual environment and install the required dependencies:

1. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - **Windows:** `venv\Scripts\activate`
   - **Mac/Linux:** `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install prettytable
   ```

4. **Run the parser:**
   ```bash
   python GEDCOMParser.py
   ```

## Running Unit Tests

To run all unit tests in the repository, you can use the test runner script:

```bash
python run_tests.py
```

Alternatively, you can run tests using Python's built-in `unittest` module:

- **Run all tests:**
  ```bash
  python -m unittest discover -s Unittests -p "*.py"
  ```

- **Run a specific test file (e.g., US09):**
  ```bash
  python -m unittest Unittests.US09
  ```

