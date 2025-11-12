import kwant
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.linalg import eigsh

# --- Definir geometria ---
def circle(pos):
    x, y = pos
    return x**2 + y**2 < 50**2  

# --- Construir sistema ---
lat = kwant.lattice.square(a=1)
sys = kwant.Builder()
sys[lat.shape(circle, (0, 0))] = 4.0
sys[lat.neighbors()] = -1.0
finalized_sys = sys.finalized()

# --- Hamiltoniana esparsa ---
hamiltonian = finalized_sys.hamiltonian_submatrix(sparse=True)

# --- Cálculo eficiente dos autovalores ---
num_levels = 20
energies, _ = eigsh(hamiltonian, k=num_levels, which='SM')
energies = np.sort(energies)

# --- Plotar espectro ---
kwant.plot(finalized_sys, show = False)
plt.figure(2)
plt.plot(range(1, num_levels + 1), energies, 'bo')
plt.xlabel('Índice do nível')
plt.ylabel('Energia')
plt.title('Espectro de energia')
plt.grid(True)
plt.show()
