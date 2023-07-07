# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 12:37:29 2020

@author: Xavier
"""

import iapws.iapws97 as prop
import numpy as np
import pandas as pd

#%% UTILITY FUNCTIONS

def ABT(T):
    return T + 273.15    #Absolute Temperature Scale Converter
#%% MATERIALS

# TUBE

SS316 = {'metal' : "Stainless Steel Alloy 316",'C' : 500 , 'k' : 17.9 , 'rho' : 7990 , 'E': 193000,'Syt' : 290 , 'Cost' : 3.5} # Cost in dollar / kg
MONEL400 = {'metal' : "MONEL Alloy 400",'C' : 427 , 'k' : 21.8 , 'rho' : 8830 , 'E': 173000,'Syt' : 276 , 'Cost' : 30}  # E and Syt in MPa
INCONEL600 = {'metal' : "INCONEL Alloy 600",'C' : 460 , 'k' :14.8 , 'rho' : 8420 , 'E': 207000,'Syt' : 176 , 'Cost' : 24}
INCOLOY800 = {'metal' : "INCONEL Alloy 800" ,'C' : 460 , 'k' : 16.5 , 'rho' : 7940 , 'E': 208000,'Syt' : 275 , 'Cost' : 35}
TUBE_mat = [SS316,MONEL400,INCONEL600,INCOLOY800]

#SHELL
Carbon_steel = {'metal' : "A515 Gr. 70 Carbon Steel", 'rho' : 7800 , 'Syt' : 265 , 'Cost' : 0.8}
#%% INITIAL CONDITIONS (FIXED)

Cir_rate = 3.7  #Circulation rate : mf tubeside / mf steam

Thi = ABT(337)  #Inlet Temperature of Reactor Coolant
Tho = ABT(300)  #Outlet Temperature of Reactor Coolant
xh = 0          #Steam Quality of Reactor Coolant
Phi = 15 #MPA   #Inlet Pressure of Reactor Coolant
Tci = ABT(200)  #Inlet Temperature of Secondary Circuit Coolant
Tco = ABT(285)  #Outlet Temperature of Secondary Circuit Coolant
xci = 0         #Inlet Steam Quality of Secondary Circuit Coolant
xco = 1 / Cir_rate       #Outlet Steam Quality of Secondary Circuit Coolant
Pci = 6.9 #MPA             #Inlet Pressure of Secondary Circuit Coolant
Power = 150*(10**3)        #Power to be generated (kW)

#%% VALIDATION CONDITIONS (FIXED)
# Cir_rate = 3.7  #Circulation rate : mf tubeside / mf steam

# Thi = 598  #Inlet Temperature of Reactor Coolant
# Tho = 559  #Outlet Temperature of Reactor Coolant
# xh = 0          #Steam Quality of Reactor Coolant
# Phi = 15.5 #MPA   #Inlet Pressure of Reactor Coolant
# Tci = 492  #Inlet Temperature of Secondary Circuit Coolant
# Tco = 552 #Outlet Temperature of Secondary Circuit Coolant
# xci = 0         #Inlet Steam Quality of Secondary Circuit Coolant
# xco = 1 / Cir_rate         #Outlet Steam Quality of Secondary Circuit Coolant
# Pci = 6.3 #MPA             #Inlet Pressure of Secondary Circuit Coolant
# Power = 1000*(10**3)        #Power to be generated (kW)

#%% OBJECTS OF WATER AND STEAM AT DIFFERENT INLET/OUTLET CONDITIONS (FIXED)
Ci = prop.IAPWS97(P= Pci, T= Tci)       #Single-phase
Co = prop.IAPWS97(T=Tco , x= xco)       #Two-phase
Hi = prop.IAPWS97(P= Phi, T= Thi)
Ho = prop.IAPWS97(P= Phi, T= Tho)
Cb = prop.IAPWS97(P= Pci, T= (Tci+Tco)/2) #shell bulk
Hb = prop.IAPWS97(P= Phi, T= (Thi+Tho)/2) #tube bulk
#%% MASS FLOW RATE CALCULATION FROM Q' = m'x del_h (FIXED)
print("hco: " , Co.Vapor.h)
print("hci: " , Ci.Liquid.h)
print("hho: " , Hi.Liquid.h)
print("hho: " , Ho.Liquid.h)
mf_steam = Power / (Co.Vapor.h-Ci.Liquid.h)
mf_shellside = mf_steam * Cir_rate
mf_tubeside = Power / (Hi.Liquid.h - Ho.Liquid.h)
#print(Hi.Liquid.h, Ho.Liquid.h)
#print(Co.Vapor.h, Ci.Liquid.h)

print("Tubeside mass flow rate = " + str(mf_tubeside) + " kg/s")
print("Shellside mass flow rate = " + str(mf_shellside) + " kg/s")
print("Steam mass flow rate = " + str(mf_steam) + " kg/s")

#%% LOG MEAN TEMPERATURE DIFFERENCE (COUNTER FLOW CONSIDERED) (FIXED)
if (Tho - Tci) != (Thi - Tco):
    LMTD = ((Thi - Tco) - (Tho - Tci)) / np.log((Thi - Tco)/(Tho - Tci)) 
else:
    LMTD = (Tho - Tci)
print("LMTD : ", LMTD)
#%% Nshell - 2M tube pass : Correction Factor F for Shell and Tube (FIXED) 
P = (Tco - Tci) / (Thi - Tci)
print("P: ", P)
R = (Thi - Tho) / (Tco - Tci)
print("R: ", R)
S = pow(R**2+1,0.5) / (R-1)

W = (1-P*R)/(1-P)
correction_F = S*np.log(W) / np.log((1 +W-S+S*W)/(1 +W+S -S*W))
corrected_LMTD = LMTD * correction_F
print("LMTD correction factor F: ", correction_F)
print("Corrected Log mean Temperature difference: " + str(corrected_LMTD) + ' deg C')

#%% OVERALL HEAT TRANSFER COEFFICIENT CALCULATIONS

UA = (Power / (LMTD * correction_F)) * (10**3)
print("UA: ",UA)
init_rating = Power
print("Rated power to be generated = " + str(Power) + ' kW')

#DATA STORAGE
col = ["No. of tubes", "Shell inner Diameter","Shell Outer Diameter","Area", "Length of Tubes","Velocity in tubes","Tubeside Pdrop","Shellside P drop","Price of tubes", "Price of Shell", "Pumping Operational Cost", "Total Cost", "U" ,"Heat Duty", "OD%"]
data = np.zeros(shape=(int((8000-2500)/50) + 1,len(col))) 
it = 0


max_U = 1910
for var in range(0,1):
    
    U_init = max_U
    print("Assumed U in range 1500 - 6000: ", max_U)
    A_init = UA/U_init
    print("Area from assumed U: ", A_init)
    #KNOWN FOULING FACTORS
    Rfs = 0.00009 #Steam fouling factor
    print("Steam fouling factor: ", Rfs)
    Rfw = 0.00009 #Distilled water fouling factor
    print("Distilled water fouling factor: ", Rfw)
    #TUBE PARAMETERS
    mat = TUBE_mat[0]       #tube material
    print("Material: "+ str(mat['metal']))
    ktube = mat['k']        #tube material conductivity
    yield_st = mat['Syt']   #yield Strength
    print("Syt: ", yield_st)
    sf = 1.6              #Safety Factor
    print("Safety factor considered: ", sf)
    tube_OD = (0.75*25.4)/1000       #tube_OD fixed 3/4 inch 
    print("Tube outer diameter: ", tube_OD)
    #CHOICE OF TUBE THICKNESS (TUBE_ID)
    inner_with_OD19 = [0.01224,0.01295,0.01351,0.01422,0.01483,0.01539,0.01575,0.01610,0.01656,0.01727]
    
    for tube_ID in reversed(inner_with_OD19):
        Sigma_max = 0
        for r in list(np.linspace((tube_ID/2), (tube_OD/2), 10, endpoint=True)):
            sig_tan = (Phi*((tube_ID*0.5)**2) - Pci*((tube_OD*0.5)**2) - ((tube_OD*0.5)**2)*((tube_ID*0.5)**2)*(Phi-Pci) / (r**2)) / (((tube_OD*0.5)**2)- ((tube_ID*0.5)**2))
            sig_rad = (Phi*((tube_ID*0.5)**2) - Pci*((tube_OD*0.5)**2) + ((tube_OD*0.5)**2)*((tube_ID*0.5)**2)*(Phi-Pci) / (r**2)) / (((tube_OD*0.5)**2)- ((tube_ID*0.5)**2))
            von_mises = pow(((sig_tan**2) -(sig_tan*sig_rad) + (sig_rad**2)),0.5) 
            # print(sig_tan,sig_rad,von_mises)
            if von_mises > Sigma_max:
                Sigma_max = von_mises
        n = yield_st / Sigma_max
        if n > sf:
            print("Tube ID chosen: " + str(tube_ID) + " m")
            print("Highest von mises stress: ", Sigma_max)
            # print("n = " + str(n))
            break
    tube_A = np.pi * (tube_ID**2) / 4
    
    #TUBE PATTERN AND SHELL
    N_tubes = 3500 #var           #2000 - 16000
    print("Tubecount = " + str(N_tubes))
    tube_clearance = tube_OD/3     #C
    print("tube clearance: ", tube_clearance)
    Pt = tube_OD + tube_clearance #tube pitch
    print("Tube pitch: ", Pt)
    PR = Pt / tube_OD             #tube pitch ratio : 1.2 - 1.5
    print("Tube pitch ratio = " + str(PR))
    Tube_pass = 2
    print("Tube pass: ", Tube_pass)
    CL = [0.87 , 1]               #Angle of pattern 0.87 : 30 60 degrees, 1 : 45 90
    CTP = [0.93, 0.9 ,0.85]       #tube pass parameter 1, 2, 3
    
    L_available = [1.83, 2.44,3.66 ,4.88, 6.1,7.32 ,8.54 ,9.76 ,10.98 ,12.2,15.25,18.3]
    
    Ao = A_init
    L = Ao / (np.pi * N_tubes * tube_OD)
    print("Calculated L from Area = " + str(L)+ " m")  
    
    for length in L_available:
        if L > max(L_available):
            print("WARNING: L is too high")
            break
        if L <= length :
            L = length
            break
        
    print("Chosen L from available lengths = " + str(L)+ " m") 
    Ao = N_tubes* np.pi * tube_OD * L             #Tubewall Heat Transfer Area
    print("Design Area: " + str(Ao) + " m^2")   
    CL_chosen = CL[0]
    if CL_chosen == 0.87:
        print("Tube Arrangement : Triangle (30 deg , 60 deg) ")
        print("CL: ",CL_chosen)
    else: 
        print("Tube Arrangement : Square (45 deg , 90 deg) ")
        print("CL: ",CL_chosen)
        
    CTP_chosen = CTP[Tube_pass - 1]
    print("CTP: ", CTP_chosen)
    Ds = 0.637* pow(CL_chosen /CTP_chosen ,0.5) * pow((Tube_pass*Ao*(PR**2)*tube_OD) / L, 0.5) # 2 for UTUBE TUBESHEET
    print("Shell Inner Diameter = " + str(Ds) + " m")
    
    No_baf = 3 #Rod baffles
    print("Number of rod baffles: ", No_baf)
    B = (L/2) / (No_baf+1) 
    print("Baffle spacing: ", B)
    As = Ds * tube_clearance* B / Pt                 #DsCB/Pt 
    print("As: ",As)
    #Shell OD Calculation
    
    Sigma_max = 0
    shell_OD = Ds + 0.001
    r = Ds/2
    
    while True:
        
        sig_tan = (Pci*((Ds*0.5)**2) - 0.1*((shell_OD*0.5)**2) - ((shell_OD*0.5)**2)*((Ds*0.5)**2)*(Pci-0.1) / (r**2)) / (((shell_OD*0.5)**2)- ((Ds*0.5)**2))
        
        sig_rad = (Pci*((Ds*0.5)**2) - 0.1*((shell_OD*0.5)**2) + ((shell_OD*0.5)**2)*((Ds*0.5)**2)*(Pci-0.1) / (r**2)) / (((shell_OD*0.5)**2)- ((Ds*0.5)**2))
        
        von_mises = pow(((sig_tan**2) -(sig_tan*sig_rad) + (sig_rad**2)),0.5) 
        
        ns = Carbon_steel['Syt'] / von_mises
        if ns > sf:
            print("Shell Outer diameter: " + str(shell_OD) + " m")
            print("Shell thickness: " + str((shell_OD - Ds)*0.5) + " m")
            print("Maximum von mises in shell: ", von_mises)
            #print("n = " + str(n))
            break
     
        shell_OD = shell_OD + 0.001
    shell_t = 0.5*(shell_OD - Ds)
    
    #BOILING HT COEFFICIENT
    #DATA FOR SHAH CORRELATION Pg.527 - 532 Heat Exchangers : Selection , Rating and Thermal Design
    
    G = mf_shellside/As              #mass_flux_on_shellside
    print("mass flux on shellside: ", G)
    x = xco                          #steam quality
    print("Steam quality: ", x)
    mul = Co.Liquid.mu               #liquid dynamic viscosity
    print("Shell side film dynamics viscosity: ", mul)
    kl = Co.Liquid.k                 #thermal conductivity of liquid
    print("thermal conductivity of liquid at film (shell): ", kl)
    Prl = Co.Liquid.Prandt           #Prandtl number of liquid
    print("Prandtl number of liquid at film (shell): ", Prl)
    rhol = Co.Liquid.rho             #density of liquid
    print("Film liquid density: ", rhol)
    rhog = Co.Vapor.rho              #density of vapor
    print("Film Vapour density: ", rhog)
    qf = Power/Ao                    #heat flux
    print("Heat flux qf: ",qf)
    ifg = (Co.Vapor.h-Co.Liquid.h)   #Latent heat of vaporization
    print("Latent heat of vapourization: ", ifg)
    #print("hg:",Co.Vapor.h ,"hf: ", Co.Liquid.h)
    g = 9.81                         #gravitational acceleration
    hLo = 0.023 * pow((G*(1-x)*Ds / mul),0.8) * pow(Prl,0.4) * (kl / Ds) #Dittus Boelter
    print("hLo: ", hLo)
    
    #NON DIMENSIONAL CONSTANTS
    CO = pow((1/x)-1,0.8)*pow((rhog/rhol),0.5) #convection number
    print("Convection number Co: ",CO )
    Bo = qf/(G*ifg) #boiling number
    print("Boiling number Bo: ",Bo)
    FrL = pow(G,2)/((rhol**2)*g*Ds) #froude number
    print("Froude number: ", FrL)
    #print(Co,Bo,FrL)
    Ns = CO
    print("Ns : ", Ns)
    Fcb = 1.8 / pow(Ns,0.8)
    print("Fcb: ", Fcb)
    if Bo >= 11 * 10**(-4):
        psi = 14.7
        print("Psi: ", psi)
    else:
        psi = 15.43
        print("Psi: ", psi)
    if Ns < 1:
        F = Fcb
        if Bo > 1.9 * 10**(-5) :
            Fnb = 231 * pow(Bo,0.5)
            if Fnb > Fcb:
                F = Fnb
        elif Bo < 0.3* 10**(-4) :
            Fnb = 1 + 46 * pow(Bo,0.5)
            if Fnb > Fcb:
                F = Fnb
    elif Ns > 0.02 and Ns < 1:
        
        Fbs = psi* (Bo**0.5) * np.exp(2.74*pow(Ns,-0.1))
        if Fbs > Fcb:
            F = Fbs
    elif Ns < 0.1 :
        Fbs = psi* (Bo**0.5) * np.exp(2.74*pow(Ns,-0.15))
        if Fbs > Fcb:
            F = Fbs
    print("F for Shah correlation: ",F)
    #SHAH CORRELATION
    hTP = F * hLo
    print("h in shellside from Shah correlation =" + str(hTP) + " W/m^2 K")
    
    #TUBESIDE h - DITTUS BOELTER
    Re_tube = (tube_ID * (mf_tubeside / (N_tubes*Hi.Liquid.rho * tube_A))) / Hi.Liquid.nu
    print("Re in tube",Re_tube)
    kt = Hi.Liquid.k
    print("Thermal conductivity in tube: ", kt)
    Prt = Hi.Liquid.Prandt
    print("Prandtl in tube: ", Prt)
    Nu = 0.023 * pow(Re_tube,0.8) * pow(Prt,0.4)
    print("Nu from dittus boelter in tube: ", Nu)
    # fg = pow((1.58 * np.log(Re_tube) - 3.28),-2)
    # nu = ((fg/2) * (Re_tube - 1000) * Prt)/(1 + 12.7 * pow((fg/2),0.5)*(pow(Prt,2/3) - 1))
    #print("Nu tube dittus : " + str(Nu))
    
    h_tubeside = Nu*kt / tube_ID
    print("h in tubeside = "+ str(h_tubeside) + " W/m^2 K")
    
    #EQUIVALENT DIAMETERS
    if CL_chosen == 0.87 :
        De = 4*(((Pt**2)*pow(3,0.5)/4) - (np.pi * (tube_OD**2) /8))/(np.pi*tube_OD/2)
    else :
        De = 4*(((Pt**2) - (np.pi * (tube_OD**2) /4)))/(np.pi*tube_OD)
    print("equivalent/ hydraulic diameter of shell De:", De)
    #PRESSURE DROP CALCULATIONS
    
    #SHELLSIDE
    Re_s = G * De / (Cb.Liquid.mu)
    print("Shellside Re: ",Re_s)
    if Re_s <400 or Re_s > 10**6:
        print("Warning: Re_s out of range")
    f = np.exp(0.576 - 0.19* np.log(Re_s))
    print("f for shellside Re: ", f)
    phi_s = pow((Cb.Liquid.mu / Ci.Liquid.mu),0.14)
    print("Phi_s for pressure drop calc: ", phi_s)
    Nb_plus_1 = 1 + No_baf
    print("Nb + 1: ", Nb_plus_1)
    rho_s = Cb.Liquid.rho
    print("density of liquid shellside: ", rho_s)
    Shellside_Pdrop = (f*(G**2)*Nb_plus_1*Ds)/(2*rho_s * De * phi_s)
    hydrostat_Pdrop = Cb.Liquid.rho * g * (L/2)
    #Shellside_Pdrop += hydrostat_Pdrop
    #Annular Area surrounding Shell
    
    print("Shellside Pressure Drop = "+ str(Shellside_Pdrop/1000) + " kPa")
    
    #TUBESIDE
    Np = Tube_pass
    um = mf_tubeside / (N_tubes*Hi.Liquid.rho * tube_A) #tube fluid velocity 1.40 - 3.00
    print("Tube fluid Velocity: " + str(um) + " m/s")
    if Re_tube <= 2 * (10**4):
        ft = 0.316 * pow(Re_tube,-0.25)
        print("ft: ",ft )
    elif Re_tube <= 3 * (10**5):
        ft = 0.184 * pow(Re_tube,-0.20) 
        print("ft: ", ft)
    else:
        print("WARNING: Re_tube out of range")
        ft = 1
    Tubeside_Pdrop = ((4*ft*L*Np / tube_ID) + 4 * Np) * ((Hb.Liquid.rho) *(um**2) /2)
    print("Tubeside Pressure Drop = "+ str(Tubeside_Pdrop/1000) + " kPa")
    
    #COST
    Price_of_tubes = mat['Cost']*mat['rho']*(np.pi)*(tube_OD-tube_ID)*0.5*tube_OD*L*N_tubes 
    print("Price of tubes, USD" ,Price_of_tubes)
    L_Shell = 2*L
    Price_of_shell = np.pi*((shell_OD-Ds)/2)*L_Shell*shell_OD*Carbon_steel['rho'] * Carbon_steel['Cost']
    
    print("Price of shell, USD" ,Price_of_shell)
    pump_eff = 0.85
    print("Rho bulk: ", Hb.Liquid.rho)
    tube_side_pumppower = mf_tubeside* Tubeside_Pdrop/ (pump_eff * Hb.Liquid.rho)
    shell_side_pumppower = mf_shellside * Shellside_Pdrop/ (pump_eff * Cb.Liquid.rho)   #mf_steam because this is makeup shellside water
    Pumping_power = (tube_side_pumppower + shell_side_pumppower) / 1000
    Elec_cost_business_BD = 0.106                                              #USD/kWh business in Bangladesh
    Year = 24*365                                                              #hours
    Pumping_op_cost = Elec_cost_business_BD * Pumping_power * Year
    print("Cost of pumping annually, USD" ,Pumping_op_cost)
    Total_cost = Price_of_shell + Price_of_tubes 
    print("minimum construction cost, USD" ,Total_cost)
    
    #EQUIVALENT U
    
    Tflu = (tube_OD/tube_ID)*pow(h_tubeside,-1)                #tubeside fluid resistance
    Tfou = (tube_OD/tube_ID)*Rfw #tubeside fouling
    Dm = (tube_OD-tube_ID)/np.log((tube_OD/tube_ID))
    Tube_wall = (tube_OD-tube_ID)*tube_OD/(ktube*Dm)           #wall resistance
    Ssfou = Rfs                                                #shellside fluid resistance
    Ssflu = pow(hTP,-1)                                        #shellside fluid resistance
    U_foul = pow(Ssflu + Ssfou + Tube_wall + Tfou+ Tflu,-1)    #Fouling included
    #U = pow(Ssflu + Tube_wall + Tflu,-1)
    #print("U = " + str(U) + " W/m^2K")
    print("U_with_fouling = " + str(U_foul) + " W/m^2K")
    current = correction_F*U_foul*Ao*LMTD/(10**3)
    print("Power generated by current Area = " + str(current) + ' kW')
    overdesign = (current-init_rating)*100/init_rating
    print("Overdesign : " + str(overdesign) + " %" )
    
    data[it] = [var,Ds,shell_OD,Ao,L,um,Tubeside_Pdrop, Shellside_Pdrop,Price_of_tubes,Price_of_shell,Pumping_op_cost,Total_cost , U_foul,current,overdesign]
    it +=1
    max_U = U_foul
    if U_foul > max_U:
        max_U = U_foul
#print(data)
#file = pd.DataFrame(data,columns = col)
#file.to_excel("Result.xlsx")