from solver import expression_solver

from thermodynamics.assumptions import ideal_gas


class TestAssumptions:
    def test_ideal_gas(self):
        @ideal_gas.IdealGas
        def fake_func():
            return []

        @ideal_gas.IdealGas()
        def fake_func_two():
            return []

        @ideal_gas.IdealGas
        @ideal_gas.IdealGas()
        def fake_func_three():
            return []

        expected = [expression_solver.EquationFormat("P*V", "n*8.3145*T")]
        o1 = fake_func()
        o2 = fake_func_two()
        o3 = fake_func_three()
        assert expected == o1 == o2
        assert expected + expected == o3
