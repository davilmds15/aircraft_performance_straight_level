from dinamica_translacao import dinamica_translacao
from controles import controles_planeio
from controles import controles_reto_niv
import numpy as np


def simula_planeio(t,X):
    CL,F,phi,Y = controles_planeio()
    U = np.array([CL,F,phi,Y])
    Xp = dinamica_translacao(t,X,U)
    return Xp
# Função para simulação do voo reto e nivelado
def simula_reto_niv(t,X):
    # Entradas: t e X
    CL,F,phi,Y = controles_reto_niv()
    U = np.array([CL,F,phi,Y])
    Xp = dinamica_translacao(t,X,U)
    return Xp
