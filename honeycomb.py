import kwant
import numpy as np
import matplotlib.pyplot as plt

# parametros
a = 1
W, L = 30, 60
t = 1

kwant.lattice.honeycomb()
syst = kwant.Builder()

def rectangle(pos):
    x, y = pos 
    return 0 <= 