import kwant
import numpy as np
import matplotlib.pyplot as plt

# parametros
t = 1.0
a = 1  
w, L = 30, 60
xc, yc = 30,15
r = 5

# função do furo
def shape_with_hole(pos):
    x, y = pos
    inside_rectangle = (0 <= x <= L) and (0 <= y <= w)
    outside_rectangle = (x-xc)**2 + (y-yc)**2 >= r**2

    return inside_rectangle and outside_rectangle

# criar uma rede quadrada com um furo
lat = kwant.lattice.square(a)
syst = kwant.Builder()

syst[lat.shape(shape_with_hole, (0,0))] = 4 * t
syst[lat.neighbors()] = -t

# Lead da esquerda
sym_left_lead = kwant.TranslationalSymmetry((-a, 0))
left_lead = kwant.Builder(sym_left_lead)
for y in range(w):
    left_lead[lat(0, y)] = 4 * t
    if y > 0:
        left_lead[lat(0, y), lat(0, y - 1)] = -t
    left_lead[lat(1, y), lat(0, y)] = -t

syst.attach_lead(left_lead)

# Lead da direita
sym_right_lead = kwant.TranslationalSymmetry((a, 0))
right_lead = kwant.Builder(sym_right_lead)
for y in range(w):
    right_lead[lat(0, y)] = 4 * t
    if y > 0:
        right_lead[lat(0, y), lat(0, y - 1)] = -t
    right_lead[lat(1, y), lat(0, y)] = -t


syst.attach_lead(right_lead)
# Finalize the system
syst = syst.finalized()

#calculo da conduntancia
energies = []
data = []
for ie in range(100):
    energy = ie * 0.01
    smatrix = kwant.smatrix(syst, energy = energy)
    energies.append(energy)
    data.append(smatrix.transmission(1, 0))

# plotar o grafico
kwant.plot(syst, show=False)
plt.figure(2)
plt.plot(energies, data)
plt.xlabel("energy [t]")
plt.ylabel("conductance [e^2/h]")
plt.title("Condutância x Energia")
plt.show()

kwant.plot(syst)