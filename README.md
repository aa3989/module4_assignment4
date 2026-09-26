# Python Calculator — Module 4

A command-line calculator built with Python using object-oriented programming, a calculation factory, and automated tests. The calculator runs in a Read-Eval-Print Loop (REPL), allowing users to perform multiple calculations, view session history, and get help without restarting the program.

## Features

- Six arithmetic operations: addition, subtraction, multiplication, division, power, and modulus.
- Session history of successful calculations.
- Built-in help and exit commands.
- Error handling for invalid input, unsupported operations, and arithmetic errors.
- Graceful exit when interrupted with Ctrl+C or when input ends.
- Parameterized tests with pytest and branch coverage measurement.
- GitHub Actions workflow that requires 100% coverage.

## Requirements

- Python and pip installed on your computer.
- The packages listed in `requirements.txt`.
- Git, if cloning the project from GitHub.

## Installation

Download or clone this repository, then open a terminal in the project folder—the directory containing `main.py` and `requirements.txt`.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it using the command for your terminal:

**Windows PowerShell**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```bat
venv\Scripts\activate.bat
```

**macOS or Linux**

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

If your system uses `python3` instead of `python`, use `python3` when creating the virtual environment. After activation, use the environment's `python` command.

## Running the Calculator

From the project folder, run:

```bash
python main.py
```

Enter calculations in this format:

```text
<operation> <number1> <number2>
```

Separate the operation and operands with spaces. Operands are converted to floating-point numbers, so whole numbers, decimals, and negative numbers are supported.

| Operation | Description | Example | Result |
|---|---|---|---|
| `add` | Add two numbers | `add 10 5` | `15.0` |
| `subtract` | Subtract the second number from the first | `subtract 20 5` | `15.0` |
| `multiply` | Multiply two numbers | `multiply 7 8` | `56.0` |
| `divide` | Divide the first number by the second | `divide 20 4` | `5.0` |
| `power` | Raise the first number to the second number's power | `power 2 3` | `8.0` |
| `modulus` | Return the remainder using Python's `%` operator | `modulus 10 3` | `1.0` |

For negative operands, modulus follows Python's sign convention. For example, `modulus -10 3` returns `2.0`.

### Special Commands

| Command | Purpose |
|---|---|
| `help` | Display usage instructions and supported operations |
| `history` | Display successful calculations from the current session |
| `exit` | Close the calculator |

History is stored in memory and is cleared when the calculator closes. Failed calculations are not added to history.

### Example Session

```text
>> power 2 3
Result: PowerCalculation: 2.0 Power 3.0 = 8.0

>> modulus 10 3
Result: ModulusCalculation: 10.0 Modulus 3.0 = 1.0

>> history
Calculation History:
1. PowerCalculation: 2.0 Power 3.0 = 8.0
2. ModulusCalculation: 10.0 Modulus 3.0 = 1.0

>> exit
Exiting calculator. Goodbye!
```

## Error Handling

The calculator reports errors and allows the user to enter another command. Examples include:

- Missing or extra operands, such as `add 5` or `add 1 2 3`.
- Non-numeric operands, such as `add ten five`.
- Unsupported operations, such as `unknown 2 3`.
- Division or modulus by zero.
- Raising zero to a negative power.

The operation and calculation layers have distinct exception contracts. For example, `Operation.modulus(10, 0)` raises `ValueError`, while `ModulusCalculation(10, 0).execute()` raises `ZeroDivisionError`. The REPL handles calculation errors and presents feedback to the user.

## Project Structure

```text
app/
    __init__.py
    calculator/
        __init__.py       # REPL, help, input handling, and history
    calculation/
        __init__.py       # Abstract base, calculation classes, and factory
    operation/
        __init__.py       # Arithmetic methods
tests/
    __init__.py
    conftest.py           # Reset registered calculations between tests
    test_calculation.py   # Calculation and factory tests
    test_calculator.py    # REPL and command tests
    test_operations.py    # Arithmetic method tests
.github/
    workflows/
        tests.yml         # Automated tests and coverage enforcement
.coveragerc               # Branch coverage configuration
.gitignore
main.py                   # Application entry point
pytest.ini                # Test discovery and coverage options
requirements.txt          # Project dependencies
README.md
```

## Testing and Coverage

Run the test suite from the project folder with the virtual environment activated:

```bash
python -m pytest
```

The project configuration enables coverage reporting and generates an HTML report. To explicitly measure branch coverage and enforce the assignment's 100% threshold, run:

```bash
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=100
```

The command exits unsuccessfully if a test fails or measured coverage is below 100%. Open `htmlcov/index.html` in a browser to inspect the generated report.

The tests cover arithmetic methods, calculation classes, factory registration, command handling, history, invalid inputs, arithmetic errors, and graceful termination. Parameterized tests exercise multiple inputs with the same test logic. An automatic fixture restores all six registered operations before each test.
