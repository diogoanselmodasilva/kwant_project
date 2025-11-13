import kwant
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.linalg import eigsh

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
syst = syst.finalized()

hamiltonian = syst.hamiltonian_submatrix(sparse=True)

# --- Cálculo dos autovalores ---
num_levels = 20
energies, _ = eigsh(hamiltonian, k=num_levels, which='SM')
energies = np.sort(energies)

# Calculo de densidade de estados (DOS)
num_bins = 40
dos_counts, energy_bins = np.histogram(energies, bins=num_bins, density=True)
energy_centers = 0.5 * (energy_bins[:-1] + energy_bins[1:])


kwant.plot(syst, show = False)
plt.figure(2)
plt.plot(range(1, num_levels + 1), energies, 'bo')
plt.xlabel('Índice do nível')
plt.ylabel('Energia')
plt.title('Espectro de energia')
plt.grid(True)
plt.figure(3)
plt.plot(energy_centers, dos_counts, 'r-', lw=2)
plt.xlabel('Energia E')
plt.ylabel('Densidade de estados ρ(E)')
plt.title('Densidade de estados (DOS)')
plt.grid(True)
plt.tight_layout()
plt.show()


kwant.plot(syst)