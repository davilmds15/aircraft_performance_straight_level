import parametros
from modelo_ambiental import ISA
import numpy as np
from aerodinamica import modelo_aerodinamico_planeio


def dinamica_translacao(t,X,U):
    m = parametros.M;
    g = parametros.G;
    alfaf = parametros.ALFAF;
    V = X[0];
    gama = X[1];
    psi = X[2];
    H = X[5];
    CL = U[0];
    F = U[1];
    phi = U[2];
    Y = U[3];
    
    _,_,rho,_,_,_ = ISA(H,0)
    
    L,D,alfa,Y=modelo_aerodinamico_planeio(CL,V,rho)
    
    Vp = (F*np.cos(alfa+alfaf)-D-m*g*np.sin(gama))/m
    gamap = ((F*np.sin(alfa+alfaf)+L)*np.cos(phi)-m*g*np.cos(gama)+Y*np.sin(phi))/(m*V)
    psip = ((F*np.sin(alfa+alfaf)+L)*np.sin(phi)-Y*np.cos(phi))/(m*V*np.cos(gama))
    
    xp = V*np.cos(gama)*np.cos(psi)
    yp = V*np.cos(gama)*np.sin(psi)
    Hp = V*np.sin(gama)
    
    Xp = np.array([Vp, gamap, psip, xp, yp, Hp])
    
    return Xp