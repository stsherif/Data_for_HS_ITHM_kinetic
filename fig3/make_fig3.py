import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import math
import matplotlib.pyplot as plt
import sys
import os
import matplotlib.gridspec as gridspec
from pathlib import Path
import re
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
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
#import matplotlib as mpl

#mpl.rcParams["text.usetex"] = False  # disable LaTeX, use mathtext


nh = []
Nx=[6,12]
Ny=[6,6]
N=[36,72]
num_hole_con=[]
num_en=[]
en_dmrg=[]
en_free=[]
en_freen=[]
en_freez=[]
er_en_freez=[]
hole_con=[]
ff=['summary_sample_6x6.txt','summary_sample_12x6.txt']
for s in range(len(Nx)):
    num_hole_con.append([])
    num_en.append([])
    g=open('GS_energy_xc_'+str(Nx[s])+'x'+str(Ny[s])+'.txt','r')
    for l,line in enumerate(g):
        if l>0:
            line=line.strip()
            line=line.split(" ")
            num_hole_con[s].append(float(line[0]))
            num_en[s].append(float(line[1]))


    fnames=["sorted_energy_U0_"+str(Nx[s])+"x"+str(Ny[s])+"_in_the_first_zone"]

    en_dmrg.append([])
    en_free.append([])
    en_freen.append([])
    en_freez.append([])
    er_en_freez.append([])
    hole_con.append([])
    for q in range(len(fnames)):
        energy_sorted=[]
        name = fnames[q]
        f=open(name,'r')
        for l,line in enumerate(f):
            line=line.strip()
            line=line.split(" ")
            if(l>0):
                 energy_sorted.append(float(line[0]))  
        for p in range(0,N[s],2):
            delta = (N[s]-p)/N[s]
            hole_con[s].append(delta)
            free_energy=0.0
            for i in range(int(p/2)):
                 free_energy += 2*energy_sorted[i]
            en_free[s].append(free_energy)
            en_freen[s].append(free_energy*delta)
            #print("here",delta,N[s]-p,free_energy)
                

    zfiles=[ff[s]]

    for q in range(len(zfiles)):
                   nh.append([])
                   z = []
                   er_z =[]

                   name = zfiles[q]
                   f=open(name,'r')
                   for l,line in enumerate(f):
                         line=line.strip()
                         line=line.split()#" ")
                         nh[s].append(float(line[0]))
                         z.append(float(line[1]))
                         er_z.append(float(line[2]))
                   for i in range(len(z)):
                         Np = N[s]-round(nh[s][i]*N[s])
                         if Np%2 ==1:
                            Np +=1
                         dn=0.0
                         for j in range(int(Np/2)):
                             dn += 2*energy_sorted[j]
                         #print(nh[s][i]," ",z[i])    
                         en_freez[s].append(dn*z[i])
                         er_en_freez[s].append(np.abs(dn)*er_z[i])
    print(z)
#print(nh[1])
#print(en_freez[1])

#-----------------------------------------------------------------------------------------------
folder=Path('.')
print('Provide inputs: no need')
fnames=[]
for f in folder.rglob('*.txt'):
    if f.is_file() and f.name and 'Nq' in f.name:
        fnames.append(str(f))
match = re.search(r'(\d+)x', fnames[0])
Nx_a = int(match.group(1))
match = re.search(r'x(\d+)', fnames[0])
Ny_a = int(match.group(1))
match = re.search(r'(\d+)h', fnames[0])
Nh_a = int(match.group(1))


fnames.append('a_erra_b_errb_vs_Nh_6x6_3points_0ky.txt')
fnames.append('a_vs_nh_10x6.txt')
fnames.append('a_erra_b_errb_vs_Nh_12x6_3points_0ky.txt')

ky=[]
NN=[]
kx=[]
num_of_xpnts = 1 + 2 * Nx_a
num_of_ypnts = 1 + 2 * Ny_a

f=open(fnames[0],'r')
for l,line in enumerate(f):
      if ((l-(Ny_a+1))%num_of_ypnts == 0):
            line=line.strip()
            line=line.split(" ")
            kx.append(float(line[0]))
            ky.append(float(line[1]))
            NN.append(float(line[2]))
f.close()
#-----------------------------------------------------------------------------------------------
N2=[]
nha=[]
alpha2=[]
Nx=[6,10,12]
Ny=[6,6,6]
for i in range(len(fnames)-1):
    nha.append([])
    alpha2.append([])
    ff=open(fnames[i+1],'r')
    for l,line in enumerate(ff):
            line=line.strip()
            line=line.split(" ")
            if l >= 0:
                if i == 0:
                    nha[i].append(float(line[0])/36)
                    print('here', float(line[0])/36)
                elif i == 2:
                    nha[i].append(float(line[0])/72)
                else:
                    nha[i].append(float(line[0]))
                alpha2[i].append(float(line[1]))
    ff.close()
err_files = ['6x6_energy_convergence_error.dat' , '10x6_energy_convergence_error.dat' , '12x6_energy_convergence_error.dat'] #['6x6_error.dat', '10x6_error.dat', '12x6_error.dat']
err = []
for fname in err_files:
    Nh_temp, Np_temp, err_temp, err_sq, err_N_sq = np.loadtxt(fname,unpack=True)
    err.append(err_N_sq)
print(len(err[0]),len(err[1]),len(err[2]))
#=------------------------------------------------------------------------------------------------------------
Nx2=[6,12]
Ny2=[6,6]
coord=[-20,-50]
fontz=60
fontz2=100
markz=20
labelz=50
fig= plt.figure(figsize=(30,30))
gs = gridspec.GridSpec(3,2, width_ratios=[1, 1.3],height_ratios=[1, 1, 2.0])
ax=[]
#plt.subplots_adjust(hspace=0)
ax.append(fig.add_subplot(gs[0:2, 0]))
tosharex=fig.add_subplot(gs[0, 1])
ax.append(tosharex)
ax.append(fig.add_subplot(gs[1, 1],sharex=tosharex))
ax.append(fig.add_subplot(gs[2, 0]))
ax.append(fig.add_subplot(gs[2, 1]))#,sharex=tosharex))
for i in range(2):
    ax[i+1].text(0.42,coord[i],"$N$  = " + str(Nx2[i])+'$\\times$'+str(Ny2[i]),fontsize=70)#,fontweight='bold')
    #ax[i+1].grid(alpha=0.7)

ax[1].scatter(num_hole_con[0],num_en[0],label="$U/t=\infty$",color='black',s=300)
ax[1].plot(hole_con[0],en_free[0],label="$U/t=0$",linestyle='dashed',color='red',linewidth=6)
ax[1].plot(hole_con[0],en_freen[0],linestyle='dotted',color='black',linewidth=6)
#ax[1].plot(nh[0],en_freez[0],linestyle='dashed',color="green",linewidth=6)
ax[1].errorbar(nh[0], en_freez[0], yerr=er_en_freez[0],c='green',fmt='s',ecolor='green',capsize=6,linestyle='--',linewidth=6)

x  = np.array(nh[0])
y  = np.array(en_freez[0])
errxy = np.array(er_en_freez[0])
ax[1].fill_between(x,y - errxy,y + errxy,color='green',alpha=0.3)

#ax[1].plot(hole_con[0],en_free[0]*(hole_con[0])**(1/4),label="sqrt",linestyle='dashed',color='C6',linewidth=6)

ax[2].scatter(num_hole_con[1],num_en[1],color='black',s=300)
ax[2].plot(hole_con[1],en_free[1],linestyle='dashed',color='red',linewidth=6)
ax[2].plot(hole_con[1],en_freen[1],label=" $n_{h}$",linestyle='dotted',color='black',linewidth=6)
#ax[2].plot(nh[1],en_freez[1],label="$Z$",linestyle='dashed',color="green",linewidth=6)
ax[2].errorbar(nh[1], en_freez[1], yerr=er_en_freez[1],c='green',fmt='s',ecolor='green',capsize=6,linestyle='--',linewidth=6,label="$Z$")

x  = np.array(nh[1])
y  = np.array(en_freez[1])
errxy = np.array(er_en_freez[1])
ax[2].fill_between(x,y - errxy,y + errxy,color='green',alpha=0.3)

ax[1].tick_params(labelsize=labelz)
ax[2].tick_params(labelsize=labelz)


nh = []
q = []
err = []
Nx=[6,10,12]
Ny=[6,6,6]
fnames=['summary_sample_6x6.txt','summary_sample_10x6.txt','summary_sample_12x6.txt']
for i in range(3):
    nh.append([])
    q.append([])
    err.append([])
    f=open(fnames[i],'r')
    for l,line in enumerate(f):
        elements = line.strip().split()
        line=line.strip()
        line=line.split()#" ")
        nh[i].append(float(line[0]))
        q[i].append(float(line[1]))
        err[i].append(float(line[2]))
    f.close()
#fig,ax=plt.subplots()
print(len(q[0]),len(q[1]),len(q[2]))
alph=[0.4,0.8,0.4]
colorintensity=[1,0.7,1]
color=['C0','C2','C1']
for i in range(3):
    q_arr = np.array(q[i])
    err_arr = np.array(err[i])
    nh_arr = np.array(nh[i])
    #ax[0].errorbar(nh[i], q[i],yerr=err[i],label="$N$ = " + str(Nx[i]) + r"$\times$" + str(Ny[i]),marker='o',markersize=markz,
    #alpha=colorintensity[i],c=color[i])#,capsize=3,linestyle='-')
    if i == 10:
        ax[0].plot(nh[i],q[i],label = "$N$ = "+ str(Nx[i])+'$\\times$'+str(Ny[i]),marker='o',markersize=markz,alpha=colorintensity[i],c=color[i])#+' and U = '+U[i])
    else:
        ax[0].errorbar(nh[i], q[i], yerr=err[i],label = "$N$ = "+ str(Nx[i])+'$\\times$'+str(Ny[i]),marker='o',markersize=markz,alpha=colorintensity[i],c=color[i],fmt='s',ecolor=color[i],capsize=4,linestyle='-')
        ax[0].fill_between(nh_arr, q_arr-err_arr, q_arr+err_arr, alpha=0.2,color=color[i])
ax[0].legend(fontsize=90)#, loc='lower right')

#fmt='s', color='#ff7f0e',ecolor='#ff7f0e', elinewidth=1.5, capsize=4,label='Sample 12x6 (Avg ± Error)', linestyle='-')

#print(nh)
#print(q)
ax[0].set_xlabel('$n_{h}$',fontsize=70)
ax[0].set_ylabel('$Z$',fontsize=85)
#ax[0].text(-0.26,0.4,'$Z$',fontsize=fontz,rotation=90)
#ax[0].set_ylabel('Quasiparticle Weight',fontsize=fontz)
#ax[0].text(-0.17,0.1,'Quasiparticle Weight',fontsize=fontz,rotation=90)
#plt.title(name_of_quantity+'_vs_nh')
#ax[0].grid(alpha = 0.7)
plt.xticks(np.arange(0, 1.0, 0.2),fontsize=fontz)
plt.yticks(np.arange(0, 0.9, 0.2),fontsize=fontz)
ax[0].set_yticks(np.arange(0,1,0.2))
ax[0].set_ylim(0.0,0.852)
ax[0].set_xlim(0,0.91)
ax[0].tick_params(labelsize=labelz)
plt.tight_layout()
#plt.text(-0.2,0.74,'(b)',fontsize=fontz)


#ax[2].set_xlabel("$n_{h}$",fontsize=28)
plt.text(-0.13,1.2,"$E_{\\rm{gs}}/t$",fontsize=70,rotation=90)
#ax[0].set_ylabel("Energy",fontsize=28)
ax[0].legend(loc='lower right',fontsize=70)#,loc='upper left')
ax[1].legend(ncol=1,loc='lower right',fontsize=50)
ax[2].legend(ncol=1,loc='lower right',fontsize=50)
#--------------------------------------------------------------------------
ax[3].plot(kx,NN,label='DMRG',markersize=markz, marker='o',linewidth=6,c='violet')

sub_kx=[]
sub_NN=[]
c=21
sub_kx=kx[c:-c]
sub_NN=NN[c:-c]
'''
for i in range(int((len(ky)/2))-3,(int(len(ky)/2))+4):
    sub_kx.append(kx[i])
    sub_NN.append(NN[i])
'''
print(sub_kx)
kx_fit=[]
for i in range(100):
    #kx_fit.append(-0.15+i*0.003)
    kx_fit.append(-0.3+i*0.003)
kx_fit.append(0.0)
for i in range(101,200):
    #kx_fit.append(-0.15+i*0.003)
    kx_fit.append(-0.3+i*0.003)


#fit function----------------------------- alpha |kx|-------------------------
def func(x, a):
        return a*abs(x)

param1, param_cov1 = curve_fit(func, sub_kx, sub_NN)
#print(param)
fit2 = []
for i in range(len(kx_fit)):
     fit2.append(func(kx_fit[i],param1[0]))
#print(fit2)
ax[3].plot(kx_fit,fit2,label='Linear Fit',linestyle='dashed',linewidth=6,c='navy') #($\\alpha$ = '+str(round(param1[0],3))+')'

#fit function----------------------------- beta kx^2-------------------------
def funcb(x, b):
        return b*x*x

param2, param_cov2 = curve_fit(funcb, sub_kx, sub_NN)
#print(param)
fit3 = []
kx_fit = kx_fit[37:-36]
for i in range(len(kx_fit)):
     fit3.append(funcb(kx_fit[i],param2[0]))
ax[3].plot(kx_fit,fit3,label='Quadratic Fit',linestyle='--',linewidth=6,c='indianred') #($\\beta$ = '+str(round(param2[0],3))+')'

ax[3].set_xlabel('$q_{x}/2\pi$',fontsize = 70)
ax[3].set_ylim(-0.002,0.13)
ax[3].text(-0.47,0.03,'$N(q_x,0)$',rotation=90, fontsize = 80)
'''
leg = ax.legend(
    loc='lower center',
    bbox_to_anchor=(0.3, 1.02),   # 0.5 centers it, 1.02 pushes it slightly above
    ncol=1,                       # Number of columns (adjust as needed)
    frameon=False,                  # Optional: no legend box
    fontsize=18                   # Optional: font size
)
'''
ax[3].legend(fontsize=50, loc='upper center')
#leg.get_frame().set_alpha(0)
#ax[3].grid(alpha=0.7)
ax[3].set_xlim(-0.31, 0.31)
ax[3].set_ylim(-0.0001, 0.101)
ax[3].text(0.072, 0.01, '$ N  = 24 \\times 4$', fontsize=60)#, fontweight='bold', color='black')
ax[3].text(0.11, 0.02, r'$n_h = 0.1$', fontsize=66, color='black')

# ✅ Correct way: set ticks, then control fontsize with tick_params
ax[3].set_xticks([-0.3,-0.15, 0.0, 0.15, 0.3])
ax[3].tick_params(axis='x', labelsize=labelz)
ax[3].set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.1])
ax[3].tick_params(axis='y', labelsize=labelz)

#--------------------------------------------------------------------------
for i in range(3):
    ax[4].plot(nha[i], alpha2[i], label=str(Nx[i])+'$\\times$'+str(Ny[i]),
               alpha=colorintensity[i], marker='o', markersize=markz,color=color[i])

ax[4].set_ylim(0, 0.75)
ax[4].set_xlim(-0.01, 0.94)
#ax[4].grid(alpha=0.7)
#ax[4].legend(fontsize=fontz)
ax[4].set_xlabel(r'$n_{h}$', fontsize=80)
ax[4].text(-0.14, 0.34, r'$\alpha$', rotation=90, fontsize=85)
#ax[4].set_ylabel('$MW$',fontsize = fontz)

# ✅ Same fix for ticks
#ax[4].set_yticks([0.0, 0.25, 0.50, 0.75 ,1.0])
ax[4].tick_params(axis='y', labelsize=fontz)
ax[4].set_xticks([0.0, 0.2, 0.4, 0.6, 0.8])
ax[4].tick_params(axis='x', labelsize=fontz)


#-----------------------------------------------------------------------------
pos = ax[1].get_position()
ax[1].set_position([pos.x0+0.01, pos.y0-0.03, pos.width, pos.height+0.03])
pos = ax[2].get_position()
ax[2].set_position([pos.x0+0.01, pos.y0, pos.width, pos.height+0.03])
pos = ax[4].get_position()
ax[4].set_position([pos.x0+0.01, pos.y0-0.0, pos.width, pos.height])
pos = ax[3].get_position()
ax[3].set_position([pos.x0, pos.y0-0.0, pos.width, pos.height])

ax[1].tick_params(axis='x', labelbottom=False)
ax[2].tick_params(axis='x', labelbottom=True)
ax[2].set_xlabel("$n_h$", fontsize=70)

ax[4].set_yticks([0.2, 0.4, 0.6])
ax[4].set_yticklabels(['0.2', ' 0.4', '0.6'])

ax[3].set_yticks([0.0, 0.02, 0.04,0.06, 0.08,0.1])
ax[3].set_yticklabels(['0.0',0.02, 0.04,'0.06 ', 0.08,'0.1'])


ax[4].axvspan(0.22, 0.30, color="lightgrey", alpha=0.5)
ax[4].axvspan(0.46, 0.51, color="lightgrey", alpha=0.5)
#for a in ax:
#    a.tick_params(axis='both', labelsize=60)
for a in ax:
    a.tick_params(axis='both',
                  which='major',
                  length=20,   # longer major ticks
                  width=4,     # thicker line
                  direction='inout',
                  labelsize=65,
                  top=False,   # remove top ticks
                  right=False) # remove right ticks
    a.tick_params(axis='both',
                  which='minor',
                  length=10,
                  width=3,
                  direction='inout',
                  top=False,
                  right=False)
#____________________________________________________________________________
plt.rcParams.update({
    "text.usetex": False})
plt.text(-1.15, 1.65, '(a)', fontsize=70)
plt.text(-0.13, 1.65, '(b)', fontsize=70)
plt.text(-1.15, 0.69, '(c)', fontsize=70)
plt.text(-0.13, 0.7, '(d)', fontsize=70)
ax[4].text(-0.03, 0.15, '      Hole ',
           fontsize=60, color='black')#, zorder=10)
ax[4].text(-0.1, 0.08, '       dominated',
           fontsize=60, color='black')#, zorder=10)

ax[4].text(0.6, 0.34, '    Particle',
           fontsize=60, color='black', zorder=10)
ax[4].text(0.57, 0.28, '   dominated',
           fontsize=60, color='black', zorder=10)

ax[4].text(0.36, 0.2, '    Intermediate', rotation = 90,
           fontsize=60, color='black', zorder=10)


"""
inax = inset_axes(ax[4], width="30%", height="30%", loc='lower right')
print('here', nhx)
print(aax)
inax.grid(alpha=0.7)
inax.set_ylim(0.0, 0.78)
inax.set_yticks([0.2, 0.4, 0.6])
inax.text(0.22, 0.4, 'Periodic direction', fontsize=20)
inax.set_yticklabels(['0.2', '0.4', '0.6'])
ccl = ['#1f77b4', '#2ca02c']
for i in range(2):
    inax.plot(nhx[i], aax[i], marker='o', c=ccl[i])  # ,markersize=markz)
"""
#____________________________________________________________________________
#-----------------------------------------------------------------------------


plt.savefig("fig3.pdf", dpi=300, bbox_inches='tight')

#plt.show()

