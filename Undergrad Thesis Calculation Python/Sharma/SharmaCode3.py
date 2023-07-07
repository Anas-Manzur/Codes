from calendar import c
from time import time
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint
tnrfont = {'fontname':'Times New Roman'}

l_fwhm = 200                   #cm^-1
centre = 1/(230.1e-7)               #cm^-1
std_dev = l_fwhm/(2*np.sqrt(2*np.log(2)))       #cm^-1
max_amp_bfr_chrp = 1/(std_dev*np.sqrt(2*np.pi))
max_amp_aftr_chrp = max_amp_bfr_chrp*np.exp(-0.4847)

planck = 6.626e-34
ph_freq = 3e8/230.1e-9
pls_dur = 100e-15           #s
laser_area = 1.12e-12        #cm^2

def get_omega_12(I):
    sig_abs = 1.5e-35
    G=1
    return np.sqrt(2*G*sig_abs/np.pi)*I/(planck/(2*np.pi)*(3e8/230.1e-9))

def get_Gam_ion(I):
    sig_ion = 9e-18
    return sig_ion*I/(planck/(2*np.pi)*(3e8/230.1e-9))

def get_gam_2(I):
    tau = 25.9e-9                                  #s
    return 1/tau + 28.4e-16*I

def get_omega_34(I):
    c = 3e8
    A_43 = 3e6              #s^-1
    return np.sqrt((2*np.pi*np.power(c,2)*A_43/(planck/(2*np.pi)*np.power((c/230.1e-9),3)))*I)

def get_Gam_diss(I):
    sig_diss = 9e-18*0.5              #s^-1
    return sig_diss*I/(planck/(2*np.pi)*(3e8/230.1e-9))

def get_gam_4(I):
    tau = 55e-9              #s
    return 1/tau + 28.4e-16*0.5*I

def model (n,t,omega_12,Gam_ion,gam_2,omega_34,Gam_diss,gam_4):
    n1 = n[0]
    n2 = n[1]
    n3 = n[2]
    n4 = n[3]
    n5 = n[4]
    n6 = n[5]
    n7 = n[6]
    n8 = n[7]
    dn1dt = -omega_12*n4
    dn2dt = omega_12*n4 - (Gam_ion+gam_2)*n2
    dn3dt = -0.5*(Gam_ion+gam_2)*n3
    dn4dt = -0.5*(Gam_ion+gam_2)*n4 + 0.5*omega_12*(n1-n2)
    dn5dt = Gam_ion*n2 - omega_34*n8
    dn6dt = omega_34*n8-(Gam_diss+gam_4)*n6
    dn7dt = -0.5*(Gam_diss+gam_4)*n7
    dn8dt = -0.5*(Gam_diss+gam_4)*n8 + 0.5*omega_34*(n5-n6)
    return [dn1dt,dn2dt,dn3dt,dn4dt,dn5dt,dn6dt,dn7dt,dn8dt]

def time_delay(lambd1):
    c = 3e11                #mm/s
    lambd1 = lambd1*1e-3    #micro m
    lambd2 = 230.1*2e-3-lambd1
    n_air_1 = np.sqrt(1 + (0.05792105*np.power(lambd1,2)/(np.power(lambd1,2)-238.0185) + (0.00167917*np.power(lambd1,2)/(np.power(lambd1,2)-57.362))))
    n_air_2 = np.sqrt(1 + (0.05792105*np.power(lambd2,2)/(np.power(lambd2,2)-238.0185) + (0.00167917*np.power(lambd2,2)/(np.power(lambd2,2)-57.362))))
    n_silica_1 = np.sqrt(1 + (0.696166300*np.power(lambd1,2)/(np.power(lambd1,2)-4.67914826e-3) + (0.407942600*np.power(lambd1,2)/(np.power(lambd1,2)-1.35120631e-2)) + (0.897479400*np.power(lambd1,2)/(np.power(lambd1,2)-97.9340025))))
    n_silica_2 = np.sqrt(1 + (0.696166300*np.power(lambd2,2)/(np.power(lambd2,2)-4.67914826e-3) + (0.407942600*np.power(lambd2,2)/(np.power(lambd2,2)-1.35120631e-2)) + (0.897479400*np.power(lambd2,2)/(np.power(lambd2,2)-97.9340025))))
    v_air_1 = c*n_air_1
    v_air_2 = c*n_air_2
    v_silica_1 = c/n_silica_1
    v_silica_2 = c/n_silica_2
    
    del_t = (20+150-12.7)*(1/v_air_1-1/v_air_2) + (2.5+12.7)*(1/v_silica_1-1/v_silica_2)      #s
    if lambd1 >= lambd2:
        del_t_max = 1/(4*np.pi*c*1e-3*(1/(230.1e-9*2)-1/lambd1*1e-6))                   #s
    else:
        del_t_max = 1/(4*np.pi*c*1e-3*(1/(230.1e-9*2)-1/lambd2*1e-6))
    
    return np.absolute(del_t*1e15),np.absolute(del_t_max*1e15)                                        #fs


nCO = np.array(([9.66e17, 1.45e18, 2.42e18],[2.9e18, 5.8e18, 1.45e19],[4.83e18, 2.42e19, 1.21e20]))
P = [1,3,5]

i = 0
for nCO_row in nCO[0:][:]:
    for nCO_obj in nCO_row:
        plt.figure(str(i+1))
        n0 = [nCO_obj,0,0,0,0,0,0,0]
        ne=0      
        count = 0
        for E in np.linspace(8e-6, 20e-6, 100):
            ph_per_sec = E*1000/(planck*ph_freq)
            I = ph_per_sec/laser_area
            omega_12 = get_omega_12(I)
            Gam_ion = get_Gam_ion(I)
            gam_2 = get_gam_2(I)
            omega_34 = get_omega_34(I)
            Gam_diss = get_Gam_diss(I)
            gam_4 = get_gam_4(I)
            n = odeint(model,n0,[0,pls_dur/2], args = (omega_12,Gam_ion,gam_2,omega_34,Gam_diss,gam_4))
            
            if count == 0:
                ne = [n[1,4]]
                count += 1
            else:
                ne.append(n[1,4])
        print("{:.3e}".format(ne[0]))
        print(n)
        plt.plot(np.linspace(0.7e10, 1.8e10, 100),ne, label = "nCO = " + str(nCO_obj))
    
    plt.xlabel("Intensity (W/cm^2)", **tnrfont)
    plt.ylabel("Ne (cm^-3)", **tnrfont)
    plt.xlim([0.6e10,2e10])
    plt.ylim([0,4e11])
    plt.grid(True)
    plt.title("Figure " + str(i),**tnrfont)
    plt.legend(loc = 2)
    i+=1

plt.show()

