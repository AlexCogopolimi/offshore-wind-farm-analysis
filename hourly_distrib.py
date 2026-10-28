import numpy as np
import matplotlib.pyplot as plt

def read_matrices_from_file(filename):
    matrices = []
    current_lines = []
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("====== MATRICE"):
                if current_lines:
                    matrices.append(np.loadtxt(current_lines))
                    current_lines = []
            elif line.strip():   
                current_lines.append(line)
        if current_lines:
            matrices.append(np.loadtxt(current_lines))

    return matrices

powertrb=[0,0,0,0,540,1250,2600,4100,6070,9300,12500,15000]
powertrb.extend(15000*np.ones(18))
powertrb.extend(np.zeros(10))
powertrb=np.array(powertrb)
prezzo = np.loadtxt("prezzi.txt")
#matrici = read_matrices_from_file("turbina_1.txt")
#print(matrici[11])
energy=[]
ore_mensili = np.array([744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744])
density_corr_array=np.array([0.993653314881756,0.991912201661357,0.983297365794921,0.976175708722428,0.96486158767366,0.948373753540184,0.937691392228153,0.93738084697489,0.948373753540184,0.95995301592019,0.977186765903912,0.993653314881756])
annual_pow_degradation=np.array([1,0.9936,0.98724096,0.980922617856,0.974644713101722,0.968406986937871,0.962209182221468,0.956051043455251,0.949932316777138,0.943852749949764,0.937812092350085,0.931810094959045,0.925846510351307,0.919921092685059,0.914033597691875,0.908183782666647,0.90237140645758,0.896596229456252,0.890858013587732,0.88515652230077,0.879491520558045,0.873862774826474,0.868270053067585,0.862713124727952,0.857191760729693,0.851705733461023,0.846254816766873,0.840838785939565,0.835457417709552,0.83011049023621])
array_vento=[] #plot mensile vento
oraanno=0
revenue=[]
price_plot=[]
#print(np.mean(prezzo))
'''plt.plot(np.arange(1,8761,1),prezzo)
plt.show()'''
n_hours_year = len(prezzo)
ore_mesi=0
for anno in range(30):
    
    for j in np.arange(1,34,1):
        
        matrici = read_matrices_from_file(f"turbina_{j}.txt") # tolgiere cons
        for i in np.arange(0,12,1): 
            
            for hour in np.arange(1,ore_mensili[i]+1,1):
                #print(oraanno)
                idx_prezzo = oraanno % n_hours_year
                prob=matrici[i].flatten()
                choice=np.random.choice(33*33,p=prob)
                r,c=divmod(choice,33)
                array_vento.append(c+1) #serve per plot mensile vento 
                energy.append(powertrb[c]*density_corr_array[i]*annual_pow_degradation[anno]*0.96*0.965*0.96)
                revenue.append((powertrb[c]*density_corr_array[i]*annual_pow_degradation[anno]/1000)*0.965*0.96*0.96*prezzo[idx_prezzo])
                price_plot.append(prezzo[idx_prezzo])
                oraanno+=1
                
            
            '''fig,ax1=plt.subplots()
            ax1.set_xlabel("hours [h]")
            ax1.set_ylabel("wind speed [m/s]")
            ax1.plot(np.arange(1,ore_mensili[i],1),array_vento,label='wind speed')
            
            ax2=ax1.twinx()
            ax2.plot(np.arange(1,ore_mensili[i],1),price_plot,color="orange",label='cost of electricity')
            ax2.tick_params( axis="y")
            ax2.set_ylabel("electricity price [$/MWh]")
            plt.title("wind speed and cost of electricity for a month")
            
            plt.show()'''
            price_plot=[]
            array_vento=[]
    

    
    
    print(np.sum(revenue))
    energy=[]
    revenue=[]