
"""
Unit tests for the calculator REPL.

Tests cover help, history, arithmetic operations, invalid input,
unsupported operations, division by zero, and graceful termination.
"""

from io import StringIO

import pytest

from app.calculator import calculator, display_help, display_history


def run_calculator(monkeypatch, user_input):
    """Run the calculator with simulated user input."""
    monkeypatch.setattr("sys.stdin", StringIO(user_input))

    with pytest.raises(SystemExit) as exc_info:
        calculator()

    return exc_info


def test_display_help(capsys):
    """Test that the help command displays usage information."""
    display_help()

    captured = capsys.readouterr()

    assert "Calculator REPL Help" in captured.out
    assert "<operation> <number1> <number2>" in captured.out
    assert "add" in captured.out
    assert "subtract" in captured.out
    assert "multiply" in captured.out
    assert "divide" in captured.out
    assert "power" in captured.out
    assert "modulus" in captured.out
    assert "history" in captured.out
    assert "exit" in captured.out


def test_display_history_empty(capsys):
    """Test displaying an empty calculation history."""
    display_history([])

    captured = capsys.readouterr()

    assert captured.out.strip() == "No calculations performed yet."


def test_display_history_with_entries(capsys):
    """Test displaying a populated calculation history."""
    history = [
        "AddCalculation: 10.0 Add 5.0 = 15.0",
        "SubtractCalculation: 20.0 Subtract 3.0 = 17.0",
    ]

    display_history(history)

    captured = capsys.readouterr()

    assert "Calculation History:" in captured.out
    assert "1. AddCalculation: 10.0 Add 5.0 = 15.0" in captured.out
    assert "2. SubtractCalculation: 20.0 Subtract 3.0 = 17.0" in captured.out


def test_calculator_exit(monkeypatch, capsys):
    """Test that the exit command terminates the calculator."""
    exc_info = run_calculator(monkeypatch, "exit\n")

    captured = capsys.readouterr()

    assert "Exiting calculator. Goodbye!" in captured.out
    assert exc_info.value.code == 0


def test_calculator_help(monkeypatch, capsys):
    """Test the help command from the REPL."""
    run_calculator(monkeypatch, "help\nexit\n")

    captured = capsys.readouterr()

    assert "Calculator REPL Help" in captured.out
    assert "Exiting calculator. Goodbye!" in captured.out


@pytest.mark.parametrize(
    "user_input, expected_output",
    [
        (
            "add 10 5\nexit\n",
            "Result: AddCalculation: 10.0 Add 5.0 = 15.0",
        ),
        (
            "subtract 20 5\nexit\n",
            "Result: SubtractCalculation: 20.0 Subtract 5.0 = 15.0",
        ),
        (
            "multiply 7 8\nexit\n",
            "Result: MultiplyCalculation: 7.0 Multiply 8.0 = 56.0",
        ),
        (
            "divide 20 4\nexit\n",
            "Result: DivideCalculation: 20.0 Divide 4.0 = 5.0",
        ),
                (
            "power 2 3\nexit\n",
            "Result: PowerCalculation: 2.0 Power 3.0 = 8.0",
        ),
        (
            "modulus 10 3\nexit\n",
            "Result: ModulusCalculation: 10.0 Modulus 3.0 = 1.0",
        ),
    ],
)
def test_calculator_operations(
    monkeypatch,
    capsys,
    user_input,
    expected_output,
):
    """Test supported arithmetic operations through the REPL."""
    run_calculator(monkeypatch, user_input)

    captured = capsys.readouterr()

    assert expected_output in captured.out


@pytest.mark.parametrize(
    "user_input",
    [
        "invalid input\nexit\n",
        "add 5\nexit\n",
        "subtract\nexit\n",
        "add 1 2 3\nexit\n",
        "add ten five\nexit\n",
    ],
)
def test_calculator_invalid_input(monkeypatch, capsys, user_input):
    """Test invalid input formats and non-numeric operands."""
    run_calculator(monkeypatch, user_input)

    captured = capsys.readouterr()

    assert (
        "Invalid input. Please follow the format: "
        "<operation> <num1> <num2>"
    ) in captured.out

    assert "Type 'help' for more information." in captured.out


def test_calculator_unsupported_operation(monkeypatch, capsys):
    """Test an unsupported arithmetic operation."""
    run_calculator(monkeypatch, "unknown 2 3\nexit\n")

    captured = capsys.readouterr()

    assert "Unsupported calculation type: 'unknown'." in captured.out
    assert (
        "Type 'help' to see the list of supported operations."
        in captured.out
    )


@pytest.mark.parametrize(
    "command, expected_error",
    [
        ("divide 10 0", "Cannot divide by zero."),
        ("modulus 10 0", "Cannot perform modulus by zero."),
        ("power 0 -1", "negative power"),
    ],
)
def test_calculator_zero_errors(
    monkeypatch, capsys, command, expected_error
):
    """Report arithmetic errors and continue accepting commands."""
    user_input = (
        f"{command}\n"
        "add 2 3\n"
        "history\n"
        "exit\n"
    )

    run_calculator(monkeypatch, user_input)
    captured = capsys.readouterr()

    assert expected_error in captured.out
    assert "Please check your operands and try again." in captured.out
    assert "Result: AddCalculation: 2.0 Add 3.0 = 5.0" in captured.out
    assert "1. AddCalculation: 2.0 Add 3.0 = 5.0" in captured.out
    assert "2. " not in captured.out

def test_calculator_empty_history(monkeypatch, capsys):
    """Test the history command before calculations are performed."""
    run_calculator(monkeypatch, "history\nexit\n")

    captured = capsys.readouterr()

    assert "No calculations performed yet." in captured.out


def test_calculator_keyboard_interrupt(monkeypatch, capsys):
    """Test graceful handling of Ctrl+C."""
    def mock_input(_prompt):
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", mock_input)

    with pytest.raises(SystemExit) as exc_info:
        calculator()

    captured = capsys.readouterr()

    assert "Keyboard interrupt detected" in captured.out
    assert exc_info.value.code == 0


def test_calculator_eof_error(monkeypatch, capsys):
    """Test graceful handling of EOF."""
    def mock_input(_prompt):
        raise EOFError

    monkeypatch.setattr("builtins.input", mock_input)

    with pytest.raises(SystemExit) as exc_info:
        calculator()

    captured = capsys.readouterr()

    assert "EOF detected" in captured.out
    assert exc_info.value.code == 0


def test_calculator_unexpected_exception(monkeypatch, capsys):
    """Test handling of an unexpected calculation error."""
    class MockCalculation:
        def execute(self):
            raise RuntimeError("Mock exception during execution")

    def mock_create_calculation(_operation, _a, _b):
        return MockCalculation()

    monkeypatch.setattr(
        "app.calculator.CalculationFactory.create_calculation",
        mock_create_calculation,
    )

    run_calculator(monkeypatch, "add 10 5\nexit\n")

    captured = capsys.readouterr()

    assert (
        "An error occurred during calculation: "
        "Mock exception during execution"
    ) in captured.out

    assert "Please try again." in captured.out
