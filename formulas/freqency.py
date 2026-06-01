import numpy as np

def capacitor_impedance(frequency: float, capacitance: float) -> complex:
    omega = 2 * np.pi * frequency
    return 1 / (1j * omega * capacitance)

def pole_frequency(resistance: float, capacitance: float) -> float:
    return 1 / (2 * np.pi * resistance * capacitance)



