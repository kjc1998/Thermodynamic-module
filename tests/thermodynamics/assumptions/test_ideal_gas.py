from unittest import mock

import pytest
from solver import expression_solver

from thermodynamics.assumptions import ideal_gas


@pytest.fixture
def func_mock():
    result = mock.MagicMock(
        return_value=[expression_solver.EquationFormat("123", "456")]
    )
    return result


class TestAssumptions:
    def test_decorator(self):
        @ideal_gas.IdealGas
        def fake_func():
            return []

        @ideal_gas.IdealGas()
        def fake_func_two():
            return []

        expected = [expression_solver.EquationFormat("P*V", "n*8.3145*T")]
        o1 = fake_func()
        o2 = fake_func_two()
        assert expected == o1 == o2

    def test_ideal_gas(self, func_mock):
        """
        @ideal_gas(pressure=..., temp...)
        def func(...):
            ...
        """
        expected = func_mock() + [
            expression_solver.EquationFormat("P1*V", "n*8.3145*T")
        ]
        observed = ideal_gas.IdealGas(pressure="P1")(func_mock)()
        assert expected == observed
