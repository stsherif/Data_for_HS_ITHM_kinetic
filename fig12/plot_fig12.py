import numpy as np
import math
import matplotlib.pyplot as plt
import sys
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit

from matplotlib import font_manager
font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/times.ttf")
font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/timesbd.ttf")
font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/timesi.ttf")
font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/timesbi.ttf")
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 25,          # base font size
    "axes.labelsize": 24,
    "axes.titlesize": 26,
    "xtick.labelsize": 25,
    "ytick.labelsize": 25,
    "legend.fontsize": 25,
    "axes.linewidth": 1.2,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "grid.alpha": 0.5
})
import matplotlib
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"]  = 42

U=[]
sqmax=[]
sk=[]
sisj=[]
a=[]
fnames=[]
Nx=[6,6,6]
Ny=[6,6,6]
nh=[0.11,0.16,0.19]
N=[24,24,24]

fnames=['S_one_site_bulk_K_selected_6x6_4Nh.dat','S_one_site_bulk_K_selected_6x6_6Nh.dat','S_one_site_bulk_K_selected_6x6_7Nh.dat',
        'NN_SS_6x6_4Nh_bulk.dat','NN_SS_6x6_6Nh_bulk.dat','NN_SS_6x6_7Nh_bulk.dat']
err_sk=[]

for i in range(3):
    U.append([])
    sqmax.append([])
    sk.append([])
    err_sk.append([])
    f=open(fnames[i],'r')
    for l,line in enumerate(f):
        if l>=0:
             elements = line.strip().split()
             line=line.strip()
             line=line.split(" ")
             if line[0] == '0' or line[0] == '0.0':
                 continue
             if line[0] == '40' or line[0] == '40.0':
                 continue
             if line[0] == 'inf':
                  U[i].append(0) #0
                  sk[i].append(float(line[1])/N[i])
                  err_sk[i].append(float(line[2])/N[i])
             else:
                  U[i].append(1/float(line[0])) #1/
                  sk[i].append(float(line[1])/N[i])
                  err_sk[i].append(float(line[2])/N[i])
                  #sm.append(float(line[3]))

    f.close()
#--------------------------------------------------
err_nn=[]
for i in range(3):
    sisj.append([])
    err_nn.append([])
    f=open(fnames[i+3],'r')
    for l,line in enumerate(f):
        if l>=0:
             elements = line.strip().split()
             line=line.strip()
             line=line.split(" ")
             if line[0] == '0' or line[0] == '0.0':
                 continue
             if line[0] == '40' or line[0] == '40.0':
                 continue
             if line[0] == 'inf':
                  #U[i].append(1/float(line[0]))
                  sisj[i].append(float(line[1]))
                  err_nn[i].append(float(line[2]))
             else:
                 #U[i].append(1/float(line[0]))
                 sisj[i].append(float(line[1]))
                 err_nn[i].append(float(line[2]))
    f.close()

#-----------------------------------------------------

fs=38
ms=11
ls=40
az=1
fig, ax =plt.subplots(nrows=1, ncols=2,figsize=(24,8)) #14,13
#fig.subplots_adjust(hspace=0.1,wspace=0.31) 
fig.subplots_adjust(wspace=0.31)
for i in range(3):
    if i != 2:
        ax[1].errorbar(U[i],sk[i],yerr=err_sk[i], marker='o', linestyle='-',markersize=ms,alpha=az,fmt='s',capsize=6)
    else:
        ax[1].errorbar(U[i],sk[i],yerr=err_sk[i], marker='o', linestyle='-',markersize=ms,alpha=az,fmt='s',capsize=6,c='C2')
        ax[1].plot(U[i],sk[i], marker='o',label='$n_h=$'+str(nh[i]), linestyle='-',markersize=ms,alpha=az,c='C2')

ax[1].text(-0.031,0.055,'$S(\mathbf{K})/N$',fontsize=fs+5,color='black',rotation=90)

ax[1].tick_params(axis='x', labelsize=ls)
ax[1].tick_params(axis='y', labelsize=ls)
ax[0].tick_params(axis='x', labelsize=ls)
ax[0].tick_params(axis='y', labelsize=ls)
cclor=['C0', 'C1', 'C2']
#-----------------------------------------------------------------------------------
print(U,sisj)
for i in range(3):
    if i!= 2:
        #ax[0].errorbar(U[i],sisj[i],yerr=err_nn[i], marker='o',label='$n_h=$'+str(nh[i]), linestyle='-',markersize=ms,alpha=az,fmt='s',capsize=6)
        ax[0].plot(U[i],sisj[i], marker='o',label='$n_h=$'+str(nh[i]), linestyle='-',markersize=ms,alpha=az)
    else: 
        ax[0].plot(U[i],sisj[i], marker='o', linestyle='-',markersize=ms,alpha=az)
        #ax[0].errorbar(U[i],sisj[i],yerr=err_nn[i], marker='o', linestyle='-',markersize=ms,alpha=az,fmt='s',capsize=6)

ax[0].set_ylabel('$\\frac{1}{N_{bonds}} \displaystyle\\sum_{\\langle i,j\\rangle} \\langle \\vec{S}_{i} \cdot \\vec{S}_{j}\\rangle $',fontsize=fs+3)
#l=['$n_h = 0.11 $', '$n_h = 0.16$']
ax[0].legend(fontsize=fs-5,loc='upper left',ncols=2)
ax[1].legend(fontsize=fs-5,loc='upper right',ncols=2)
#-----------------------------------------------------------------------------------
ax[0].axvspan(0.015, 0.035, color='grey', alpha=0.3)
ax[1].axvspan(0.015, 0.035, color='grey', alpha=0.3)
ax[0].set_xticks([0, 0.02,0.04,0.06,0.08,0.1])
ax[1].set_xticks([0, 0.02,0.04,0.06,0.08,0.1])
plt.text(-0.068,0.04,'(a)',fontsize=fs+4)
plt.text(0.075,0.04,'(b)',fontsize=fs+4)
plt.savefig('fig12.pdf',dpi=300,bbox_inches='tight')
#plt.show()

