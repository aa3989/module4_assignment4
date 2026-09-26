
"""
Unit tests for the calculation module.

Tests cover calculation execution, the CalculationFactory,
string representations, error handling, and registration.
"""

import pytest

from app.calculation import (
    Calculation,
    CalculationFactory,
    AddCalculation,
    SubtractCalculation,
    MultiplyCalculation,
    DivideCalculation,
    PowerCalculation,
    ModulusCalculation,

)


@pytest.mark.parametrize(
    "calculation_class, a, b, expected",
    [
        (AddCalculation, 10.0, 5.0, 15.0),
        (AddCalculation, -10.0, 5.0, -5.0),
        (SubtractCalculation, 10.0, 5.0, 5.0),
        (SubtractCalculation, -10.0, 5.0, -15.0),
        (MultiplyCalculation, 10.0, 5.0, 50.0),
        (MultiplyCalculation, -10.0, 5.0, -50.0),
        (DivideCalculation, 10.0, 5.0, 2.0),
        (DivideCalculation, -10.0, 5.0, -2.0),
    ],
)
def test_calculation_execute(calculation_class, a, b, expected):
    """Test execute() for all calculation classes."""
    calculation = calculation_class(a, b)

    assert calculation.execute() == expected


@pytest.mark.parametrize(
    "operation, expected_class",
    [
        ("add", AddCalculation),
        ("subtract", SubtractCalculation),
        ("multiply", MultiplyCalculation),
        ("divide", DivideCalculation),
        ("power", PowerCalculation),
        ("modulus", ModulusCalculation),
    ],
)
def test_factory_creates_correct_calculation(operation, expected_class):
    """Test that the factory creates the correct calculation class."""
    a = 10.0
    b = 5.0

    calculation = CalculationFactory.create_calculation(
        operation,
        a,
        b,
    )

    assert isinstance(calculation, expected_class)
    assert calculation.a == a
    assert calculation.b == b


def test_factory_unsupported_operation():
    """Test that an unsupported operation raises ValueError."""
    with pytest.raises(
        ValueError,
        match="Unsupported calculation type: 'unknown'",
    ):
        CalculationFactory.create_calculation(
            "unknown",
            10.0,
            5.0,
        )


def test_factory_duplicate_registration():
    """Test that duplicate operation registration raises ValueError."""
    with pytest.raises(
        ValueError,
        match="Calculation type 'add' is already registered.",
    ):

        @CalculationFactory.register_calculation("add")
        class DuplicateAddCalculation(Calculation):
            """Duplicate class used only for testing."""

            def execute(self) -> float:
                return self.a + self.b


def test_divide_calculation_by_zero():
    """Test division by zero at the calculation level."""
    calculation = DivideCalculation(10.0, 0.0)

    with pytest.raises(
        ZeroDivisionError,
        match="Cannot divide by zero.",
    ):
        calculation.execute()


@pytest.mark.parametrize(
    "calculation_class, a, b, expected",
    [
        (
            AddCalculation,
            10.0,
            5.0,
            "AddCalculation: 10.0 Add 5.0 = 15.0",
        ),
        (
            SubtractCalculation,
            10.0,
            5.0,
            "SubtractCalculation: 10.0 Subtract 5.0 = 5.0",
        ),
        (
            MultiplyCalculation,
            10.0,
            5.0,
            "MultiplyCalculation: 10.0 Multiply 5.0 = 50.0",
        ),
        (
            DivideCalculation,
            10.0,
            5.0,
            "DivideCalculation: 10.0 Divide 5.0 = 2.0",
        ),
    ],
)
def test_calculation_string(calculation_class, a, b, expected):
    """Test string representations for calculation classes."""
    calculation = calculation_class(a, b)

    assert str(calculation) == expected


@pytest.mark.parametrize(
    "calculation_class",
    [
        AddCalculation,
        SubtractCalculation,
        MultiplyCalculation,
        DivideCalculation,
    ],
)
def test_calculation_repr(calculation_class):
    """Test repr() for all calculation classes."""
    calculation = calculation_class(10.0, 5.0)

    expected = (
        f"{calculation_class.__name__}"
        "(a=10.0, b=5.0)"
    )

    assert repr(calculation) == expected


@pytest.mark.parametrize(
    "calculation_class, a, b, expected",
    [
        (PowerCalculation, 2.0, 3.0, 8.0),
        (PowerCalculation, 10.0, 0.0, 1.0),
        (PowerCalculation, 2.0, -2.0, 0.25),
        (ModulusCalculation, 10.0, 3.0, 1.0),
        (ModulusCalculation, 10.0, 5.0, 0.0),
        (ModulusCalculation, -10.0, 3.0, 2.0),
    ],
)
def test_power_and_modulus_calculations(
    calculation_class, a, b, expected
):
    """Test the new calculation classes."""
    calculation = calculation_class(a, b)

    assert calculation.execute() == pytest.approx(expected)


def test_modulus_calculation_by_zero():
    """Reject modulus by zero at the calculation layer."""
    calculation = ModulusCalculation(10.0, 0.0)

    with pytest.raises(
        ZeroDivisionError,
        match="Cannot perform modulus by zero",
    ):
        calculation.execute()