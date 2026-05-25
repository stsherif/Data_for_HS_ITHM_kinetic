import matplotlib.pyplot as plt
import numpy as np


def diagonal_lat_bonds(Nx,Ny):
    N = Nx*Ny
    bond = [] #clyndrical
    opbond = [] #open
    for i in range(1,N):
        if i in range(2,Ny):
            #first diagonal
            b=[i,i+1]
            bond.append(b)
            opbond.append(b)
            b=[i,i+Ny]
            bond.append(b)
            opbond.append(b)
            b=[i,i+Ny+1]
            bond.append(b)
            opbond.append(b)
            b=[i,i-1]
            #bond.append(b)
            #opbond.append(b)
        elif i in range(N-Ny+2,N):
            #last diagonal
            b=[i,i+1]
            bond.append(b)
            opbond.append(b)
            b=[i,i-1]
            #bond.append(b)
            #opbond.append(b)
            b=[i,i-Ny]
            #bond.append(b)
            #opbond.append(b)
            b=[i,i-Ny-1]
            #bond.append(b)
            #opbond.append(b)
        elif (i%Ny==0 and i<N and i>Ny):
            # bottom line
            b=[i,i+1]
            bond.append(b)
            b=[i,i+Ny]
            bond.append(b)
            opbond.append(b)
            b=[i,i-Ny+1]
            #bond.append(b)
            b=[i,i-1]
            #bond.append(b)
            #opbond.append(b)
            b=[i,i-Ny]
            #bond.append(b)
            #opbond.append(b)
            b=[i,i-Ny-1]
            #bond.append(b)
            #opbond.append(b)
        elif (i%Ny==1 and i>1 and i<N-Ny+1):
            #top line
            b=[i,i+1]
            bond.append(b)
            opbond.append(b)
            b=[i,i+Ny-1]
            bond.append(b)
            b=[i,i+Ny]
            bond.append(b)
            opbond.append(b)
            b=[i,i+Ny+1]
            bond.append(b)
            opbond.append(b)
            b=[i,i-1]
            #bond.append(b)
            b=[i,i-Ny]
            #bond.append(b)
            #opbond.append(b)
        elif (i==1):
            b=[i,i+1]
            bond.append(b)
            opbond.append(b)
            b=[i,i+Ny-1]
            bond.append(b)
            b=[i,i+Ny]
            bond.append(b)
            opbond.append(b)
            b=[i,i+Ny+1]
            bond.append(b)
            opbond.append(b)
        elif (i==Ny):
            b=[i,i+1]
            bond.append(b)
            b=[i,i-1]
            #bond.append(b)
            #opbond.append(b)
            b=[i,1]
            #bond.append(b)
            b=[i,i+Ny]
            bond.append(b)
            opbond.append(b)
        elif (i==N-Ny+1):
            b=[i,i+1]
            bond.append(b)
            opbond.append(b)
            b=[i,i-1]
            #bond.append(b)
            b=[i,i+Ny-1]
            #bond.append(b)
            b=[i,i-Ny]
            #bond.append(b)
            #opbond.append(b)
        else:
            #bulk
            b=[i,i+1]
            bond.append(b)
            opbond.append(b)
            b=[i,i+Ny]
            bond.append(b)
            opbond.append(b)
            b=[i,i+Ny+1]
            bond.append(b)
            opbond.append(b)
            b=[i,i-1]
            #bond.append(b)
            #opbond.append(b)
            b=[i,i-Ny]
            #bond.append(b)
            #opbond.append(b)
            b=[i,i-Ny-1]
            #bond.append(b)
            #opbond.append(b)
    unique_bond=sorted(set(tuple(t) for t in bond))
    unique_opbond=sorted(set(tuple(t) for t in opbond))
    return unique_bond, unique_opbond

#finding coordinates
def coordinates(Nx,Ny):
    N = Nx*Ny
    a1 = np.array([1,0])
    a2 = np.array([-0.5,np.sqrt(3)/2.0])
    #a2 = np.array([0.5,np.sqrt(3)/2.0])

    Rxy = {}

    for i in range (1,Nx+1):
        for j in range (1,Ny+1):
            l = j+(i-1)*Ny
            Rxy[l] = (i-1)*a1+(j-1)*a2

    return Rxy


def sub(Nx,Ny):
    sublattice = {}
    color = {}

    for i in range(1,Nx+1):
        for j in range(1,Ny+1):
            site = j + (i-1)*Ny
            if i%3 == 1:
                if j%3 == 1:
                    label = 'A'
                    c = 'red'
                elif j%3 ==2:
                    label = 'B'
                    c = 'blue'
                elif j%3 ==0:
                    label = 'C'
                    c = 'green'
            elif i%3 == 2:
                if j%3 == 1:
                    label = 'B'
                    c='blue'
                elif j%3 == 2:
                    label = 'C'
                    c='green'
                elif j%3 == 0:
                    label = 'A'
                    c = 'red'
    
            else:
                if j%3 == 1:
                    label = 'C'
                    c='green'
                if j%3 == 2:
                    label = 'B'
                    c='blue'    
                else:
                    label = 'A'
                    c='red'

            sublattice[site] = label
            color[site] = c

    return sublattice, color

"""
Nx = 4
Ny = 3
N = Nx*Ny
sublattice, color = sub(Nx,Ny)
print(sublattice)
bond,bonds = diagonal_lat_bonds(Nx,Ny)
Rxy = coordinates(Nx,Ny)
print(Rxy)
for k,bnd in enumerate(bonds):
    s1=bnd[0]
    s2=bnd[1]
    
    plt.plot([Rxy[s1][0],Rxy[s2][0]],[Rxy[s1][1],Rxy[s2][1]],lw=1,c='k')
    plt.text(Rxy[s1][0]+0.05,Rxy[s1][1],str(s1),fontsize=10)#,weight="bold",color='green')
plt.text(Rxy[N][0]+0.05,Rxy[N][1],str(N),fontsize=10)
plt.axis("off")
print(bond)
plt.axis('equal')
#plt.savefig('lattice_18x3.pdf',dpi=600,bbox_inches='tight')

for i in range(1,N+1):
    plt.text(Rxy[i][0],Rxy[i][1]+0.1,sublattice[i],color=color[i],zorder=3,fontweight='bold',fontsize=10)

#plt.show()
"""

