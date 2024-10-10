# -*- coding: utf-8 -*-
"""
Created on Sat May 13 22:19:26 2023

@author: mj_sc
"""
import numpy as np
from scipy.integrate import solve_ivp #solução numérica de eq diferenciais
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D #gráficos 3D
import datetime #conversão de min em h:min:s
import sys #funções de sistema
from equilibrio import equilibrio_reto_niv
import parametros
from modelo_ambiental import ISA
from modelos_dinamicos_desempenho import simula_reto_niv
from modelo_propulsivo import posicao_manete

#Inicializacoes

g = 9.80665 # gravidade m/s²

# Tipo de avião
av = int(input("Digite a opção de avião: (1) Avião a Jato ou (2) Avião a hélice"))
if av == 1:
    CD0 = 0.015
    k = 0.05
    CL0 = 0;CLa = 5
    CLmax = 2.8
    S = 290*0.092903
    m = 73000*0.453592 #m²
    alfaf = 2*np.pi/180 #rad
    Fi = 12500*4.448222 # força propulsiva, N
    rhoi = 1.225 # kg/m³
    nr = 0.6
else:
    CD0 = 0.026;
    k = 0.054;
    CL0 = 0;CLa = 5
    CLmax = 2.4;
    S = 175*0.092903; #m²
    m = 2900*0.453592; #kg
    alfaf = 2*np.pi/180; #rad
    etap = 0.8; #rendimento da hélice
    Pi = 290*745.6999; # Potencia de eixo máxima a nível do mar, HP to W
    rhoi = 1.225; # kg/m³
    mr = 0.6;
    
    
print('Dados da Aeronave:');
print('CD0: ', CD0)
print('k: ', k)
print('m (kg): ', m)
print('S (m²): ', S)

#Entradas - Condicoes de contorno
Ve = float(input('Digite a velocidade (m/s): '))
He = float(input('Digite a altitude (m): '))

#Carrega os parâmetros do exemplo no módulo de variáveis globais
parametros.G = g
parametros.CD0 = CD0
parametros.K = k
parametros.M = m
parametros.S = S
parametros.ALFAF = alfaf
parametros.CLA = CLa
parametros.CL0 = CL0
parametros.RHOI = rhoi
parametros.AV = av

if av == 1:
    parametros.FI = Fi
    parametros.NR = nr
else:
    parametros.PI = Pi
    parametros.MR = mr
    parametros.ETAP = etap

# Tempo final da simulação
TF = float(input('Digite a duração da simulação (s): '))

Xe,Ue = equilibrio_reto_niv(Ve, He);
CLe = Ue[0] ; Fe = Ue[1]
print('')
print('Estado no equilíbrio:')
print('')
print('V = ', Xe[0], ' m/s')
print('gama = ', Xe[1]*180/np.pi, '°')
print('psi = ', Xe[2]*180/np.pi, '°')
print('x0 = ', Xe[3], 'm')
print('y0 = ', Xe[4], 'm')
print('H = ', Xe[5], 'm')
print('')
print('Controle no equilíbrio:')
print('')
print('CL = ', Ue[0])
print('F = ', Ue[1], 'N')
print('phi = ', Ue[2]*180/np.pi, '°')
print('Y = ', Ue[3], 'N')
print('')

alfa = (CLe - CL0)/CLa #ângulo de ataque
dp = posicao_manete(Fe,Ve,He) #posição da manete
print('Outras variáveis:')
print('')
print('alfa = ', alfa*180/np.pi, '°')
print('dp = ', dp)

#Resultados analíticos
_,_,rho,_,_,_ = ISA(He,0) # calcula densidade do ar
CLT = 2*m*g/(rho*S*Ve**2)
FT = 0.5*rho*S*CD0*Ve**2 + 2*k*(m*g)**2/(rho*S*Ve**2)
print('Valor teorico do CL: ', CLT)
print('Valor teorico da força propulsiva: ', FT, ' N')

#Verifica se a condição de voo é factível - limite propulsivo e estol

if CLe >= CLmax:
    print('Cuidado: o avião está em situação de estol.')
if dp >= 1:
    if av == 1:
            print('Cuidado: a tração requerida é maior que a tração disponível.')
    else: 
        print('Cuidado: a potência requerida é maior que a disponível.')

# Resolução da equação diferencial
parametros.CL = CLe; parametros.F = Fe
sol = solve_ivp(simula_reto_niv, [0, TF], Xe)

t = np.array(sol.t)
V = np.array(sol.y[0]); gama = np.array(sol.y[1]); psi = np.array(sol.y[2])
x0 = np.array(sol.y[3]); y0 = np.array(sol.y[4]); H = np.array(sol.y[5])

# Plots
plt.close("all")
plt.figure(1);

plt.subplot(3,2,1);plt.plot(t,V)
plt.xlabel('t (s)');plt.ylabel('V (m/s)');plt.grid()

plt.subplot(3,2,2);plt.plot(t, gama*180/np.pi)
plt.xlabel('t (s)');plt.ylabel('Gama (graus)');plt.grid()

plt.subplot(3,2,3);plt.plot(t, psi*180/np.pi)
plt.xlabel('t (s)');plt.ylabel('Psi (graus)');plt.grid()

plt.subplot(3,2,4);plt.plot(t, x0/1e3)
plt.xlabel('t (s)');plt.ylabel('x_0 (km)');plt.grid()

plt.subplot(3,2,5);plt.plot(t, y0/1e3)
plt.xlabel('t (s)');plt.ylabel('y_0 (km)');plt.grid()

plt.subplot(3,2,6);plt.plot(t, H)
plt.xlabel('t (s)');plt.ylabel('H (m)');plt.grid()

fig2 = plt.figure(2)

ax = fig2.add_subplot(111, projection = '3d')
ax.plot(x0/1e3, y0/1e3, H)
ax.set_xlabel('x (km)'); ax.set_ylabel('y (km)'); ax.set_zlabel('H (m)')

plt.show()
plt.show(fig2)
