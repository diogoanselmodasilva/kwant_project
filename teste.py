import kwant
import matplotlib.pyplot as plt

# Parâmetros
t = 1.0
a = 1  # distância entre sítios na rede
W, L = 10, 30  # largura e comprimento

# Define a rede quadrada
lat = kwant.lattice.square(a)

# Inicializa o sistema
syst = kwant.Builder()

# Define a região de espalhamento
for i in range(L):
    for j in range(W):
        syst[lat(i, j)] = 4 * t  # potencial on-site

        if i > 0:
            syst[lat(i, j), lat(i - 1, j)] = -t  # hopping em x
        if j > 0:
            syst[lat(i, j), lat(i, j - 1)] = -t  # hopping em y

# Lead da esquerda
sym_left_lead = kwant.TranslationalSymmetry((-a, 0))
left_lead = kwant.Builder(sym_left_lead)

for j in range(W):
    left_lead[lat(0, j)] = 4 * t
    if j > 0:
        left_lead[lat(0, j), lat(0, j - 1)] = -t
    left_lead[lat(1, j), lat(0, j)] = -t

syst.attach_lead(left_lead)

# Lead da direita
sym_right_lead = kwant.TranslationalSymmetry((a, 0))
right_lead = kwant.Builder(sym_right_lead)

for j in range(W):
    right_lead[lat(0, j)] = 4 * t
    if j > 0:
        right_lead[lat(0, j), lat(0, j - 1)] = -t
    right_lead[lat(1, j), lat(0, j)] = -t

syst.attach_lead(right_lead)
# Finalize the system
syst = syst.finalized()

# Now that we have the system, we can compute conductance

energies = []
data = []
for ie in range(100):
    energy = ie * 0.01

    # compute the scattering matrix at a given energy
    smatrix = kwant.smatrix(syst, energy = energy)

    # compute the transmission probability from lead 0 to
    # lead 1
    energies.append(energy)
    data.append(smatrix.transmission(1, 0))

# Use matplotlib to write output
# We should see conductance steps
kwant.plot(syst, show=False)
plt.figure(2)
plt.plot(energies, data)
plt.xlabel("energy [t]")
plt.ylabel("conductance [e^2/h]")
plt.title("Condutância x Energia")
plt.show()