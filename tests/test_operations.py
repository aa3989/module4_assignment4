
"""
Unit tests for the Operation class.

The tests use pytest parameterization to verify arithmetic operations
with positive numbers, negative numbers, zero, and invalid inputs.
"""

import pytest

from app.operation import Operation


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10.0, 5.0, 15.0),
        (-10.0, -5.0, -15.0),
        (10.0, -5.0, 5.0),
        (10.0, 0.0, 10.0),
        (0.0, 0.0, 0.0),
    ],
)
def test_addition(a, b, expected):
    """Test addition with multiple input combinations."""
    assert Operation.addition(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10.0, 5.0, 5.0),
        (-10.0, -5.0, -5.0),
        (10.0, -5.0, 15.0),
        (10.0, 0.0, 10.0),
        (0.0, 5.0, -5.0),
    ],
)
def test_subtraction(a, b, expected):
    """Test subtraction with multiple input combinations."""
    assert Operation.subtraction(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10.0, 5.0, 50.0),
        (-10.0, -5.0, 50.0),
        (10.0, -5.0, -50.0),
        (10.0, 0.0, 0.0),
        (0.0, 5.0, 0.0),
    ],
)
def test_multiplication(a, b, expected):
    """Test multiplication with multiple input combinations."""
    assert Operation.multiplication(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10.0, 5.0, 2.0),
        (-10.0, -5.0, 2.0),
        (10.0, -5.0, -2.0),
        (0.0, 5.0, 0.0),
        (5.0, 2.0, 2.5),
    ],
)
def test_division(a, b, expected):
    """Test division with multiple valid input combinations."""
    assert Operation.division(a, b) == expected


def test_division_by_zero():
    """Test that division by zero raises the expected exception."""
    with pytest.raises(
        ValueError,
        match="Division by zero is not allowed.",
    ):
        Operation.division(10.0, 0.0)


@pytest.mark.parametrize(
    "operation, a, b",
    [
        (Operation.addition, "10", 5.0),
        (Operation.subtraction, 10.0, "5"),
        (Operation.multiplication, "10", "5"),
        (Operation.division, 10.0, "5"),
    ],
)
def test_invalid_input_types(operation, a, b):
    """Test that invalid operand types raise TypeError."""
    with pytest.raises(TypeError):
        operation(a, b)

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2.0, 3.0, 8.0),
        (10.0, 0.0, 1.0),
        (2.0, -2.0, 0.25),
        (-2.0, 3.0, -8.0),
    ],
)
def test_power(a, b, expected):
    """Test power with positive, zero, and negative exponents."""
    assert Operation.power(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10.0, 3.0, 1.0),
        (10.0, 5.0, 0.0),
        (-10.0, 3.0, 2.0),
        (10.0, -3.0, -2.0),
    ],
)
def test_modulus(a, b, expected):
    """Test remainders with positive and negative operands."""
    assert Operation.modulus(a, b) == pytest.approx(expected)


def test_operation_modulus_zero_divisor():
    """Test the zero-divisor check in Operation.modulus."""
    with pytest.raises(
        ValueError,
        match="Modulus by zero is not allowed",
    ):
        Operation.modulus(10.0, 0.0)
