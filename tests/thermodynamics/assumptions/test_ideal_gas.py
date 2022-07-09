from solver import expression_solver

from thermodynamics.assumptions import ideal_gas, assumptions


@ideal_gas.IdealGas()
class FakeDevice(assumptions.AbstractDevice):
    def __init__(self, list):
        self._list = list

    def __call__(self):
        return self._list


@ideal_gas.IdealGas()
@ideal_gas.IdealGas(pressure="P1")
class StackDevice(assumptions.AbstractDevice):
    def __init__(self, list):
        self._list = list

    def __call__(self):
        return self._list


class TestAssumptions:
    def test_class_construction(self):
        device = FakeDevice([expression_solver.EquationFormat("123", "456")])
        expected = [
            expression_solver.EquationFormat("123", "456"),
            expression_solver.EquationFormat("P*V", "n*8.3145*T"),
        ]
        observed = device()
        assert expected == observed

    def test_stack_decorator(self):
        device = StackDevice([])
        expected = [
            expression_solver.EquationFormat("P1*V", "n*8.3145*T"),
            expression_solver.EquationFormat("P*V", "n*8.3145*T"),
        ]
        observed = device()
        assert expected == observed
