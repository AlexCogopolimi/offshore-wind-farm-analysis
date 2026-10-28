import numpy as np
import pandas as pd

df = pd.read_excel("hourly_price.xlsx")
#print(str(df.iloc[:,2].to_string(index=False)).replace(",","."))
ore_mensili = np.array([744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744])
months=["genn","febb","mar","apr","magg","giu","lugl","ago","sett","nov","dec"]
#array=np.array(str(df.iloc[:,2].to_string(index=False)).replace(",","."))
#print(len(array))
prezzi = df.iloc[:, 0].astype(float)
arr = prezzi.to_numpy()
print(arr)
np.savetxt("prezzi.txt", arr)
#for month in months:
