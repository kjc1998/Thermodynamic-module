try:
    from .packages import ideal_gas
except ImportError:
    from packages import ideal_gas

if __name__ == "__main__":
    test = ideal_gas.IdealGas(P=1,  m=1, T=1)
