import parametros

def controles_planeio():
    F=0; phi=0; Y=0
    CL=parametros.CL
    return CL,F,phi,Y

def controles_reto_niv():
    phi=0;Y=0
    CL = parametros.CL
    F  = parametros.F
    return CL,F,phi,Y
