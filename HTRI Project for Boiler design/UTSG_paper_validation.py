# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 12:37:29 2020

@author: Xavier
"""

import iapws.iapws97 as prop
import numpy as np

#%% UTILITY FUNCTIONS

def ABT(T):
    return T + 273.15    #Absolute Temperature Scale Converter
#%% MATERIALS

# TUBE

SS316 = {'C' : 500 , 'k' : 16.3 , 'rho' : 7.99 , 'E': 193000,'Syt' : 290 , 'Cost' : 3.5} # Cost in dollar / kg
MONEL400 = {'C' : 427 , 'k' : 21.8 , 'rho' : 8.83 , 'E': 173000,'Syt' : 276 , 'Cost' : 30}
INCONEL600 = {'C' : 460 , 'k' :14.8 , 'rho' : 8.42 , 'E': 207000,'Syt' : 176 , 'Cost' : 18}
INCOLOY800 = {'C' : 460 , 'k' : 11.5 , 'rho' : 7.94 , 'E': 208000,'Syt' : 275 , 'Cost' : 35}
TUBE_mat = [SS316,MONEL400,INCONEL600,INCOLOY800]
#%% INITIAL CONDITIONS

Cir_rate = 3.7  #Circulation rate : mf tubeside / mf steam

Thi = 598#ABT(337)  #Inlet Temperature of Reactor Coolant
Tho = 559#ABT(300)  #Outlet Temperature of Reactor Coolant
xh = 0          #Steam Quality of Reactor Coolant
Phi = 15.5 #MPA   #Inlet Pressure of Reactor Coolant
Tci = 492#ABT(200)  #Inlet Temperature of Secondary Circuit Coolant
Tco = 552#ABT(285)  #Outlet Temperature of Secondary Circuit Coolant
xci = 0         #Inlet Steam Quality of Secondary Circuit Coolant
xco = 1 / Cir_rate         #Outlet Steam Quality of Secondary Circuit Coolant
Pci = 6.3 #MPA    #Inlet Pressure of Secondary Circuit Coolant
Power = 1000*(10**3)     #Power to be generated (kW)

#%% OBJECTS OF WATER AND STEAM AT DIFFERENT INLET/OUTLET CONDITIONS
Ci = prop.IAPWS97(P= Pci, T= Tci)       #Single-phase
Co = prop.IAPWS97(T = Tco , x = xco)    #Two-phase
Hi = prop.IAPWS97(P= Phi, T= Thi)
Ho = prop.IAPWS97(P= Phi, T= Tho)

#%% MASS FLOW RATE CALCULATION FROM Q' = m'x del_h
print((Co.Vapor.h-Co.Liquid.h))
mf_steam = Power / (Co.Vapor.h-Ci.Liquid.h)
mf_shellside = mf_steam * Cir_rate
mf_tubeside = Power / (Hi.Liquid.h - Ho.Liquid.h)

print("Tubeside mass flow rate = " + str(mf_tubeside) + " kg/s")
print("Shellside mass flow rate = " + str(mf_shellside) + " kg/s")
print("Steam mass flow rate = " + str(mf_steam) + " kg/s")
#%% LOG MEAN TEMPERATURE DIFFERENCE (COUNTER FLOW CONSIDERED)
if (Tho - Tci) != (Thi - Tco):
    LMTD = ((Thi - Tco) - (Tho - Tci)) / np.log((Thi - Tco)/(Tho - Tci)) 
else:
    LMTD = (Tho - Tci)

print("Log mean Temperature difference: " + str(LMTD) + ' deg C')

#%% UA FROM Q' = UA x LMTD
UA = (Power / LMTD) * (10**3)
print("UA = " + str(UA) + ' W/K')

