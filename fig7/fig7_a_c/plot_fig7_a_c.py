from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import matplotlib
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import re
from matplotlib.patches import FancyArrowPatch
from pathlib import Path
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec

folder=Path('.')



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

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"]  = 42
print('no inputs')

Nx = 6# int(sys.argv[1])
Ny = 6#int(sys.argv[2])
num = 4#int(sys.argv[3])
fnames=[]
fnames_temp=[]
nh=[]
for f in folder.rglob('*.txt'):
    if f.is_file() and str(Nx)+'x'+str(Ny) in f.name and 'Sq' in f.name:
        fnames_temp.append(str(f))

for f in folder.rglob('*.txt'):
    if f.is_file() and str(Nx)+'x'+str(Ny) in f.name and 'occ' in f.name and 'inf' in f.name:
        fnames_temp.append(str(f))

for f in folder.rglob('*.txt'):
    if f.is_file() and str(Nx)+'x'+str(Ny) in f.name and 'occ' in f.name and 'U0' in f.name:
        fnames_temp.append(str(f))
#print(fnames_temp)

for i in range(3):
    Nh_temp=[]
    for j in range(num):
        match = re.search(r'(\d+)h', fnames_temp[j+i*num])
        Nh_temp.append(int(match.group(1)))
    ind = np.argsort(Nh_temp)
    #print(ind)
    for l in ind:
        fnames.append(fnames_temp[l+i*num])

#print(fnames)
#num = int(len(fnames)/3)
N = Nx*Ny

nh = []
'''
if sys.argv[3]=='bulk':
    if Nx <= 6 :
        N = N - 2*Ny
        Nx = Nx-2*Ny
    else:
        N = N - 4*Ny
        Nx = Nx-4*Ny
'''


nn=4
#N = Nx*Ny
#print("N",N)
KX=[]
KY=[]
SS=[]
for i in range(num):
    fname = fnames[i]
    KX.append([])
    KY.append([])
    SS.append([])
    f=open(fname,'r')
    for l,line in enumerate(f):
         line=line.strip()
         line=line.split(" ")
         if l == 0:
             Nh = int(line[1])
             nh.append(round(Nh/N,3))
             #max_sq = float(line[2])
         else:
             KX[i].append(round(float(line[0]),5))
             KY[i].append(round(float(line[1]),5))
             SS[i].append(round(float(line[4]),5)) #3 for SZ or 4 for Stot
    f.close()
kx=[]
ky=[]
SSF=[]
for i in range(num):
    kx.append([])
    ky.append([])
    SSF.append([])
    kx[i] = np.reshape(KX[i],(2*2*Nx+1,2*2*Ny+1))
    ky[i] = np.reshape(KY[i],(2*2*Nx+1,2*2*Ny+1))
    SSF[i] = np.reshape(SS[i],(2*2*Nx+1,2*2*Ny+1))

KXo=[]
KYo=[]
OCC=[]
for i in range(num):
    fname = fnames[i+num]
    KXo.append([])
    KYo.append([])
    OCC.append([])
    f=open(fname,'r')
    for l,line in enumerate(f):
         line=line.strip()
         line=line.split(" ")
         #if l == 0:
             #Nh = int(line[1])
             #nh.append(round(Nh/N),3)
             #max_sq = float(line[2])
         #else:
         KXo[i].append(round(float(line[0]),5))
         KYo[i].append(round(float(line[1]),5))
         OCC[i].append(round(float(line[2]),5))
         #if i==2:
             #print(line[0],line[1],line[2])
    f.close()
#print(len(OCC[0]))
#print(len(OCC[1]))
#print(len(OCC[2]))
kxo=[]
kyo=[]
occ=[]
for i in range(num):
    kxo.append([])
    kyo.append([])
    occ.append([])
    kxo[i] = np.reshape(KXo[i],(2*2*Nx+1,2*2*Ny+1)) #2*Nx+1,2*Ny+1
    kyo[i] = np.reshape(KYo[i],(2*2*Nx+1,2*2*Ny+1))
    occ[i] = np.reshape(OCC[i],(2*2*Nx+1,2*2*Ny+1))    



KXo0=[]
KYo0=[]
OCC0=[]
for i in range(num):
    fname = fnames[i+num*2]
    KXo0.append([])
    KYo0.append([])
    OCC0.append([])
    f=open(fname,'r')
    for l,line in enumerate(f):
         line=line.strip()
         line=line.split(" ")
         KXo0[i].append(float(line[0]))
         KYo0[i].append(float(line[1]))
         OCC0[i].append(float(line[2]))
    f.close()
kxo0=[]
kyo0=[]
occ0=[]
for i in range(num):
    kxo0.append([])
    kyo0.append([])
    occ0.append([])
    kxo0[i] = np.reshape(KXo0[i],(2*nn*Nx+1,2*nn*Ny+1))
    kyo0[i] = np.reshape(KYo0[i],(2*nn*Nx+1,2*nn*Ny+1))
    occ0[i] = np.reshape(OCC0[i],(2*nn*Nx+1,2*nn*Ny+1))

#vx=1.85 #for all
vx=1.53 #for bulk
vn=0.01
vx2=0.97

if Nx==12:
    #vx=1.96 #all
    vx=1.73 #bulk
    #vx=0.73 #sz
    vn=0.03
    vx2=0.99
#---------------------------------------------------------------------------------------------------------
Nx=[6,6,12]
Ny=[6,6,6]

nh2=[]
sq_max=[]
sK=[]
sM=[]
sM2=[]

#---------------------------------------------------------------------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#PLOT STATIC STRUCTURE FACTOR OVER THE K SPACE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
nrows=3
#print('num',num)
ncols=num
sx=0
sy=0
offx=0.0
if num==3:
    offx=0.65
    sx=5
    sy=5
elif num==4:
    offx=0.68
    sx=6.67
    sy=5
#fig,ax = plt.subplots(nrows=3, ncols=num,sharey=True,subplot_kw={'xticks': [-1,-0.5,0,0.5,1.0], 'yticks': [-1,-0.5,0,0.5,1.0]},figsize=(sx,sy))
fig= plt.figure(figsize=(10,7)) #17,5.7
plt.subplots_adjust(wspace=0.1, hspace=-0.3)
gs = gridspec.GridSpec(3, 5, width_ratios=[1.5,1.5,1.5,1.5,1.5])
ax=[]
plt.rcParams.update({
    #"font.family": "serif",
    #"font.serif": ["Times New Roman"],
    "font.size": 24,
    #'axes.titlesize': 16,     # title size
    'axes.labelsize': 14,     # x/y label size
    'xtick.labelsize': 14,    # x tick size
    'ytick.labelsize': 14,    # y tick size
    'legend.fontsize': 13,    # legend font
    })
for n in range(3):
       for m in range(4):
              ax.append(fig.add_subplot(gs[n, m]))
gx=22
gy=12
norm = mcolors.Normalize(vmin=0,vmax=vx)
for i in range(num):
     im1 = ax[i].contourf(kx[i],ky[i],SSF[i],300,cmap=plt.cm.gist_heat, norm=norm)#vmax=vx, vmin=0.0) #vn,extent=[-1, 1, -1, 1] 
     ax1_divider = make_axes_locatable(ax[i])
     im10 = ax[0].contourf(kx[0],ky[0],SSF[0],300,cmap=plt.cm.gist_heat ,norm = norm)# vmax=vx, vmin=0.0)
     ax10_divider = make_axes_locatable(ax[0])
     #for im in im1.collections:
     #       im.set_edgecolor("face")
     im1.set_edgecolor("face")
     im1.set_linewidth(0.0)
     im1.set_rasterized(True)
     ax[i].axis('equal')
     ax[i].set_ylim([-1,1])
     ax[i].set_xlim(-1,1)
     #ax[i].autoscale_view()
     ax[i].set_aspect('equal', adjustable='box')
     #ax[i].set_aspect('auto')
     #===========================================================================================================
     ax2_divider = make_axes_locatable(ax[i+4])
     im2 = ax[i+4].scatter(kxo[i].flatten(),kyo[i].flatten(),c=occ[i].flatten(),marker='h',cmap='Reds',s=((occ[i].flatten())**1)*60)#plt.cm.gist_heat)
     im2.set_edgecolor("face")
     ax[i+4].axis('equal')
     ax[i+4].set_aspect('equal', adjustable='box')
     #ax[i+8].set_aspect('equal', adjustable='box')
     ax[i+4].set_ylim(-1,1)
     ax[i+4].set_xlim(-1,1)
     #ax[i+4].autoscale_view()
     #ax[i+4].set_aspect('auto')
     #im2 = ax[i+4].contourf(kxo[i],kyo[i],occ[i],300,cmap=plt.cm.gist_heat, vmin=0,vmax=0.98)
     #==========================================================================================================
     ax3_divider = make_axes_locatable(ax[i+8])
     im3 = ax[i+8].scatter(kxo0[i].flatten(),kyo0[i].flatten(),c=occ0[i].flatten(),marker='h',cmap='Reds',s=((occ0[i].flatten())**1)*60)#plt.cm.gist_heat) #s=((occ0[i].flatten())**1)*100
     #ax[i+8].set_ylim(-1,1)
     #ax[i+8].set_xlim(-1,1)
     #ax[i+8].autoscale_view()
     im3.set_edgecolor("face")
     ax[i+8].axis('equal')
     ax[i+8].set_aspect('equal', adjustable='box')
     ax[i+8].set_xlim([-1, 1])
     ax[i+8].set_ylim([-1, 1])
     #ax[i+8].set_aspect('equal', adjustable='box')
     #ax[i+8].set_aspect('auto')
     #im3 = ax[i+8].contourf(kxo0[i],kyo0[i],occ0[i],300,cmap=plt.cm.gist_heat , vmin=0,vmax=0.98)
#========================color bar=======================================

cax1 = fig.add_axes([0.75, ax[3].get_position().y0+0.06, 0.009, 0.20])
tick1 = [0.00, round((np.min(SSF[0]) + np.max(SSF[0])) / 2, 2), round(np.max(SSF[0]), 2)-0.01]
cb1 = fig.colorbar(im10, cax=cax1, orientation='vertical', ticks=tick1)
cb1.ax.tick_params(labelsize=14)

cax3 = fig.add_axes([0.75, ax[11].get_position().y0+0.19, 0.009, 0.20])
tick3 = [0, round((np.min(occ0[num-1]) + np.max(occ0[num-1])) / 2, 2), round(np.max(occ0[num-1]), 2)-0.01]
cb3 = fig.colorbar(im3, cax=cax3, orientation='vertical', ticks=tick3)
cb3.ax.tick_params(labelsize=14)
#=======================================================================
#for i in range(12):
#ax[i].set_frame_on(False)
#========================================================================
#corners of hexagonal BZ
coord=[[2.0/3,0],[1.0/3,-1.0/np.sqrt(3)],[-1.0/3,-1.0/np.sqrt(3)],[-2.0/3,0],[-1.0/3,1.0/np.sqrt(3)],[1.0/3,1.0/np.sqrt(3)]]
bonds=[[1,2],[2,3],[3,4],[4,5],[5,6],[6,1]]

for j,bond in enumerate(bonds):
    site1=bond[0]-1
    site2=bond[1]-1
    for r in range(12):
            ax[r].set_ylim(-1, 1)
            ax[r].tick_params(labelbottom=False, labelleft=False, bottom=False, left=False) 
            ax[r].plot([coord[site1][0],coord[site2][0]],[coord[site1][1],coord[site2][1]],lw=0.9,c='y',linestyle='--')

fig.canvas.draw()
y_line = 0.845
fig_width = fig.get_figwidth()
for i in range(num):
    bbox = ax[i].get_position()
    x_center = (bbox.x0 + bbox.x1) / 2
    fig.text(x_center,y_line+0.012, f'{nh[i]:.3f}',ha='center',va='bottom',fontsize=18)
    fig.text(x_center, y_line, '|', ha='center', va='center', fontsize=18,rotation=90)
fig.lines.append(plt.Line2D([ax[0].get_position().x0+0.02, (ax[3].get_position().x1)-0.005],[y_line, y_line], transform=fig.transFigure, color='black'))
#=============================================================================================
ax_annotate = fig.add_axes([0, 0, 1, 1], zorder=-1)
ax_annotate.axis('off')

# Draw full ray as arrow
start_x = ax[0].get_position().x0+0.011
end_x = ax[3].get_position().x1

ax_annotate.annotate(
    '',
    xy=(end_x+0.0, y_line),        # arrow tip
    xytext=(start_x, y_line),  # arrow tail
    xycoords='figure fraction',
    textcoords='figure fraction',
    arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
)
#=================================================================================================
#ax[0][0].set_ylabel(r'$q_y/2\pi$',rotation=90, position=(-1,0.5),fontsize = 12)
#ax[1][0].set_ylabel(r'$q_y/2\pi$',rotation=90, position=(-1,0.5),fontsize = 12)
#plt.tight_layout()    
ax[0].set_ylabel(r'$U/t=\infty$',rotation=90, position=(-1,0.5),fontsize = 20.5)
ax[4].set_ylabel(r'$U/t=\infty$',rotation=90, position=(-1,0.5),fontsize = 20.5)
ax[8].set_ylabel(r'$U/t=0$',rotation=90, position=(-1,0.5),fontsize = 20.5)
plt.text(0.12,y_line+0.015,'$n_{h}$',fontsize = 24)
#ax[0].text(-0.12,0.00,r'$\Gamma$',fontsize = 16,color='w')
#ax[0].text(-0.12,1/np.sqrt(3),'$M_{1}$',fontsize = 14,color='w')
#ax[0].text(1/3,1/np.sqrt(3),r'$K$',fontsize = 14,color='w')
#ax[0].text(0.5,1/(2*np.sqrt(3)),r'$M_{2}$',fontsize = 14,color='w')
#plt.subplots_adjust(wspace=0.0)
#=========================================================================
'''
fig.canvas.draw()
x_line = 0.95
#fig_len = fig.get_figlength()
fig.text(x_line+0.028,0.5+0.01, r'$U = \infty$',rotation=90,ha='center',va='bottom',fontsize=18)
fig.text(x_line-0.013,ax[0][-1].get_position().y1+0.065 , '_', ha='center', va='center', fontsize=20)
fig.text(x_line-0.0118,ax[1][-1].get_position().y0-0.018 , '_', ha='center', va='center', fontsize=20)
fig.lines.append(plt.Line2D([x_line, x_line], [ax[0][-1].get_position().y1+0.04, ax[1][-1].get_position().y0-0.04],transform=fig.transFigure, color='black'))
'''
#==========================================================================
#ax[13].set_ylabel('Spin structure factor',fontsize=24)
#ax[12].text(-0.073,0,'$S(\\vec{q})$',fontsize=24,rotation=90)
#'Spin structure factor',fontsize=24,rotation=90)
#plt.text(0.55,y_line+0,'$n_{h}$',fontsize = 24)

plt.text(0.075,0.8,'(a)',fontsize=18)#,style='italic')
#plt.text(0.518,0.8,'(d)',fontsize=22,style='italic')
plt.text(0.075,0.58,'(b)',fontsize=18)#,style='italic')
plt.text(0.075,0.35,'(c)',fontsize=18)#,style='italic')
#---------------------------------------------------------
ax[3].text(0.2,0.6,'$S(\\vec{q})$',c='y',fontsize=16)
ax[7].text(0.2,0.6,'$n_{\\sigma}(\\vec{q})$',c='y',fontsize=16)
ax[11].text(0.2,0.6,'$n_{\\sigma}(\\vec{q})$',c='y',fontsize=16)

'''
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 24,
    #'axes.titlesize': 16,     # title size
    'axes.labelsize': 14,     # x/y label size
    'xtick.labelsize': 12,    # x tick size
    'ytick.labelsize': 12,    # y tick size
    'legend.fontsize': 20,    # legend font
    })
'''


#ax[12].set_ylim([0.21,1.99])
#ax[13].set_ylim([0.21,1.99])

#---------------------------------------------------------
plt.savefig("figs6x6.pdf",dpi=300,bbox_inches='tight',pad_inches=0.0)

#plt.show()
