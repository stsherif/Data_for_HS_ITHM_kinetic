import numpy as np
import sys 
sys.path.append("../")
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import matplotlib.pyplot as plt
import os
from bonds_n_coords_diagonal import diagonal_lat_bonds
from bonds_n_coords_diagonal import coordinates

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#INPUT SYSTEM SIZES
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
Nx = 9 #input('Enter the number of sites along open boundary ')
Ny = 6  #input('Enter the number of sites along periodic boundary ')
Nx = int(Nx)
Ny = int(Ny)
N = Nx*Ny
terms=int(N*N)   #NUMBER OF DATA POINTS TO READ FROM EACH FILE
ln=terms
U='inf'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#READ THE DMRG OUTPUT FILE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fname = 'file9x6_dia_third_Uinf_pn12.txt' 
#sys.argv[1]
#["file6x6_Uinf_dia_8h_pn3.txt","file_6x6_diagonal_Uinf_12h_pn12.txt"]         #FILE NAME
Nh = 18
#int(sys.argv[2])
#[8,12]
#int(sys.argv[2]) 
#12
nh = round(Nh/N,2)
center = 21
command = "grep -A"+str(terms)+" \"i j <Si\" "+fname+" > temp" 
os.system(command)

SiSj = [[],[],[],[],[]]
f=open("temp",'r')
for l,line in enumerate(f):
    if (l>=1):
        line=line.strip()
        line=line.split(" ")
        sitei = int(line[0])
        sitej = int(line[1])
        if ((sitei <= Ny or sitej <= Ny or sitei > N-Ny or sitej > N-Ny)):
                continue
        #print(line[0], line[1], line[2], line[3], line[4])
        SiSj[0].append(int(line[0]))
        SiSj[1].append(int(line[1]))
        SiSj[2].append(float(line[2]))
        SiSj[3].append(float(line[3]))
        SiSj[4].append(float(line[4]))
        
f.close()

Nbulk=N-2*Ny
print(SiSj[0],SiSj[1])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#DEFINE LATTICE VECTORS (I have taken two sides of rhombus)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
a1 = [1,0]
a2 = [0.5,np.sqrt(3)/2]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#FIND X,Y COORDINATES OF EACH SITE CORRESPONDING TO THE LABEL
#WE HAVE IN DMRG
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Rxy = {} #initialize coordinate disctionary
for j in range(Ny,0,-1):
    for i in range(1,Nx+1):
        label = j + (i-1)*Ny
        if (j>1):
            Rxy[label] = (i-1)*np.array(a1)+(Ny%j)*np.array(a2)
        else:
            Rxy[label] = (i-1)*np.array(a1)-1*np.array(a2)
        #print(label,Rxy[label])    
        #plt.scatter(Rxy[label][0],Rxy[label][1],marker='o',c='red')
        #plt.axis('equal')
#plt.show()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#NOW HERE WE ARE READY TO CALCULATE STATIC STRUCTURE FACTOR
#FIRST MAKE K GRIDS FOR TRIANGULAR LATTICE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print(Rxy)
print(Rxy[21])
KX = []
KY = []

for n in range(-Nx,Nx+2):
    for m in range(-Ny-4,Ny+4):
        Kx = 1.0/Nx*n #in the unit of 2pi
        Ky = 1.0/np.sqrt(3)*(2.0/Ny*m-Kx)
        KX.append(Kx)
        KY.append(Ky)

#-----------COMPUTE STRUCTURE FACTOR---------------------------------
def str_fac(kx,ky,r,corr):
    SFxx_n_SFyy = 0
    SFzz = 0
    for i in range(len(corr[0])):
        index_i = corr[0][i]
        index_j = corr[1][i]
        szsz = corr[2][i]
        #sxsx = 0.5*(corr[3][i]+corr[4][i])
        sxx_n_syy = 0.5*(corr[3][i]+corr[4][i])
        r_ij = r[index_j]-r[index_i]
        #kr_ij = np.dot(k_vec,r_ij)
        kr_ij = kx*r_ij[0]+ky*r_ij[1]
        if (index_i==index_j):
            SFzz += szsz
            SFxx_n_SFyy += sxx_n_syy
        else:
            SFzz += np.cos(kr_ij*2*np.pi)*szsz
            SFxx_n_SFyy += np.cos(kr_ij*2*np.pi)*sxx_n_syy

    return (SFzz+SFxx_n_SFyy)/Nbulk#SFzz/N,0.5*SFxx/N

SSF=[]
for index_k in range(len(KX)):
    #print kx, ky, str_fac(kx,ky,Rxy,SiSj)
    ss =str_fac(KX[index_k],KY[index_k],Rxy,SiSj)
    SSF.append(ss)
    #Sfxx.append(sxx)
kx=np.reshape(KX,(2*(Nx+1),2*(Ny+4)))
ky=np.reshape(KY,(2*(Nx+1),2*(Ny+4)))
SSF=np.reshape(SSF,(2*(Nx+1),2*(Ny+4)))
#Sfzz=np.reshape(Sfzz,(2*(Nx+1),2*(Ny+4)))
#kx,ky = np.meshgrid(KX,KY)
 #Sfzz,Sfxx = str_fac(kx,ky,Rxy,SiSj)

SSkt = str_fac(2/3,0,Rxy,SiSj)
SStqp = str_fac(13/18,-1.0/(18*np.sqrt(3)),Rxy,SiSj)

skpoint= str_fac(2/3,0,Rxy,SiSj)
smpoint= str_fac(0,1.0/np.sqrt(3),Rxy,SiSj)
#--------------------------------------------------------------------------------------------
mxa=0
mya=(2*1)/(Ny*np.sqrt(3))
mxb=0
myb=(2*2)/(Ny*np.sqrt(3))
smpointa = str_fac(mxa,mya,Rxy,SiSj)
smpointb = str_fac(mxb,myb,Rxy,SiSj)
sm2point = 0.5*(smpointa+smpointb)
print('jjjjjjjjjjjjjjjjjjjjjjjj',smpointa,smpointb,sm2point)
#--------------------------------------------------------------------------------------------
sgamma = str_fac(0,0,Rxy,SiSj)
max_sq=0
#print(SSF)
for i in range(len(SSF)):
    temp=max(SSF[i])
    if (max_sq < temp):
        max_sq = temp
cy_bond, op_bond = diagonal_lat_bonds(Nx,Ny)
bonds=op_bond
Rxy2 = coordinates(Nx,Ny)

command = "grep -A"+str(ln)+" \"i j <Si^z Sj^z>\" "+fname+" > tmp"
os.system(command)
SS2 = [[],[],[],[],[]]
SiSj2 = []
SiSc=[]
site_num_for_c=[]

f=open("tmp",'r')
for l,line in enumerate(f):
    line=line.strip()
    line=line.split(" ")
    for n in range(len(op_bond)):
        if (l == (op_bond[n][0]-1)*N+op_bond[n][1]):
            sitei = int(line[0])
            sitej = int(line[1])
            if (Nx <= 9 and (sitei <= Ny or sitej <= Ny or sitei > N-Ny or sitej > N-Ny)):
                continue
            #print(line[0],line[1])
            SS2[0].append(int(line[0]))
            SS2[1].append(int(line[1]))
            SS2[2].append(float(line[2]))
            SS2[3].append(float(line[3]))
            SS2[4].append(float(line[4]))
            val = (float(line[2]) + 0.5 * float(line[3]) + 0.5 * float(line[4]))
            SiSj2.append(np.abs(val))
            #print(line[0],line[1],line[2],line[3],line[4],val)
    if l>(center-1)*N and l<=center*N:
            #print('jjjjjjjjjj',l)      
            #line=line.strip()
            #line=line.split(" ")
            sitei = int(line[0])
            sitej = int(line[1])
            #print(l,sitei,sitej)
            '''
            if (Nx <= 9 and (sitei <= Ny or sitej <= Ny or sitei > N-Ny or sitej > N-Ny)):
                         #print(l,sitei,'not taken')
                         continue
            if (Nx > 9 and (sitei <= 2*Ny or sitej <= 2*Ny or sitei > N-2*Ny or sitej > N-2*Ny)):
                         continue
            '''
            vall = (float(line[2]) + 0.5 * float(line[3]) + 0.5 * float(line[4]))
            if l == (center-1)*N + center :
                       vall=0
            SiSc.append(vall)
            #print('kkkkkkkkkkkkk',sitei,sitej,vall)
            site_num_for_c.append(int(line[1]))
        
f.close()



Nbonds=len(SiSj2)
print(Nbonds)
ss_avg=sum(SiSj2)/Nbonds
ss_max=max(SiSj2)
ss_min=min(SiSj2)
bulk_bonds=[]
for i in range(len(bonds)):
        if ((Nx <= 9 and (bonds[i][0] <= Ny or bonds[i][1] > N-Ny)) or (Nx > 9 and (bonds[i][0] <= 2*Ny or bonds[i][1] > N-2*Ny)) ):
            continue
        bulk_bonds.append(bonds[i])

sc= 1000
p= 3
fs=24
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#PLOT STATIC STRUCTURE FACTOR OVER THE K SPACE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#fig,(ax1,ax2) = plt.subplots(nrows=1, ncols=2,sharey=True,subplot_kw={'xticks': [-1,-0.5,0,0.5,1.0], 'yticks': [-1,-0.5,0,0.5,1.0]},figsize=(12,6))
fig,(ax1,ax2) = plt.subplots(nrows=1, ncols=2,figsize=(12,3),  gridspec_kw={'width_ratios': [1, 2]})
fig.subplots_adjust(wspace=0.3)
im1 = ax1.contourf(kx,ky,SSF,300,extent=[-1, 1, -1, 1],cmap=plt.cm.gist_heat,vmin=0.16,vmax=1.1) #Adjust for scaling between 5 and 1.17
ax1_divider = make_axes_locatable(ax1)
im1.set_edgecolor("face")
im1.set_linewidth(0.0)
im1.set_rasterized(True)
# add an axes to the right of the main axes.
cax1 = ax1_divider.append_axes("right", size="5%", pad="3%")

length=SSF.max()-SSF.min()
tick1=[round(SSF.min()+0.00+x*(length-0.01)*1.0/3,2) for x in range(4)]
#tick1=[round(x*(Sfxx.max()-0.0)*1.0/6,2) for x in range(7)]
cb1 = fig.colorbar(im1, cax=cax1,orientation="vertical",ticks=tick1)
cax1.xaxis.set_ticks_position("default")
cb1.ax.tick_params(labelsize=9)
#ax1.set_title(r'$S(q) = \frac{1}{N} \sum_{i,j} e^{-iqr_{ij}} \left< S_{i} \cdot S_{j} \right>}$',y=1.15, fontsize=16)
ax1.set_ylim([-1,1])
ax1.text(0.62,0.7,'$S(\\vec{q})$',c='w',fontsize=20)
#ax1.text(-1.5,0.7,'(a)', fontsize=fs)
#ax1.text(-1.4,-0.6,'$U/t=\infty$',rotation=90,fontsize=fs)
#ax1.set_xlabel(r'$q_x/2\pi$',fontsize = 16)
#ax1.set_ylabel(r'$q_y/2\pi$',rotation=90, position=(-1,0.5),fontsize = 16)
"""
im2 = ax2.contourf(kx,ky,Sfzz,300,extent=[-1, 1, -1, 1],cmap=plt.cm.jet)
ax2_divider = make_axes_locatable(ax2)
# add an axes above the main axes.
cax2 = ax2_divider.append_axes("top", size="5%", pad="2%")
tick2=[round(x*(Sfzz.max()-0.00)*1.0/6,2) for x in range(7)]
cb2 = fig.colorbar(im2, cax=cax2, orientation="horizontal",ticks=tick2)
# change tick position to top. Tick position defaults to bottom and overlaps
# the image.
cax2.xaxis.set_ticks_position("top")
ax2.set_title(r'$S^{zz}(q)$',y=1.19)
ax2.set_xlabel(r'$k_x/2\pi$',fontsize = 28)
"""
#corners of hexagonal BZ
coord=[[2.0/3,0],[1.0/3,-1.0/np.sqrt(3)],[-1.0/3,-1.0/np.sqrt(3)],[-2.0/3,0],[-1.0/3,1.0/np.sqrt(3)],[1.0/3,1.0/np.sqrt(3)]]
bonds=[[1,2],[2,3],[3,4],[4,5],[5,6],[6,1]]

for j,bond in enumerate(bonds):
    site1=bond[0]-1
    site2=bond[1]-1
    ax1.plot([coord[site1][0],coord[site2][0]],[coord[site1][1],coord[site2][1]],lw=1.2,c='w',linestyle='--')
    #ax2.plot([coord[site1][0],coord[site2][0]],[coord[site1][1],coord[site2][1]],lw=2,c='k',linestyle='--')

#ax1.axis('off')
#ax1.axis('equal')
#ax1.set_axis_off()
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_xticklabels([])
ax1.set_yticklabels([])
print('----------------------------------',max(SiSj2),min(SiSj2))
norm = plt.Normalize((0.04**p)*sc, (0.117**p)*sc) #53
cmap = plt.cm.Reds
for k,bnd in enumerate(bulk_bonds):
            s1=bnd[0]
            s2=bnd[1]
            strength = (SiSj2[k]**p)*sc
            color = cmap(norm(strength))
            ax2.plot([Rxy2[s1][0],Rxy2[s2][0]],[Rxy2[s1][1],Rxy2[s2][1]],c=color,lw=3) #-ss_avg
ax2.axis("off")
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Needed for colorbar without image
cbar = plt.colorbar(sm, ax=ax2, shrink=0.8)#, ticks=[0.01, 0.03,0.05])




#-----------------------------------------------------------------------------------------------------------------
colorc=[]
#print(SiSc)
for j in range(len(SiSc)):
        if SiSc[j]>0:
            colorc.append('b')
        else:
            colorc.append('r')
#for j in range(len(SiSc)):
         #print(j+1,SiSc[j])
         #ax2.scatter(Rxy[site_num_for_c[j]][0],Rxy[site_num_for_c[j]][1],s=np.abs(SiSc[j])*500,c=colorc[j],zorder=10)
#-----------------------------------------------------------------------------------------------------------------


#cbar.set_label("$|\\langle S_{i} \cdot S_{j} \\rangle|^{"+str(p)+"}$"+str(sc))
#ax.text(-3,4.5,'$n_{h}$ = '+str(nh))
#ax2.text(-2,0.9,"$|\\langle S_{i} \cdot S_{j} \\rangle|^{"+str(p)+"}$",rotation=90,fontsize=fs)
ax2.text(7.5,4.4,'$\\times10^{-3}$',fontsize=18)
#ax2.text(-2.1,4,'(b)',fontsize=fs)
#ax.text(2.5,4.5,str(round(ss_max,3)))
#ax.text(3.5,4.5,str(round(ss_avg,3)))
#ax.text(4.5,4.5,str(round(ss_min,3)))
#ax.text(5.5,4.5,str(scale))
ax2.axis('equal')
fs=30
#plt.text(-24.5,0.476,'(a)', fontsize=fs)
#plt.text(-24,0.3,'$U/t=\infty$',rotation=90,fontsize=fs+8)
plt.text(53,0.22,"$|\\langle S_{i} \cdot S_{j} \\rangle|^{"+str(p)+"}_{\\langle i,j\\rangle}$",rotation=90,fontsize=fs-5)
#plt.text(7,0.476,'(b)',fontsize=fs)
ax2.text(-4,5.2,'$n_{h} = 0.333$',fontsize=fs-4)
cb1.ax.tick_params(labelsize=20)  # first colorbar ticks

cbar.ax.tick_params(labelsize=20) 
plt.savefig("figs9x6diagonal_nh"+str(round(nh,3))+".pdf",bbox_inches='tight',dpi=300)
#plt.savefig("Bragg_peak_18x3_U=20_nholes="+str(nh)+".pdf",bbox_inches='tight',dpi=300)
#plt.show()
'''
fig = plt.figure()

ax = fig.add_subplot(1,1,1,projection='3d')
surf = ax.plot_surface(kx, ky, Sfxx, rstride=1, cstride=1,cmap=plt.cm.jet, edgecolor='none')
#fig.colorbar(surf, shrink=0.5,aspect=5)
fig.colorbar(surf,shrink=0.5)
ax.set_xlabel('kx/$\pi$')
ax.set_ylabel('ky/$\pi$')
ax.set_zlabel('Sxyq)')
#ax.set_title('surface');
#plt.savefig("3D_L149_T300")
plt.show()
'''
