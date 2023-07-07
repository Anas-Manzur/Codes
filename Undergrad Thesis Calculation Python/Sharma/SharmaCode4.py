import numpy as np
from matplotlib import pyplot as plt
tnrfont = {'fontname':'Times New Roman'}


planck = 6.626e-34                  #J-s
pls_dur = 100e-15                      #s
rep_rate = 1000                           #Hz
l_area = 1.12e-12                   #cm^2
ph_lambd = 230.1e-9                  #m
c = 3*10**8                             #m/s
ph_freq = c/ph_lambd                    #Hz
l_linewidth = 200*c*100                   #Hz


k = 1.38e-23                        #Boltzmann Constant in SI
m = 28e-3/(6.023e23)            #Atom Mass (kg)

I_mod = np.exp(-0.011*12.7-0.138*2.5)
sig_0 = 1.5e-35
sig_2 = sig_0/(np.sqrt(np.pi)*l_linewidth)
sig_ion = 10e-18
sig_Q = 28.4e-16                    #Quenching cross section (cm^2)
a = 1/(24.3e-9)                             # s^-1


def get_w13(I,sig_2,P):
    return sig_2*np.power(I,2)

def get_q(I,sig_Q):
    return sig_Q*np.power(I,1)

def get_p_ion(I,sig_ion,P):
    return sig_ion*np.power(I,1)


nCO = np.array(([[9.66e17,4], [1.45e18,6], [2.42e18,10]],[[2.9e18,4], [5.8e18,8], [1.45e19,20]],[[4.83e18,4], [2.42e19,20], [1.21e20,100]]))
P = [1,3,5]

ne_n_percent = [0,0,0] 
i = 0
for nCO_row in nCO[0:][:]:
    for nCO_obj in nCO_row:
        plt.figure(str(i+1))
        n_percent = nCO_obj[1]
        n = [nCO_obj[0],0]  
        count = 0
        for E in np.linspace(8e-6, 20e-6, 12):
            ph_no = E*1000*0.7/(planck*ph_freq)
            ph_I = ph_no/l_area
            w13 = get_w13(ph_I,sig_2,P[i])
            q = get_q(ph_I,sig_Q)           
            p_ion = get_p_ion(ph_I,sig_ion, P[i])
            
            A = w13 + q + p_ion + a
            K = (A+w13)/2 + 0.5*np.sqrt(np.power(A+w13,2)-4*w13*(p_ion+q))
            L = (A+w13)/2 - 0.5*np.sqrt(np.power(A+w13,2)-4*w13*(p_ion+q))
            n[1] = p_ion*n[0]/n_percent/(p_ion+q)*(1+(L/(K-L))*np.exp(-K*pls_dur)-(K/(K-L))*np.exp(-L*pls_dur))
            n[1] = n[1]*np.power(n_percent,1/P[i]) + n[1]*np.log(np.power(P[i],0.9))
            
            if count == 0:
                n1 = [n[0]]
                ne = [n[1]]
                count += 1
            else:
                n1.append(n[0])
                ne.append(n[1])
            
               
        print("{:.3e}".format(ne[11]))
            
        plt.plot(np.linspace(8, 20, 12),ne, label = "nCO = " + str(nCO_obj[0]))
        
    
    plt.xlabel("Pulse Energy (μJ)", **tnrfont)
    plt.ylabel("Ne (cm^-3)", **tnrfont)
    plt.xlim([6,22])
    plt.ylim([0,4e11])
    plt.grid(True)
    plt.title(str(P[i])+" bar",**tnrfont)
    plt.legend(loc = 2)
    i+=1

plt.show()
