import sys
sys.path.append("../../")
from bonds_n_coords import lat_bonds
from bonds_n_coords import coordinates
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import os
import numpy as np
from matplotlib.ticker import ScalarFormatter

#print('provide: power and scale center1 and center2')


from matplotlib import font_manager

font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/times.ttf")
font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/timesbd.ttf")
font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/timesi.ttf")
font_manager.fontManager.addfont("/mnt/c/Windows/Fonts/timesbi.ttf")
plt.rcParams.update({
     "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 24,
    #'axes.titlesize': 16,     # title size
    'axes.labelsize': 14,     # x/y label size
    'xtick.labelsize': 14,    # x tick size
    'ytick.labelsize': 14,    # y tick size
    'legend.fontsize': 13,    # legend font
    })
import matplotlib
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"]  = 42


p=3
#float(sys.argv[1])
sc=1000
#int(sys.argv[2])
#Nx=[12,9]
Nx=[6,6]
Ny = 6
#N = [72,54]
N=[36,36]
U='inf'
SiSj=[]
nh=[0.25,0.33]
center = [15,15]
SiSc=[]
site_num_for_c=[]
#fnames=['restfile12x6_Uinf_18h_pn9.txt','file9x6_xc_third_Uinf_pn8.txt']
fnames=['file6x6_Uinf_9h_pn2.txt','file6x6_Uinf_12h_pn2.txt']
bulk_bonds=[]
Rxy=[]
for ff in range(len(fnames)):
    ln = N[ff]*N[ff]
    SiSc.append([])
    site_num_for_c.append([])
    bulk_bonds.append([])
    Rxy.append([])
    cy_bond, op_bond = lat_bonds(Nx[ff],Ny)
    bonds=op_bond
    Rxy[ff] = coordinates(Nx[ff],Ny)
    for i in range(len(bonds)):
        if ((Nx[ff] <= 9 and (bonds[i][0] <= Ny or bonds[i][1] > N[ff]-Ny)) or (Nx[ff] > 9 and (bonds[i][0] <= 2*Ny or bonds[i][1] > N[ff]-2*Ny)) ):
            continue
        bulk_bonds[ff].append(bonds[i])
    command = "grep -A"+str(ln)+" \"i j <Si^z Sj^z>\" "+fnames[ff]+" > tmp"
    os.system(command)
    SS = [[],[],[],[],[]]
    SiSj.append([])
    f=open("tmp",'r')
    for l,line in enumerate(f):
          line=line.strip()
          line=line.split(" ")
          for n in range(len(op_bond)):
               if (l == (op_bond[n][0]-1)*N[ff]+op_bond[n][1]):
                   #line=line.strip()
                   #line=line.split(" ")
                   sitei = int(line[0])
                   sitej = int(line[1])
                   if (Nx[ff] <= 9 and (sitei <= Ny or sitej <= Ny or sitei > N[ff]-Ny or sitej > N[ff]-Ny)):
                         continue
                   if (Nx[ff] > 9 and (sitei <= 2*Ny or sitej <= 2*Ny or sitei > N[ff]-2*Ny or sitej > N[ff]-2*Ny)):
                         continue
                   #print(line[0],line[1])
                   SS[0].append(int(line[0]))
                   SS[1].append(int(line[1]))
                   SS[2].append(float(line[2]))
                   SS[3].append(float(line[3]))
                   SS[4].append(float(line[4]))
                   val = (float(line[2]) + 0.5 * float(line[3]) + 0.5 * float(line[4]))
                   SiSj[ff].append(np.abs(val))
                   #print(line[0],line[1],line[2],line[3],line[4],val)
          
          if l>(center[ff]-1)*N[ff] and l<=center[ff]*N[ff]:
                   #line=line.strip()
                   #line=line.split(" ")
                   sitei = int(line[0])
                   sitej = int(line[1])
                   if (Nx[ff] <= 9 and (sitei <= Ny or sitej <= Ny or sitei > N[ff]-Ny or sitej > N[ff]-Ny)):
                         continue
                   if (Nx[ff] > 9 and (sitei <= 2*Ny or sitej <= 2*Ny or sitei > N[ff]-2*Ny or sitej > N[ff]-2*Ny)):
                         continue
                   vall = (float(line[2]) + 0.5 * float(line[3]) + 0.5 * float(line[4]))
                   if l == (center[ff]-1)*N[ff] + center[ff] :
                       vall=0
                   SiSc[ff].append(vall)
                   site_num_for_c[ff].append(int(line[1]))
                   #print('hhh',line[0],line[1],line[2],line[3],line[4],vall)
          

    f.close()
Nbonds=[]
for i in range(len(fnames)):
      Nbonds.append(len(SiSj[i]))

'''
color=[]
for i in range(len(SiSj)):
    if (SiSj[i]-ss_avg) > 0:
        color.append('black')
    else:
        color.append('orange')
'''
#for i in range(len(SiSj)):
#color.append('red')

#sc=int(sys.argv[2])
#p=float(sys.argv[1])
ticks=[[(0.1**p)*sc,(0.2**p)*sc],[(0.05**p)*sc,(0.1**p)*sc]]
#print(color)
fig,ax = plt.subplots(1,len(fnames),figsize=(4,4), gridspec_kw={'width_ratios': [1,1.25]})  #,gridspec_kw={'width_ratios': [4, 8]})#, gridspec_kw={'width_ratios': [4, 7, 8]})figsize=(12,6)
plt.subplots_adjust(wspace=0.1)#, hspace=0.6)
#norm = plt.Normalize(vmin=sc*min(min(SiSj))**p, vmax=sc*max(max(SiSj))**p)
norm = [None] * len(fnames)
cmap = [None] * len(fnames)

# Set normalization and colormap
for i in range(len(fnames)):
    norm[i] = mcolors.Normalize(vmin=(0.0000017)*sc, vmax=(0.00224)*sc) # [i]  #min(SiSj)**p max(SiSj)**p
    cmap[i] = cm.Reds #Greys
    for k,bnd in enumerate(bulk_bonds[i]):
                  s1=bnd[0]
                  s2=bnd[1]
                  strength = (SiSj[i][k]**p)*sc
                  color = cmap[i](norm[i](strength))
                  ax[i].plot([Rxy[i][s1][0],Rxy[i][s2][0]],[Rxy[i][s1][1],Rxy[i][s2][1]],c=color,lw=1) #-ss_avg
    ax[i].axis("off")
    ax[i].axis("equal")
    sm = plt.cm.ScalarMappable(cmap=cmap[i], norm=norm[i])
    sm.set_array([])  # Needed for colorbar without imag
#from matplotlib.ticker import ScalarFormatter
cbar = plt.colorbar(sm, ax=ax[i], shrink=0.4)#, ticks=ticks[])
'''
fmt = ScalarFormatter(useMathText=True)
fmt.set_scientific(True)
fmt.set_powerlimits((0, 0))   # force scientific for all ticks
cbar.ax.yaxis.set_major_formatter(fmt)
cbar.update_ticks()
'''
#cbar.set_label("$|\\langle S_{i} \cdot S_{j} \\rangle|^{"+str(int(p))+"}$",fontsize=20)
#cbar.ax[0].set_yticklabels(['1e-3', '2e-3'])
#cbar.ax[1].set_yticklabels(['0.5e-3', '1e-3'])
plt.text(4.8,4.2,'$\\times 10^{-3}$',fontsize=8.5)
plt.text(-2.8,4.5,'(d)',fontsize=7.5,style='italic')
plt.text(1.5,4.5,'(e)',fontsize=7.5,style='italic')
#ax[0].text(Rxy[0][center[0]][0]-0.21,Rxy[0][center[0]][1]-0.15,'x',fontsize=13.5,c='black')
#ax[1].text(Rxy[1][center[1]][0]-0.22,Rxy[1][center[1]][1]-0.15,'x',fontsize=13.5,c='black')

#plt.text(-4.5,1.3,"$|\\langle S_{i} \cdot S_{j} \\rangle|^{"+str(int(p))+"}$",fontsize=20,rotation=90)
plt.text(5.8,1.8,"$|\\langle S_{i} \cdot S_{j} \\rangle|^{"+str(int(p))+"}$",fontsize=9.5,rotation=90)
plt.text(-2.1,4.5,'$n_{h}$ = '+str(nh[0]),fontsize=7.5)
plt.text(2.1,4.5,'$n_{h}$ = '+str(nh[1]),fontsize=7.5)
#-----------------------------------------------------------------------------------------------------------------
colorc=[[],[]]
for i in range(2):
    for j in range(len(SiSc[i])):
        if SiSc[i][j]>0:
            colorc[i].append('b')
        else:
            colorc[i].append('r')
#for i in range(2):
#    for j in range(len(SiSc[i])):
#         ax[i].scatter(Rxy[i][site_num_for_c[i][j]][0],Rxy[i][site_num_for_c[i][j]][1],s=np.abs(SiSc[i][j])*400,c=colorc[i][j],zorder=10)
#-----------------------------------------------------------------------------------------------------------------

plt.savefig('figsed_6x6.pdf',dpi=600,bbox_inches='tight')
#plt.show()

