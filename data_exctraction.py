import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

ds = xr.open_dataset(r"C:\\Users\\Utente\\Desktop\\newa_mesoscale_ts_.nc")
#print(ds)
ws_original = np.array(ds["WS"].values)
ws_original=ws_original[:,0]

#print(ws*6.9/6.64)
mean_array=np.array([6.754,6.982,6.992,7.114,7.124,7.114,6.907,6.907,6.907,7.03,7.03,7.114,7.207,6.836,6.836,6.836,6.95,7.03,7.121,7.121,6.769,6.769,6.875,6.95,6.95,7.037,7.037,6.704,6.704,6.769,6.875,6.875,6.875])
years=np.arange(1995,2023,1)
mean_cons_array=np.array([6.43938,6.43938,6.68005,6.58179,6.46992,6.58179,6.40428,6.63992,6.59699,6.42225,6.65128,6.65128,6.60875,6.59198,6.4577,6.39678,6.61357,6.57399,6.40428,6.40428,6.35884,6.55171,6.55171,6.52989,6.37574,6.59198,6.59198,6.51169,6.44242,6.51169,6.44242,6.34484,6.5444])
turbina=0
for trb_mean in mean_cons_array: #togliere cons 
    turbina=turbina+1
    ws=ws_original*trb_mean/np.mean(ws_original) #togliere cons
    new_ws_array=[]
    dec,gen,feb,mar,apr,mag,giu,lug,ago,set,ott,nov=[],[],[],[],[],[],[],[],[],[],[],[]
    for speed in ws:
        speed=float(speed)
        #new_speed=int(speed)
        if speed%1>=0.5:
            new_speed=int(speed)+1
        else :
            new_speed=int(speed)
        new_ws_array.append(new_speed)
    new_ws_array=np.array(new_ws_array)
    #ora devo fare la roba della divisione dei mesi
    dec.extend(new_ws_array[0:48])
    prev_index=48
    for year in years:
        gen.extend(new_ws_array[prev_index:prev_index+1488])
        prev_index=prev_index+1488
        if year%4!=0:
            feb.extend(new_ws_array[prev_index:prev_index+1344])
            prev_index=prev_index+1344
        else:
            feb.extend(new_ws_array[prev_index:prev_index+1392])
            prev_index=prev_index+1392
        mar.extend(new_ws_array[prev_index:prev_index+1488])
        prev_index=prev_index+1488
        apr.extend(new_ws_array[prev_index:prev_index+1440])
        prev_index=prev_index+1440
        mag.extend(new_ws_array[prev_index:prev_index+1488])
        prev_index=prev_index+1488
        giu.extend(new_ws_array[prev_index:prev_index+1440])
        prev_index=prev_index+1440
        lug.extend(new_ws_array[prev_index:prev_index+1488])
        prev_index=prev_index+1488
        ago.extend(new_ws_array[prev_index:prev_index+1488])
        prev_index=prev_index+1488
        set.extend(new_ws_array[prev_index:prev_index+1440])
        prev_index=prev_index+1440
        ott.extend(new_ws_array[prev_index:prev_index+1488])
        prev_index=prev_index+1488
        nov.extend(new_ws_array[prev_index:prev_index+1440])
        prev_index=prev_index+1440
        dec.extend(new_ws_array[prev_index:prev_index+1488])
        prev_index=prev_index+1488
    #print(np.array(dec[0:1000]) )
    #print(len(dec)) 
    #finito il for annuale , ora devo fare le matrici per ogni mese 
    dec_matr,gen_matr,feb_matr,mar_matr,apr_matr,mag_matr,giu_matr,lug_matr,ago_matr,set_matr,ott_matr,nov_matr=np.zeros((33,33)),np.zeros((33,33)),np.zeros((33,33)),np.zeros((33,33)),np.zeros((33,33)),np.zeros((33,33)),np.zeros((33,33)),np.zeros((33,33)),np.zeros((33,33)),np.zeros((33,33)),np.zeros((33,33)),np.zeros((33,33))
    #ora devo mettere i cosi nelle matrici
    index=0
    for speed in dec[1:]:
        index=index+1
        prev_speed=dec[index-1]
        dec_matr[prev_speed,speed]=dec_matr[prev_speed,speed]+1
    dec_matr=dec_matr/np.sum(dec_matr)
    index=0
    for speed in gen[1:]:
        index=index+1
        prev_speed=gen[index-1]
        gen_matr[prev_speed,speed]=gen_matr[prev_speed,speed]+1
    gen_matr=gen_matr/np.sum(gen_matr)
    index=0
    for speed in mar[1:]:
        index=index+1
        prev_speed=mar[index-1]
        mar_matr[prev_speed,speed]=mar_matr[prev_speed,speed]+1
    mar_matr=mar_matr/np.sum(mar_matr)
    index=0
    for speed in feb[1:]:
        index=index+1
        prev_speed=feb[index-1]
        feb_matr[prev_speed,speed]=feb_matr[prev_speed,speed]+1
    feb_matr=feb_matr/np.sum(feb_matr)
    index=0
    for speed in mag[1:]:
        index=index+1
        prev_speed=mag[index-1]
        mag_matr[prev_speed,speed]=mag_matr[prev_speed,speed]+1
    mag_matr=mag_matr/np.sum(mag_matr)
    index=0
    for speed in apr[1:]:
        index=index+1
        prev_speed=apr[index-1]
        apr_matr[prev_speed,speed]=apr_matr[prev_speed,speed]+1
    apr_matr=apr_matr/np.sum(apr_matr)
    index=0
    for speed in giu[1:]:
        index=index+1
        prev_speed=giu[index-1]
        giu_matr[prev_speed,speed]=giu_matr[prev_speed,speed]+1
    giu_matr=giu_matr/np.sum(giu_matr)
    index=0
    for speed in lug[1:]:
        index=index+1
        prev_speed=lug[index-1]
        lug_matr[prev_speed,speed]=lug_matr[prev_speed,speed]+1
    lug_matr=lug_matr/np.sum(lug_matr)
    index=0
    for speed in ago[1:]:
        index=index+1
        prev_speed=ago[index-1]
        ago_matr[prev_speed,speed]=ago_matr[prev_speed,speed]+1
    ago_matr=ago_matr/np.sum(ago_matr)
    index=0
    for speed in set[1:]:
        index=index+1
        prev_speed=set[index-1]
        set_matr[prev_speed,speed]=set_matr[prev_speed,speed]+1
    set_matr=set_matr/np.sum(set_matr)
    index=0
    for speed in ott[1:]:
        index=index+1
        prev_speed=ott[index-1]
        ott_matr[prev_speed,speed]=ott_matr[prev_speed,speed]+1
    ott_matr=ott_matr/np.sum(ott_matr)
    index=0
    for speed in nov[1:]:
        index=index+1
        prev_speed=nov[index-1]
        nov_matr[prev_speed,speed]=nov_matr[prev_speed,speed]+1
    nov_matr=nov_matr/np.sum(nov_matr)
    index=0
    matrices=[gen_matr,feb_matr,mar_matr,apr_matr,mag_matr,giu_matr,lug_matr,ago_matr,set_matr,ott_matr,nov_matr,dec_matr]
    for matr in matrices:
        plt.imshow(matr[0:31,0:31], cmap='plasma', origin='lower')
        plt.colorbar(label='Value')
        plt.xlabel("next wind speeds [m/s]")
        plt.ylabel("previous wind speeds [m/s]")
        plt.title("Transition rate matrix")
        plt.show()
    '''filename = f"cons_turbina_{turbina}.txt"
    with open(filename, "w") as f:
        for idx, M in enumerate(matrices):
            f.write(f"====== MATRICE {idx} ======\n")
            np.savetxt(f, M, fmt="%.18e")
            f.write("\n\n")
'''
