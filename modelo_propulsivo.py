# -*- coding: utf-8 -*-
"""
Created on Sun May 14 01:10:40 2023

@author: mj_sc
"""

import parametros
from modelo_ambiental import ISA

def posicao_manete(F,V,H):
    Fi = parametros.FI; nr = parametros.NR
    rhoi = parametros.RHOI; av = parametros.AV
    Pi = parametros.PI; etap = parametros.ETAP; mr = parametros.MR
    
    _,_,rho,_,_,_ = ISA(H,0)
    if av == 1:
        Fd = Fi*(rho/rhoi)**nr
        dp = F/Fd #posicao da manete
        print('Jato')
        print('dp = ', dp)
        print('')
    else: 
        P = F*V # potencia motriz
        Pd = etap*Pi*(rho/rhoi)**mr #potencia motriz disponivel
        dp = P/Pd #posicao da manete
        print('Hélice')
        print('dp = ', dp)
        print('')
    return dp
    