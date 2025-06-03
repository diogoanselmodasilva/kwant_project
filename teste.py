import kwant
import matplotlib.pyplot as plt

lat = kwant.lattice.square()
sys = kwant.Builder()

for x in range(5):
    for y in range(5):
        sys[lat(x, y)] = 4
        if x > 0:
            sys[lat(x, y), lat(x - 1, y)] = -1
        if y > 0:
            sys[lat(x, y), lat(x, y - 1)] = -1

kwant.plot(sys)
