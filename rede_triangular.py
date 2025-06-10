import kwant
#import kwant.lattice
import numpy as np
import matplotlib.pyplot as plt

# vetores de base triangular
a1 = (1,0)
a2 = (0.5,np.sqrt(3)/2) # 60 graus entre a1 e a2

# criar a rede triangular
lat = kwant.lattice.general([a1,a2], [(0,0)])

syst = kwant.Builder()
# define uma forma retangular para a região
def forma(pos):
    x,y = pos
    return 0 <= x <= 10 and 0 <= y <= 10

# adiciona sitios da rede triangular dentro da forma
syst[lat.shape(forma, (0,0))] = 0.0 

# adiciona hoppings entre vizinhos mais proximos
syst[lat.neighbors()] = -1

kwant.plot(syst)
