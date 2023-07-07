import numpy as np
from scipy import integrate

planck = 6.626*10**-34                  #J-s
pls_eng = 7*10**-3                      #J
pls_dur = 8*10**-9                      #s
rep_rate = 10                           #Hz
avg_power = pls_eng * rep_rate          #W or J/s

ph_lambd = 230*10**-9                   #m
c = 3*10**8                             #m/s
ph_freq = c/ph_lambd                    #Hz

n_ph_sec = avg_power/(planck*ph_freq)   #no. of photons per sec
d0 = 10*10**-1                          #beam dia (cm)
ph_flux = n_ph_sec /(np.pi/4*d0**2)     #photons/cm^2-s

l_fwhm = 0.1                            #Laser FWHM (cm^-1)

v0 = 1/(ph_lambd*100)                   #Frequency at centre of spectral line (cm^-1)
Temp = 300                              #Temperature (K)
k = 1.38*10**-23                        #Boltzmann Constant in SI
m = 28*10**-3/(6.023*10**23)            #Atom Mass (kg)

spec_fwhm = np.sqrt(8*k*Temp*np.log(2)/(m*c**2))*v0           #FWHM of spctral line (Hz) [Doppler Broadening (Wikipedia)]

def h (vL, vL0, fwhm):                  #Autocorrelation of Laser spectral Profile (Fiechtner et. al 2000)
    rng = (vL - vL0)/(2**0.5*fwhm)
    expn = -4*np.log(2*rng**2)
    result = 2/fwhm * (np.log(2)/(np.pi*2))*np.exp(expn)
    return result

def g (v,v0,fwhm):                      #Spectral line function (Gaussian)
    coeff = 1/(fwhm/2)
    return np.exp(-(np.log(2)*(coeff*(v - v0))**2))

def gxh (v, v0, spec_fwhm, l_fwhm):
    return g(v,v0,spec_fwhm)*h(v,v0,l_fwhm)

i = 0
for v in np.linspace(43400, 43500, 10000):
    if (g(v,v0,spec_fwhm)!=0):
        if i == 0:
            x = [v/2]                               #x is basically the values for which g(v) is non-zero, not actual freq
        
        x = x + [v/2]                   
        i = i+1

i = 0
for v in x:
    if i == 0:
        y = [gxh (2*v, v0, spec_fwhm, l_fwhm)]      #y is the non-zero gxh values
        i = i+1
        continue
    y = y + [gxh (2*v, v0, spec_fwhm, l_fwhm)]      
    

Gam = integrate.simpson(y[3:-3], x[3:-3], even = "avg")    #Two photon absorption coefficient


sig0 = 1.5*10**-35                      #cm^4
gi = 1                                  #Laser intensity factor
w13 = 2*sig0*ph_flux**2*gi*Gam          #Two photon absorption rate coefficient

#print(y[3:-3])
#print(Gam)
#print(spec_fwhm)
print("{:.3e}".format(w13*pls_dur))
print("{:.3e}".format(w13))