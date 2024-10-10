import parametros

def modelo_aerodinamico_planeio(CL,V,rho):
    CD0 = parametros.CD0; k = parametros.K; S = parametros.S;
    CL0=parametros.CL0;CLa=parametros.CLA
    CD = CD0 + k*CL**2;
    D = 0.5*rho*V**2*S*CD
    L = 0.5*rho*V**2*S*CL
    alfa = (CL-CL0)/CLa;
    Y = 0;
    return L,D,alfa,Y

# Função para calcular o modelo aerodinâmico em voo reto e nivelado
def modelo_aerodinamico_reto_niv(CL,V,rho):
    # Função para calcular as forças aerodinâmicas 
    CD0=parametros.CD0;k=parametros.K;S=parametros.S;
    CL0=parametros.CL0;CLa=parametros.CLA
    CD = CD0+k*CL**2;
    D = 0.5*rho*V**2*S*CD
    L = 0.5*rho*V**2*S*CL
    alfa = (CL-CL0)/CLa;
    Y = 0;
    return L,D,alfa,Y
    