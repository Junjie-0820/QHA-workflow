#!/usr/bin/env python3

import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# temp=[0,500,1000,1500,2000,2500,3000,3500,4000]
temp=[0,1000,2000,3000,4000,5000,6000,7000]
# nv=10
nv=6


fout=open("fe-v-raw.dat","w")

#for it in temp:
#    data=np.loadtxt("mermin-"+str(it)+".dat",skiprows=1)
#    data=np.loadtxt(str(it)+"-vf.dat",skiprows=1)

#    print(it,end=" ",file=fout)
#    for k in range(nv):
#        print(data[k,1],end=" ",file=fout)
#    print("",file=fout)

for it in temp:
    fname = str(it) + "-vf.dat"
    print(it, end=" ", file=fout)

    with open(fname, "r") as f:
        next(f)  
        count = 0
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2:
                continue  
            try:
                val = float(parts[1]) 
                print(val, end=" ", file=fout)
                count += 1
            except ValueError:
                print("Warning: could not convert line:", line.strip())
        if count < nv:
            print(f"\nWarning: {fname} only has {count} lines!", file=sys.stderr)
    print("", file=fout)

fout.close()

data=np.loadtxt("fe-v-raw.dat")

# xnew=np.linspace(0, 4000, num=401, endpoint=True)
xnew=np.linspace(0, 7000, num=701, endpoint=True)
dnew=[]
dnew.append(xnew.tolist())
for k in range(nv):
    x=data[:,0]
    y=data[:,k+1]
    f = interp1d(x, y, kind='quadratic')
    #plt.plot(x,y,'o',xnew,f(new),'-')
    #plt.show()
    dnew.append(f(xnew).tolist())

fout=open("fe-v.dat","w+")
for i in range(701):
    for j in range(nv+1):
        print(dnew[j][i],end=" ",file=fout)
    print("",file=fout)
fout.close()

