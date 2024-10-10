import parametros
from modelo_ambiental import ISA
import numpy as np
from dinamica_translacao import dinamica_translacao
from scipy.optimize import fsolve
from controles import controles_planeio
from controles import controles_reto_niv
from aerodinamica import modelo_aerodinamico_reto_niv
from aerodinamica import modelo_aerodinamico_planeio


def obj_eq_planeio(x,*dados):
    # x: vetor contendo as incógnitas
    He, alfaf, m, g=dados
    Ve = x[0]; gamae = x[1]
    CLe,Fe,phie,Y = controles_planeio()
    _,_,rhoe,_,_,_ = ISA(He,0)
    Le,De,alfe,Y = modelo_aerodinamico_planeio(CLe, Ve, rhoe)
    Xe = np.array([Ve,gamae,0,0,0,He])
    U  = np.array([CLe,Fe,phie,Y])
    Xp = dinamica_translacao(0,Xe,U)
    der = np.array([Xp[0],Xp[1]])
    return der

def equilibrio_planeio(H):
    m = parametros.M; g = parametros.G; CD0 = parametros.CD0; alfaf = parametros.ALFAF
    k = parametros.K; S = parametros.S; He = parametros.H0
    dados = (He, alfaf, m, g)
    _,_,rho,_,_,_ = ISA(He,0)
    CLas = np.sqrt(CD0/k) # CL*
    Vas = np.sqrt(2*m*g/(rho*S*CLas))
    x0 = np.array([Vas,0])
    res = fsolve(obj_eq_planeio,x0,args=dados)
    Xe = np.array([res[0],res[1],0,0,0,H])
    return Xe

def obj_eq_reto_niv(x,*dados):
    # x: vetor contendo as incógnitas
    # X(1) = CL: CL coeficiente de sustentação
    # X(2) = F: Força Propulsiva
    He,Ve,alfaf, m, g=dados
    CLe = x[0]; Fe = x[1]
    # Controles planeio
    phie = 0; Ye = 0
    _,_,rhoe,_,_,_ = ISA(He,0)
    Le,De,alfe,Ye = modelo_aerodinamico_reto_niv(CLe, Ve, rhoe)
    Xe = np.array([Ve,0,0,0,0,He])
    Ue = np.array([CLe,Fe,phie,Ye])
    Xp = dinamica_translacao(0,Xe,Ue)
    der = np.array([Xp[0],Xp[1]])
    return der

def equilibrio_reto_niv(V,H):
    # Calcula o ponto de equilíbrio do voo reto e nivelado com velocidade V e altitude H
    # Entradas V H 
    # Saídas 
    # Xe [Ve gamae psie x0e y0e he] Vetor de estado no equilíbrio
    # Ue [CLe Fe phie Ye] Vetor de controle no equilíbrio
    m = parametros.M; g = parametros.G; CD0 = parametros.CD0; alfaf = parametros.ALFAF
    k = parametros.K; S = parametros.S; He = parametros.H0
    dados = (H,V,alfaf, m, g)
    # Chutes iniciais
    CL = np.sqrt(CD0/k) # CL*
    F = 0.1*m*g
    x0 = np.array([CL,F])
    res = fsolve(obj_eq_reto_niv,x0,args=dados)
    Xe=np.array([V,0,0,0,0,H])
    Ue=np.array([res[0],res[1],0,0])
    return Xe,Ue
