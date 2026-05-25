import numpy as np
import sys 
sys.path.append("../")
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import matplotlib.pyplot as plt
import os
from bonds_n_coords_diagonal import diagonal_lat_bonds
from bonds_n_coords_diagonal import coordinates

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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#INPUT SYSTEM SIZES
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Nx = 6 #input('Enter the number of sites along open boundary ')
Ny = 6  #input('Enter the number of sites along periodic boundary ')
Nx = int(Nx)
Ny = int(Ny)
N = Nx*Ny
terms=int(N*N)   #NUMBER OF DATA POINTS TO READ FROM EACH FILE
ln=terms
U='inf'
#===================================================================
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
#===================================================================
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#READ THE DMRG OUTPUT FILE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fname = ["file6x6_Uinf_dia_8h_pn3.txt","file_6x6_diagonal_Uinf_12h_pn12.txt"]         #FILE NAME
Nh = [8,12]
SSF=[]
SiSj2=[]
#int(sys.argv[2]) 
#12
nh = [0.222,0.333]
#round(Nh/N,2)
for nn in range(len(fname)):
    command = "grep -A"+str(terms)+" \"i j <Si\" "+fname[nn]+" > temp" 
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
    #print(SiSj[0],SiSj[1])
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

    SSF.append([])
    for index_k in range(len(KX)):
        #print kx, ky, str_fac(kx,ky,Rxy,SiSj)
        ss =str_fac(KX[index_k],KY[index_k],Rxy,SiSj)
        SSF[nn].append(ss)
        #Sfxx.append(sxx)
    kx=np.reshape(KX,(2*(Nx+1),2*(Ny+4)))
    ky=np.reshape(KY,(2*(Nx+1),2*(Ny+4)))
    SSF[nn]=np.reshape(SSF[nn],(2*(Nx+1),2*(Ny+4)))

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
    for i in range(len(SSF[0])):
        temp=max(SSF[nn][i])
        if (max_sq < temp):
            max_sq = temp
    cy_bond, op_bond = diagonal_lat_bonds(Nx,Ny)
    bonds=op_bond
    Rxy2 = coordinates(Nx,Ny)

    command = "grep -A"+str(ln)+" \"i j <Si^z Sj^z>\" "+fname[nn]+" > tmp"
    os.system(command)
    SS2 = [[],[],[],[],[]]
    SiSj2.append([])
    f=open("tmp",'r')
    for l,line in enumerate(f):
        for n in range(len(op_bond)):
            if (l == (op_bond[n][0]-1)*N+op_bond[n][1]):
                line=line.strip()
                line=line.split(" ")
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
                SiSj2[nn].append(np.abs(val))
                #print(line[0],line[1],line[2],line[3],line[4],val)
    f.close()

#Nbonds=len(SiSj2)
#print(Nbonds)
#ss_avg=sum(SiSj2)/Nbonds
ss_max=max(max(SiSj2))
print(ss_max)
ss_min=min(min(SiSj2))
print(ss_min)
bulk_bonds=[]
for i in range(len(bonds)):
        if ((Nx <= 9 and (bonds[i][0] <= Ny or bonds[i][1] > N-Ny)) or (Nx > 9 and (bonds[i][0] <= 2*Ny or bonds[i][1] > N-2*Ny)) ):
            continue
        bulk_bonds.append(bonds[i])

#print(SSF)
#print(SiSj2)
sc= 1000
p= 3
fs=24
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#PLOT STATIC STRUCTURE FACTOR OVER THE K SPACE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fig,ax = plt.subplots(nrows=2, ncols=2,figsize=(6,6))#,gridspec_kw={'height_ratios': [1, 1.2]})
fig.subplots_adjust(wspace=0.1,hspace=0.2)
for nn in range(len(fname)):
    im10 = ax[0][0].contourf(kx,ky,SSF[0],300,extent=[-1, 1, -1, 1],cmap=plt.cm.gist_heat,vmin=0.0,vmax=1.1) #Adjust for scaling between 5 and 1.1
    im1 = ax[0][1].contourf(kx,ky,SSF[1],300,extent=[-1, 1, -1, 1],cmap=plt.cm.gist_heat,vmin=0.0,vmax=1.1)
    ax1_divider = make_axes_locatable(ax[0][nn])
    #for im in im1.collections:
    #        im.set_edgecolor("face")
    im1.set_edgecolor("face")
    im1.set_linewidth(0.0)
    im1.set_rasterized(True)
    # add an axes to the right of the main axes.
    ax[0][nn].axis('equal')
    ax[0][nn].set_aspect('equal', adjustable='box')
    ax[0][nn].set_ylim([-1,1])
    ax[0][nn].set_xticks([])
    ax[0][nn].set_xticklabels([])
    ax[0][nn].set_yticks([])
    ax[0][nn].set_yticklabels([])
ax[0][1].text(0.65,0.7,'$S(\\vec{q})$',c='w',fontsize=18)
#corners of hexagonal BZ
coord=[[2.0/3,0],[1.0/3,-1.0/np.sqrt(3)],[-1.0/3,-1.0/np.sqrt(3)],[-2.0/3,0],[-1.0/3,1.0/np.sqrt(3)],[1.0/3,1.0/np.sqrt(3)]]
bonds=[[1,2],[2,3],[3,4],[4,5],[5,6],[6,1]]

for j,bond in enumerate(bonds):
    site1=bond[0]-1
    site2=bond[1]-1
    ax[0][0].plot([coord[site1][0],coord[site2][0]],[coord[site1][1],coord[site2][1]],lw=1.2,c='w',linestyle='--')
    ax[0][1].plot([coord[site1][0],coord[site2][0]],[coord[site1][1],coord[site2][1]],lw=1.2,c='w',linestyle='--')
    #ax2.plot([coord[site1][0],coord[site2][0]],[coord[site1][1],coord[site2][1]],lw=2,c='k',linestyle='--')

cax1 = fig.add_axes([0.92, ax[0][1].get_position().y0+0.03, 0.016, 0.31])
#tick1 = [round(np.min(SSF[0]), 2), round((np.min(SSF[0]) + np.max(SSF[0])) / 2, 2), round(np.max(SSF[0]), 2)-0.01]
tick1 = [0,0.16,0.39,0.61,0.84]
cb1 = fig.colorbar(im10, cax=cax1, orientation='vertical', ticks=tick1)
cb1.ax.tick_params(labelsize=14)


norm = plt.Normalize((ss_min**p)*sc, (ss_max**p)*sc) #53
cmap = plt.cm.Reds
for k,bnd in enumerate(bulk_bonds):
    for nn in range(2):
            s1=bnd[0]
            s2=bnd[1]
            strength = (SiSj2[nn][k]**p)*sc
            color = cmap(norm(strength))
            ax[1][nn].plot([Rxy2[s1][0],Rxy2[s2][0]],[Rxy2[s1][1],Rxy2[s2][1]],c=color,lw=3) #-ss_avg
            ax[1][nn].axis("off")
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Needed for colorbar without image
cbar = plt.colorbar(sm, ax=ax[1][1], shrink=0.8)#, ticks=[0.01, 0.03,0.05])
cbar_ax = cbar.ax
pos = cbar_ax.get_position()
cbar_ax.set_position([pos.x0 + 0.08, pos.y0+0.02, pos.width+0.8, pos.height-0.02])
#cbar.set_label("$|\\langle S_{i} \cdot S_{j} \\rangle|^{"+str(p)+"}$"+str(sc))
#ax.text(-3,4.5,'$n_{h}$ = '+str(nh))
#ax2.text(-2,0.9,"$|\\langle S_{i} \cdot S_{j} \\rangle|^{"+str(p)+"}$",rotation=90,fontsize=fs)
ax[1][1].text(4,4.2,'$\\times 10^{-3}$',fontsize=20)
#ax2.text(-2.1,4,'(b)',fontsize=fs)
#ax.text(2.5,4.5,str(round(ss_max,3)))
#ax.text(3.5,4.5,str(round(ss_avg,3)))
#ax.text(4.5,4.5,str(round(ss_min,3)))
#ax.text(5.5,4.5,str(scale))
ax[1][0].axis('equal')
ax[1][1].axis('equal')

pos = ax[1][1].get_position()
ax[1][1].set_position([pos.x0+0.0, pos.y0-0.03, pos.width+0.11, pos.height+0.11])
pos = ax[1][0].get_position()
ax[1][0].set_position([pos.x0+0.03, pos.y0, pos.width+0.04, pos.height+0.04])

fs=30
#plt.text(-24.5,0.476,'(a)', fontsize=fs)
#plt.text(-24,0.3,'$U/t=\infty$',rotation=90,fontsize=fs+8)
ax[1][0].text(11.5,0.8,"$|\\langle S_{i} \cdot S_{j} \\rangle|^{"+str(p)+"}_{\\langle i,j \\rangle}$",rotation=90,fontsize=18)
#ax[1][0].text(-4,4.7,'$n_{h} = '+str(round(nh,3))+'$',fontsize=fs)
cb1.ax.tick_params(labelsize=20)  # first colorbar ticks

cbar.ax.tick_params(labelsize=20) 

fig.canvas.draw()
y_line = 0.9
fig_width = fig.get_figwidth()
for nn in range(len(fname)):
    bbox = ax[0][nn].get_position()
    x_center = (bbox.x0 + bbox.x1) / 2
    fig.text(x_center,y_line+0.015, f'{nh[nn]:.3f}',ha='center',va='bottom',fontsize=20)
    fig.text(x_center, y_line, '|', ha='center', va='center', fontsize=16,rotation=90)
#fig.lines.append(plt.Line2D([ax[0][0].get_position().x0+0.02, (ax[0][1].get_position().x1)-0.005],[y_line, y_line], transform=fig.transFigure, color='black'))
ax_annotate = fig.add_axes([0, 0, 1, 1], zorder=-1)
ax_annotate.axis('off')

# Draw full ray as arrow
start_x = ax[0][0].get_position().x0+0.011
end_x = ax[0][1].get_position().x1

ax_annotate.annotate(
    '',
    xy=(end_x+0.01, y_line+0.012),        # arrow tip
    xytext=(start_x+0.01, y_line+0.012),  # arrow tail
    xycoords='figure fraction',
    textcoords='figure fraction',
    arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
    )

plt.text(0.12,0.91,'$n_{h}$',fontsize=24)
plt.savefig("figs6x6diagonal_2nh.pdf",bbox_inches='tight',dpi=300)
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
