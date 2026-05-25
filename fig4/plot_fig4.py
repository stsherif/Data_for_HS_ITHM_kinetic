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
Nx=[6,12]
Ny=[6,6]
nh=[0.11,0.11]
N=[24,48]

fnames=['S_one_site_bulk_K_selected_6x6_4Nh.dat','S_one_site_bulk_K_selected_12x6_8Nh.dat','NN_SS_6x6_4Nh_bulk.dat','NN_SS_12x6_8Nh_bulk.dat','NNN_SS_6x6_4Nh_bulk.dat','NNN_SS_12x6_8Nh_bulk.dat','U_d_dbulk_6x6_4h.txt','U_d_dbulk_12x6_8h.txt']
err_sk=[]

for i in range(2):
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
for i in range(4):
    sisj.append([])
    err_nn.append([])
    f=open(fnames[i+2],'r')
    for l,line in enumerate(f):
        if l>0:
             elements = line.strip().split()
             line=line.strip()
             line=line.split(" ")
             if line[0] == '0' or line[0] == '0.0':
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

d=[]
d_bulk=[]
for i in range(2):
    d.append([])
    d_bulk.append([])
    f=open(fnames[i+6],'r')
    for l,line in enumerate(f):
        if l>0:
             elements = line.strip().split()
             line=line.strip()
             line=line.split(" ")
             if line[0] == '0' or line[0] == '0.0':
                 continue
             if line[0] == 'inf':
                  d[i].append(float(line[1]))
                  d_bulk[i].append(float(line[2]))
             else:
                 d[i].append(float(line[1]))
                 d_bulk[i].append(float(line[2]))
    f.close()
a, b, c = np.polyfit(U[1][-3:],d_bulk[1][-3:],2)
xfit1 = np.linspace(min(U[1]), max(U[1]), 100)
yfit1 = a * xfit1 * xfit1 + b * xfit1 + c
#-----------------------------------------------------
fs=38
ms=11
ls=40
az=1
fig=plt.figure(figsize=(24,16)) #14,13
fig.subplots_adjust(hspace=0.1,wspace=0.31) 
gs = gridspec.GridSpec(2, 2)
ax=[]
toshare1=fig.add_subplot(gs[0, 0])  # Top-left
ax.append(toshare1)
ax.append(fig.add_subplot(gs[0, 1],sharex=toshare1))
toshare2=fig.add_subplot(gs[1, 0])  # Top-left
ax.append(toshare2)
ax.append(fig.add_subplot(gs[1, 1],sharex=toshare2))

#ax[2].plot(U[0],sk[0],label=str(Nx[0])+'x'+str(Ny[0]), marker='o', linestyle='-',markersize=ms,alpha=az)#,color='#1f77b4'
#ax[2].plot(U[1],sk[1], label=str(Nx[1])+'x'+str(Ny[1]),marker='o', linestyle='-',markersize=ms,alpha=az)
ax[2].errorbar(U[0],sk[0],yerr=err_sk[0],label=str(Nx[0])+'x'+str(Ny[0]), marker='o', linestyle='-',markersize=ms,alpha=az,fmt='s',capsize=6)
ax[2].errorbar(U[1],sk[1],yerr=err_sk[1],label=str(Nx[1])+'x'+str(Ny[1]), marker='o', linestyle='-',markersize=ms,alpha=az,fmt='s',capsize=6)


ax[2].text(-0.036,0.042,'$S(\mathbf{K})/N$',fontsize=fs+5,color='black',rotation=90)

ax[2].tick_params(axis='x', labelsize=ls)
ax[2].tick_params(axis='y', labelsize=ls)
ax[0].tick_params(axis='x', labelsize=ls)
ax[0].tick_params(axis='y', labelsize=ls)
cclor=['#1f77b4', '#ff7f0e']
#-----------------------------------------------------------------------------------
for i in range(2):
    ax[0].plot(U[i],sisj[i], marker='o', linestyle='-',label=str(Nx[i])+'$\\times$'+str(Ny[i]),markersize=ms,alpha=az)
    ax[1].plot(U[i],sisj[i+2],marker='o', linestyle='-',label=str(Nx[i])+'x'+str(Ny[i]),markersize=ms,alpha=az)

ax[0].set_ylabel('$\\frac{1}{N_{bonds}}  \displaystyle\\sum_{\\langle i,j\\rangle} \\langle \\vec{S}_{i} \cdot \\vec{S}_{j}\\rangle$',fontsize=fs+3)
ax[1].set_ylabel('$\\frac{1}{N_{bonds}}  \displaystyle\\sum_{\\langle\\langle i,j\\rangle\\rangle} \\langle \\vec{S}_{i} \cdot \\vec{S}_{j}\\rangle $',fontsize=fs+3)

ax[0].legend(fontsize=fs+2,ncol=2,loc='upper left')
ax[0].tick_params(axis='x', labelsize=ls)
ax[0].tick_params(axis='y', labelsize=ls)
ax[1].tick_params(axis='x', labelsize=ls)
ax[1].tick_params(axis='y', labelsize=ls)
#-----------------------------------------------------------------------------------
for i in range(2):
    ax[3].plot(U[i],d_bulk[i], marker='o', linestyle='-',markersize=ms,alpha=az)#,color='#2ca02c')

line1, = ax[3].plot(xfit1,yfit1,alpha=az,color='black', linestyle='--',label = "Quadratic fit")
ax[3].legend([line1], ["Quadratic fit"], fontsize=fs+2, frameon=False)
y=[0,0.04]
ax[3].tick_params(axis='x', labelsize=ls)
ax[3].tick_params(axis='y', labelsize=ls)
ax[3].text(0.03,0.03,"$U_{c}/t \\simeq 50 $",fontsize=fs+9)#, style='italic')#str(Uintercept)

ax[3].set_ylim(-0.005,0.041)

ax[2].set_xlabel('$t/U$',fontsize=fs+3)
ax[3].set_xlabel('$t/U$',fontsize=fs+3)
ax[3].set_ylabel(r'$\frac{1}{N} \displaystyle\sum_{i} \langle n_{i\uparrow}n_{i\downarrow}\rangle$', fontsize=fs+3)
#-----------------------------------------------------------------------------------
ax[0].tick_params(axis='x', labelbottom=False)
ax[1].tick_params(axis='x', labelbottom=False)

ax[2].set_xticks([0, 0.02,0.04,0.06,0.08,0.1])
ax[3].set_xticks([0, 0.02,0.04,0.06,0.08,0.1])
ax[0].axvspan(0.015, 0.035, color='grey', alpha=0.3)
ax[1].axvspan(0.015, 0.035, color='grey', alpha=0.3)
ax[2].axvspan(0.015, 0.035, color='grey', alpha=0.3)
ax[3].axvspan(0.015, 0.035, color='grey', alpha=0.3)

cc=3
ax[2].text(0.035,0.038,'Kinetic Frustration',fontsize=fs-cc,color='black') #-0.003,0.028
ax[2].text(0.041,0.032,'driven AFM',fontsize=fs-cc,color='black')#-0.015,0.0241
ax[1].text(0.036,0.064,'Superexchange',fontsize=fs-cc,color='black')#0.043,0.0385
ax[1].text(0.039,0.058,'driven AFM',fontsize=fs-cc,color='black')#0.032,0.0346

ax[2].annotate('',xy=(0.008,0.044),xytext=(0.038,0.035),arrowprops=dict(arrowstyle='->',linewidth=2))
plt.text(-0.18,0.087,'(a)',fontsize=fs+4)
plt.text(-0.0325,0.087,'(b)',fontsize=fs+4)
plt.text(-0.18,0.036,'(c)',fontsize=fs+4)
plt.text(-0.0325,0.036,'(d)',fontsize=fs+4)
plt.savefig('fig4.pdf',dpi=300,bbox_inches='tight')
#plt.show()

