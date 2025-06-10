import kwant
import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
t = 1.0  # Energia de hopping
a = 1    # Parâmetro de rede
L, W = 10, 10  # Dimensões do sistema

# Vetores de base para rede triangular
a1 = (a, 0)
a2 = (a * 0.5, a * np.sqrt(3)/2)

# Criar rede triangular com uma sub-rede
lat = kwant.lattice.general([a1, a2], [(0, 0)])
sublattice = lat.sublattices[0] 

# Sistema principal
syst = kwant.Builder()

def regiao(pos):
    x, y = pos
    return 0 <= x < L and 0 <= y < W * np.sqrt(3)/2

syst[lat.shape(regiao, (0, 0))] = 4 * t
syst[lat.neighbors()] = -t

# Lead esquerda
sym_left = kwant.TranslationalSymmetry((-a, 0))
left_lead = kwant.Builder(sym_left)
left_lead[(sublattice(0, j) for j in range(W))] = 4 * t
left_lead[lat.neighbors()] = -t

# Lead direita 
sym_right = kwant.TranslationalSymmetry((a, 0))
right_lead = kwant.Builder(sym_right)
right_lead[(sublattice(0, j) for j in range(W))] = 4 * t  
right_lead[lat.neighbors()] = -t

# Conectar leads
syst.attach_lead(left_lead)
syst.attach_lead(right_lead)

# Finalizar sistema
syst = syst.finalized()

# Cálculo de transporte
energies = np.linspace(0, 2, 100)
conductances = [kwant.smatrix(syst, energy).transmission(1, 0) 
               for energy in energies]

# Plot dos resultados
kwant.plot(syst, show = False)
plt.figure(2)
plt.plot(energies, conductances)
plt.xlabel("Energia [t]")
plt.ylabel("Condutância [e²/h]")
plt.title("Condutância vs Energia")
plt.show()