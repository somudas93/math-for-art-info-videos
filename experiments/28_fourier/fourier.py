"""Discrete Fourier primitives without external dependencies."""
import cmath, math
from typing import List, Tuple

def dft(signal:List[float])->List[complex]:
    n=len(signal)
    return [sum(signal[k]*cmath.exp(-2j*math.pi*j*k/n) for k in range(n)) for j in range(n)]

def spectrum(signal:List[float])->List[Tuple[float,float]]:
    values=dft(signal); n=len(signal)
    return [(k/n,abs(v)/n) for k,v in enumerate(values[:n//2+1])]
