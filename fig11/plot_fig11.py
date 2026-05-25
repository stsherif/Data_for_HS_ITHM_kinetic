import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
#from scipy.optimize import curve_fit

from matplotlib import font_manager

font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/times.ttf")
font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/timesbd.ttf")
font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/timesi.ttf")
font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/timesbi.ttf")

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    #"font.size": 25,          # base font size
    #"axes.labelsize": 24,
    #"axes.titlesize": 26,
    #"xtick.labelsize": 25,
    #"ytick.labelsize": 25,
    #"legend.fontsize": 25,
    #"axes.linewidth": 1.2,
    #"xtick.direction": "in",
    #"ytick.direction": "in",
    #"xtick.top": True,
    #"ytick.right": True,
    #"grid.alpha": 0.5
})
import matplotlib
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"]  = 42
#import matplotlib as mpl

#mpl.rcParams["text.usetex"] = False  # disable LaTeX, use mathtext

folder=Path('.')
fnames=[]
fnames_temp=[]
Nx=[6,10,12]
Ny=6
N=[36,60,72]
nh=[0.11,0.25,0.33,0.6]

for f in folder.rglob('*.txt'):
    if f.is_file() and '6x6' in f.name and 'occ' and 'Uinf' in f.name:
        fnames_temp.append(str(f))

for f in folder.rglob('*.txt'):
    if f.is_file() and '12x6' in f.name and 'occ' and 'Uinf' in f.name:
        fnames_temp.append(str(f))

for f in folder.rglob('*.txt'):
    if f.is_file() and '10x6' in f.name and 'occ' and 'Uinf' in f.name:
        fnames_temp.append(str(f))

num_samples=3 #3
num_nh=4
for i in range(num_samples):
     Nh_temp=[]
     for j in range(num_nh):
          match = re.search(r'(\d+)h', fnames_temp[j+i*num_nh])
          Nh_temp.append(int(match.group(1)))
     ind = np.argsort(Nh_temp)
     #print(ind)
     for l in ind:
          fnames.append(fnames_temp[l+i*num_nh])

print(fnames)
NO=[]
k=[]
c=2
for i in range(len(fnames)):
    NO.append([])
    k.append([])
    f=open(fnames[i],'r')
    for l,line in enumerate(f):
         if ((l-Ny)%(2*Ny+1) == 0):
               line=line.strip()
               line=line.split(" ")
               k[i].append(float(line[0]))
               print(line[1])
               if i>=2*num_nh:
                   c=3
               NO[i].append(float(line[c]))
    f.close()
#print(k)
#print(NO)
fs=14
fig=plt.figure(figsize=(3,4))
plt.xlabel('$q_{x}/2\\pi$',fontsize=fs-2)
plt.ylabel(r'$n_{\uparrow}(q_{x},0)$',fontsize=fs-2)
#plt.grid(alpha=0.6)
color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
style=['-',':','--','-.']
mark=['o','s','^','*']
for i in range(int(len(fnames)/num_samples)):
    plt.plot(k[i],NO[i], marker=mark[i],linewidth=1,c=color[i],linestyle='-',markersize=3,label='$n_{h}=$'+str(nh[i]))
    plt.plot(k[i+int(len(fnames)/num_samples)],NO[i+int(len(fnames)/num_samples)], marker=mark[i],linewidth=1,c=color[i],linestyle=':',markersize=3)
    plt.plot(k[i+2*int(len(fnames)/num_samples)],NO[i+2*int(len(fnames)/num_samples)], marker=mark[i],linewidth=1,c=color[i],linestyle='--',markersize=3)
plt.legend(fontsize=8,framealpha=0,loc=(0.625,0.71))#,loc='upper right')#loc=(-0.016,0.76)
plt.yticks([0.0,0.1, 0.2,0.3, 0.4,0.5, 0.6,0.7, 0.8], ['0.0','', '0.2','', '0.4','', '0.6','', '0.8'])
plt.xticks([-1.0,-0.75,-0.5,-0.25, 0.0,0.25,0.5,0.75,1.0], ['-1.0','', '-0.5','', '0.0','', '0.5','', '1.0'])
plt.text(-0.84,0.76,'6$\\times$6',fontsize=10)
plt.text(-0.95,0.68,'-  10$\\times$6 \n',fontsize=10)#n $\cdot$$\cdot$ 12$\\times$6',fontsize=10)
plt.text(-0.9,0.72,'-',fontsize=10)
plt.text(-0.99,0.68,'$\cdot$$\cdot$ 12$\\times$6',fontsize=10)
x=[-0.95,-0.9]
cc=0.775
y=[cc,cc]
#plt.xlim(-1,1)
plt.plot(x,y,c='black',lw=0.9)
plt.savefig("fig_slinecuts.pdf",dpi=300,bbox_inches='tight')
#plt.show()
