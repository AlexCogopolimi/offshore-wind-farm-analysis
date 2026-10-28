import numpy as np
from scipy.special import gamma
import matplotlib.pyplot as plt

def find_c_k(ws,pd):
    k=np.linspace(1,2,10000) #10000 punti molto simile a excel, 1000 uguale fino a due/tre cifre dopo virgola
    diff_pd=lambda k:pd-(ws**3*gamma(1+3/k)*0.5*1.2)/((gamma(1+1/k))**3) #risolve sistema 2x2 trovando k,poi c fissato
    idx=np.argmin(np.abs(diff_pd(k)))
    k_best=k[idx]
    c_best=ws/(gamma(1+1/k_best))
    return c_best,k_best

powertrb=[0,0,0,0,540,1250,2600,4100,6070,9300,12500,15000]
powertrb.extend(15000*np.ones(18))
powertrb=np.array(powertrb)

def energy_prod(trbpow_array,htot,c,k):
    #valori in GWh
    probability = lambda v: np.where(
    v >= 1,
    np.exp(-(((v - 0.5)/c)**k)) - np.exp(-(((v + 0.5)/c)**k)),
    0)
    velocities=np.arange(0,30,1)
    hours_array=probability(velocities)*htot
    energy_array=hours_array*trbpow_array/(10**6)
    return np.sum(energy_array)

ws_array=np.array([6.754,6.982,6.992,7.114,7.124,7.114,6.907,6.907,6.907,7.03,7.03,7.114,7.207,6.836,6.836,6.836,6.95,7.03,7.121,7.121,6.769,6.769,6.875,6.95,6.95,7.037,7.037,6.704,6.704,6.769,6.875,6.875,6.875])
pd_array=np.array([452.6,485.4,487.4,505.2,503.4,503.4,473.1,473.1,473.1,490.5,490.5,505.2,520.3,461.2,461.2,461.2,476.7,490.5,504.4,504.4,449.7,449.7,463.8,476.7,476.7,489.2,489.2,438.5,438.5,449.7,463.8,463.8,463.8])

ws_cons_array=np.array([6.43938,6.43938,6.68005,6.58179,6.46992,6.58179,6.40428,6.63992,6.59699,6.42225,6.65128,6.65128,6.60875,6.59198,6.4577,6.39678,6.61357,6.57399,6.40428,6.40428,6.35884,6.55171,6.55171,6.52989,6.37574,6.59198,6.59198,6.51169,6.44242,6.51169,6.44242,6.34484,6.5444])
pd_cons_array=np.array([377.495,377.495,412.259,398.463,383.637,398.463,372.936,403.816,398.121,375.698,407.742,407.742,401.881,398.696,379.382,372.381,401.782,389.465,372.936,372.936,387.782,393.605,393.605,381.758,369.479,398.696,398.696,387.782,371.895,387.782,378.521,365.441,392.279])

alpha_shear=(150/100)**((np.log(7.22)-np.log(7.01))/(np.log(150)-np.log(100))) #correzione perchè montly ws è data a 100 metri quindi shear calcolata

monthly_ws_correction=alpha_shear*np.array([1.08,1.08,1.05,0.94,1.01,1.08,1.04,0.95,0.79,0.84,0.97,1.17])
monthly_pd_correction=monthly_ws_correction**3
annual_pow_degradation=np.array([1,0.9936,0.98724096,0.980922617856,0.974644713101722,0.968406986937871,0.962209182221468,0.956051043455251,0.949932316777138,0.943852749949764,0.937812092350085,0.931810094959045,0.925846510351307,0.919921092685059,0.914033597691875,0.908183782666647,0.90237140645758,0.896596229456252,0.890858013587732,0.88515652230077,0.879491520558045,0.873862774826474,0.868270053067585,0.862713124727952,0.857191760729693,0.851705733461023,0.846254816766873,0.840838785939565,0.835457417709552,0.83011049023621])

#print(monthly_pd_correction)
ore_mensili = np.array([744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744])
density_corr_array=np.array([0.993653314881756,0.991912201661357,0.983297365794921,0.976175708722428,0.96486158767366,0.948373753540184,0.937691392228153,0.93738084697489,0.948373753540184,0.95995301592019,0.977186765903912,0.993653314881756])
energy=[]
for anno in range(30):
    for i in range(33):
        for j in range(12):
            ws=ws_cons_array[i]*monthly_ws_correction[j] #usando ws_cons_array () anche per pd) si ha stima più conservativa
            pd=pd_cons_array[i]*monthly_pd_correction[j]
            c,k=find_c_k(ws,pd)
            energy.append(energy_prod(powertrb,ore_mensili[j],c,k)*density_corr_array[j]*annual_pow_degradation[anno])

    print(np.sum(energy))
    energy=[]


'''P=np.zeros((31,31))
k,c=1.615512296,7.539665543
probability=lambda v:np.exp(-((v/c)**k))-np.exp(-(((v+1)/c)**k))
velocities=np.arange(0,30,1)
prob_array=probability(velocities)
P=np.diag(prob_array)
print(P) #in realtà l'ultimo è 1 - somma'''
    