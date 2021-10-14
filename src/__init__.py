from .packages import ideal_gas

if __name__ == "__main__":
    test = ideal_gas.IdealGas(P=1.0002, V=8.3125, m=1, T=1)
    print(test.density)
