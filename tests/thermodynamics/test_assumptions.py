import pytest
from unittest import mock
from solver import expression_solver
from thermodynamics import assumptions


@pytest.fixture
def func_mock():
    result = mock.MagicMock(
        return_value=[expression_solver.EquationFormat("123", "456")]
    )
    return result


class TestAssumptions:
    def test_decorator(self):
        """
        Works for both:

        1)  @ideal_gas
            def ...

        2)  @ideal_gas()
            def ...
        """

        def fake_func():
            return []

        expected = [expression_solver.EquationFormat("P*V", "n*8.3145*T")]
        o1 = assumptions.Assumptions.ideal_gas(fake_func)()
        o2 = assumptions.Assumptions.ideal_gas()(fake_func)()
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
        observed = assumptions.Assumptions.ideal_gas(pressure="P1")(func_mock)()
        assert expected == observed
