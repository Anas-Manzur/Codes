import numpy as np
from scipy import integrate

planck = 6.626*10**-34                  #J-s
pls_eng = 90*10**-6                      #J
pls_dur = 125*10**-15                      #s
rep_rate = 10                           #Hz
avg_power = pls_eng * rep_rate          #W or J/s

ph_lambd = 230*10**-9                   #m
c = 3*10**8                             #m/s
ph_freq = c/ph_lambd                    #Hz

n_ph_sec = avg_power/(planck*ph_freq)   #no. of photons per sec
d0 = 7.5*10**-1                          #beam dia (cm)
ph_flux = n_ph_sec /(np.pi/4*d0**2)     #photons/cm^2-s

l_fwhm = 200                            #Laser FWHM (cm^-1)

v0 = 1/(ph_lambd*100)                   #Frequency at centre of spectral line (cm^-1)
vL0 = v0                                #Laser centre frequency (cm-1)
Temp = 1700                              #Temperature (K)
k = 1.38*10**-23                        #Boltzmann Constant in SI
m = 28*10**-3/(6.023*10**23)            #Atom Mass (kg)

spec_fwhm = np.sqrt(2*k*Temp/(m*c**2))*v0           #FWHM of spctral line (Hz) [Doppler Broadening (Wikipedia)]

def h (vL, vL0, fwhm):                  #Autocorrelation of Laser spectral Profile (Fiechtner et. al 2000)
    rng = (vL - 2*vL0)/(2**0.5*fwhm)
    expn = -4*np.log(2*rng**2)
    result = 2/fwhm * (np.log(2)/(np.pi*2))*np.exp(expn)
    return result

def g (v,v0,fwhm):                      #Spectral line function (Gaussian)
    coeff = 1/(fwhm*np.sqrt(np.pi))
    return coeff*np.exp(-((v-v0)/fwhm)**2)

def gxh (v, v0, vL0, spec_fwhm, l_fwhm):
    c1 = 1/(v0*np.sqrt(np.pi))
    c2 = 2/l_fwhm * np.sqrt(np.log(2)/(2*np.pi))
    exp = ((v - v0)/spec_fwhm)**2 + 4*np.log(2*((v - 2*vL0)/(np.power(2,0.5)*l_fwhm))**2)
    return c1*c2*np.exp((-1)*exp)

i = 0
for v in np.linspace(43400, 43500, 10000):
    if (g(v,v0,spec_fwhm)!=0):
        if i == 0:
            x = [v]                               #x is basically the values for which g(v) is non-zero, 2vL
        
        x = x + [v]                   
        i = i+1

i = 0
for v in x:
    if i == 0:
        y = [gxh (v, v0, vL0, spec_fwhm, l_fwhm)]      #y is the non-zero gxh values
        i = i+1
        continue
    y = y + [gxh (v, v0, vL0, spec_fwhm, l_fwhm)]   
count = 0   
for i in range(len(x)):
    if y[i] != 0:
        if count == 0:
            xc = [x[i]]
            yc = [y[i]]
            count += 1
        else:
            xc += [x[i]]
            yc += [y[i]]
    

Gam = integrate.simpson(yc, xc, even = "avg")    #Gamma


sig0 = 1.5*10**-35                      #cm^4
gi = 1                                  #Laser intensity factor
w13 = 2*sig0*(pls_eng/(planck*ph_freq*pls_dur*((np.pi/4)*d0**2)))**2*gi*Gam          #Two photon absorption rate coefficient

#print(y)
#print(Gam)
print("{:3e}".format(pls_eng/(planck*ph_freq*pls_dur*((np.pi/4)*d0**2))))
print(ph_flux)
print("{:.3e}".format(w13))