"""Wave and signal primitives."""
import math
from typing import List

def sine_wave(amplitude=1.0, frequency=1.0, phase=0.0, samples=512) -> List[float]:
    return [amplitude*math.sin(2*math.pi*frequency*i/(samples-1)+phase) for i in range(samples)]

def superposition(waves, samples=512) -> List[float]:
    return [sum(a*math.sin(2*math.pi*f*i/(samples-1)+p) for a,f,p in waves) for i in range(samples)]

def damped_wave(amplitude=1.0, frequency=1.0, damping=0.5, samples=512) -> List[float]:
    return [amplitude*math.exp(-damping*t)*math.sin(2*math.pi*frequency*t) for t in [i/(samples-1) for i in range(samples)]]
