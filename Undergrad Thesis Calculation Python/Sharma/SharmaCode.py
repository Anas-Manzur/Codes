from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
tnrfont = {'fontname':'Times New Roman'}

l_linewidth = 3e10*200                #sec
pls_dur = 126e-15                   #sec
ph_lambd = 230.1e-9                 #m
c = 3e8                             #m/s
ph_freq = c/ph_lambd
l_area = 0.24*200e-4                #cm^2
planck = 6.626e-34                  #Planck const SI
sig0 = 1.5e-35                      #cm^4
K = (np.power(ph_lambd*100,2)/np.power(l_linewidth,2))+0.9694
sig2 = (sig0/(2*np.sqrt(np.pi)*l_linewidth))*np.exp(-K)

def get_w13(I,sig2):
    return sig2*np.power(I,2)

def get_q(I,sig_Q):
    return sig_Q*np.power(I,1)

def get_p_ion(I,sig_ion):
    return sig_ion*np.power(ph_I,1)

def model (n,t,w13,q,a,ppd,p_ion):
    n1 = n[0]
    n3 = n[1]
    ne = n[2]
    dn1dt = -w13*n1 + (q+a)*n3
    dn3dt = w13*n1 - (q+a+ppd+p_ion)*n3
    dnedt = p_ion*n3
    return [dn1dt,dn3dt,dnedt]
    
nCO = np.array(([9.66e17, 1.45e18, 2.42e18],[2.9e18, 5.8e18, 1.45e19],[4.83e18, 2.42e19, 1.21e20]))    


sig_Q = 28.4e-16                    #Quenching cross section (cm^2)



a = 1/(24.3e-9)                             # s^-1
ppd = 4e10                          # s^-1

sig_ion = 7e-17                     #cm^2

#for I in np.linspace(0.7e10, 1.8e10, 100):
#    ph_I = I/(planck*ph_freq)
#    if count == 0:
#        w13 = [get_w13(ph_I,sig2)]
#        q = [get_q(ph_I,sig_Q)]
#        p_ion = [get_p_ion(ph_I,sig_ion)]
#        count += 1
#    else:
#        w13.append(get_w13(ph_I,sig2))
#        q.append(get_q(ph_I,sig_Q))
#        p_ion.append(get_p_ion(ph_I,sig_ion))
 
i = 0
mod_const = 1

for nCO_row in nCO[0:][:]:
    for nCO_obj in nCO_row:
        plt.figure(str(i+1))
        n0 = [nCO_obj,0,0]
        n1=0
        n3=0
        ne=0      
        count = 0
        for I in np.linspace(0.7e10*mod_const, 1.8e10*mod_const, 100):
            ph_I = I/(planck*ph_freq)
            w13 = get_w13(ph_I,sig2)
            q = get_q(ph_I,sig_Q)           
            p_ion = get_p_ion(ph_I,sig_ion)

            n = odeint(model,n0,[0,pls_dur/2], args = (w13,q,a,ppd,p_ion))
        
            if count == 0:
                n1 = [n[1,0]]
                n3 = [n[1,1]]
                ne = [n[1,2]]
                count += 1
            else:
                n1.append(n[1,0])
                n3.append(n[1,1])
                ne.append(n[1,2])
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

#print("{:.3e}".format(w13))
#print("{:.3e}".format(q))
#print("{:.3e}".format(p_ion))
#print("{:.3e}".format(I))
#print(n[1,2])