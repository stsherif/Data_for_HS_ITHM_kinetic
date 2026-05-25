#import matplotlib
#matplotlib.use('agg')
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import math

color=['black', '#9467bd','#1f77b4','#8c564b', '#ff7f0e', '#2ca02c', '#d62728'] #'#8c564b' 4th     '#9467bd' 2nd
fig,ax=plt.subplots(1,2,figsize=(6,4),sharey=True)

sh1=[0.0,0.05,0.005,0.02,0.04,0.02,-0.015]
sh2=[0.0,-0.02,0.005,0.02,0.01,0.02,-0.015]
fnames1=['bulk_afm_op_N_nh_U_inf_MNB_MNS_1h.txt','bulk_afm_op_N_nh_U_inf_MNB_MNS_0.1.txt','bulk_afm_op_N_nh_U_inf_MNB_MNS_0.11.txt','bulk_afm_op_N_nh_U_inf_MNB_MNS_0.19.txt','bulk_afm_op_N_nh_U_inf_MNB_MNS_0.25.txt','bulk_afm_op_N_nh_U_inf_MNB_MNS_0.33.txt','bulk_afm_op_N_nh_U_inf_MNB_MNS_0.6.txt']
fnames2=['site_bulk_afm_op_N_nh_U_inf_MNB_MNS_1.txt','site_bulk_afm_op_N_nh_U_inf_MNB_MNS_0.1.txt','site_bulk_afm_op_N_nh_U_inf_MNB_MNS_0.11.txt','site_bulk_afm_op_N_nh_U_inf_MNB_MNS_0.19.txt','site_bulk_afm_op_N_nh_U_inf_MNB_MNS_0.25.txt','site_bulk_afm_op_N_nh_U_inf_MNB_MNS_0.33.txt','site_bulk_afm_op_N_nh_U_inf_MNB_MNS_0.6.txt']

l=['1 hole','$n_{h}=0.1$','$n_{h}=0.11$','$n_{h}=0.19$','$n_{h}=0.25$','$n_{h}=0.33$','$n_{h}=0.6$'] #'$n_{h}=0.19(0.183,0.194)$'
xb = np.arange(0,0.32,0.02)

nh=[]
N1=[]
N2=[]
MN_B1=[]
MN_B2=[]
for n in range(len(fnames1)):
    nh.append([])
    N1.append([])
    N2.append([])
    MN_B1.append([])
    MN_B2.append([])
    f=open(fnames1[n],'r')
    for i,line in enumerate(f):
        #if n==3:
            line=line.strip()
            line=line.split(" ")
            N1[n].append(1/np.sqrt(float(line[0])))
            nh[n].append(float(line[1]))
            MN_B1[n].append(float(line[3])) 
    f.close()
    ff=open(fnames2[n],'r')
    for i,line in enumerate(ff):
        #if n==3:
            line=line.strip()
            line=line.split(" ")
            N2[n].append(1/np.sqrt(float(line[0])))
            MN_B2[n].append(float(line[3]))
    ff.close()
    #if n !=3:
    #    continue
    ax[0].scatter(N1[n],MN_B1[n],label=l[n],c=color[n])
    ax[1].scatter(N2[n],MN_B2[n],label = l[n],c=color[n])

    mb ,cb = np.polyfit(N1[n], MN_B1[n], 1)
    MN_Bfit1 = mb *xb + cb

    ms ,cs = np.polyfit(N2[n], MN_B2[n], 1)
    MN_Bfit2 = ms *xb + cs
    ax[0].plot(xb,MN_Bfit1,linestyle='--',color=color[n],alpha = 0.3)#,markersize=10)
    ax[1].plot(xb,MN_Bfit2,linestyle='--',color=color[n],alpha = 0.3)#,markersize=8)
    ax[0].text(0,cb+sh1[n],str(round(cb,3)),c=color[n])
    ax[1].text(0,cs+sh2[n],str(round(cs,3)),c=color[n])


#plt.yticks(np.arange(0.0,0.5,0.05),[f"{t:.1f}" if t in [0.1, 0.2, 0.3, 0.4, 0.5] else '' for t in np.arange(0.0,0.5,0.05)])
fs=15
ax[0].set_ylabel('$M_{N}$',fontsize=fs)
ax[0].set_xlabel('$1/ \sqrt{N}$',fontsize=fs)
ax[1].set_xlabel('$1/ \sqrt{N}$',fontsize=fs)
#plt.ylim([0.05,0.5])
ax[0].grid(alpha=0.15)
ax[1].grid(alpha=0.15)

ax[0].legend(ncol=1,fontsize=8,loc=(0.05,0.47))
ax[0].set_xlim([0,0.25])
ax[0].set_ylim([0,0.5])
ax[1].set_xlim([0,0.25])
ax[1].set_ylim([0,0.5])

plt.savefig("fig10.pdf",dpi=300,bbox_inches='tight')
#plt.show()

