import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

def spheredefine(x, z, a,S):
    """Function to define a sphere shape in 2D"""
    r = np.sqrt(x*x + z*z)
    if r <= a/2:
        shape = S
    else:
        shape = 1
    return shape

def Recdefine(x, z, len, wid,S):
    """Function to define a rectangular shape in 2D"""
    if ((-len)/2 <= x <= len/2) and ((-wid) / 2 <= z <= wid/2):
        shape = S
    else:
        shape = 1
    return shape

def Triangdefine(x, z, a1,x1,y1, S):
    """Function to define a triangular shape in 2D"""
    k = np.tan(a1*np.pi/180)
    if (- k * x - y1<= z <= k * x + y1) and (-y1/k <= x <= x1-y1/k):
        shape = S
    else:
        shape = 1
    return shape

def rhombus(x, z, a1,y1, S):
    """Function to define a triangular shape in 2D"""
    k = np.tan(a1*np.pi/180)
    if (- k * x - y1<= z <= k * x + y1) and (k * x - y1<= z <= - k * x + y1) :
        shape = S
    else:
        shape = 1
    return shape

def Triedgdefine(x, z, a1,x1,y1, S):
    """Function to define a triangular shape in 2D, edge first"""
    k = np.tan(a1*np.pi/180)
    if (k * x - y1<= z <= - k * x + y1) and (-x1 + y1/k <= x <= y1/k):
        shape = S
    else:
        shape = 1
    return shape

def Resistornetwork(N, L, rho, J0, S):
    """Function to calculate resistor network"""
    DV = rho * J0 * L
    Rnode = rho
    sigma = 1 / Rnode
    N2 = N * N
    G = np.zeros((N2,N2))
    I = np.zeros((N2,1))

    # i = 1, j = 1 - top left node
    k = 0
    I[k] = DV * sigma
    G[k, k] = 3 * sigma
    G[k, k+1] = -sigma
    G[k, k+N] = -sigma
    # i = 1, j = Nx - top right node
    k = N-1
    G[k, k] = 3 * sigma
    G[k, k-1] = -sigma
    G[k, k+N] = -sigma
    # i = Ny, j = Nx - bottom right node
    k = N2-1
    G[k, k] = 3 * sigma
    G[k, k-1] = -sigma
    G[k, k-N] = -sigma
    # i = Ny, j = 1 - bottom left node
    k = (N - 1) * N
    I[k] = DV * sigma
    G[k, k] = 3 * sigma
    G[k, k + 1] = -sigma
    G[k, k - N] = -sigma

    # Left boundary(without corners)
    for i in range(1, N-1):
        k = i * N
        I[k] = DV * sigma
        G[k, k] = 4 * sigma
        G[k, k + 1] = -sigma
        G[k, k - N] = -sigma
        G[k, k + N] = -sigma

    # Right boundary(without corners)
    for i in range(1, N-1):
        k =i * N + N -1
        G[k, k] = 4 * sigma
        G[k, k - 1] = -sigma
        G[k, k - N] = -sigma
        G[k, k + N] = -sigma

    # Top boundary(without corners)
    for j in range(1, N-1):
        k = j
        G[k, k] = 3 * sigma
        G[k, k - 1] = -sigma
        G[k, k + 1] = -sigma
        G[k, k + N] = -sigma

     # Bottom boundary(without corners)
    for j in range(1, N - 1):
        k = (N - 1) * N + j
        G[k, k] = 3 * sigma
        G[k, k - 1] = -sigma
        G[k, k + 1] = -sigma
        G[k, k - N] = -sigma

    # All inner points
    # if node(i, j) has S=0, take resitor to be infinity between nodes
    for i in range(1, N - 1):
        for j in range(1, N - 1):
            k = i * N + j
            ss = S[i, j + 1] + S[i, j - 1] + S[i + 1, j] + S[i - 1, j]
            G[k, k] = ss * sigma
            G[k, k + 1] = -sigma * S[i, j + 1]
            G[k, k - 1] = -sigma * S[i, j - 1]
            G[k, k + N] = -sigma * S[i + 1, j]
            G[k, k - N] = -sigma * S[i - 1, j]

    iG = np.linalg.pinv(G)
    Vvec = np.dot(iG, I)

    # sort vector Vvec into Ny x Nx array = V
    for i in range(0, N):
        k = i * N
        for j in range(0, N):
            V[i, j] = Vvec[k + j]
    Vnode = DV / (N +1)
    for i in range(0, N):
        for j in range(0,N):
            fV[i, j] = V[i, j] - (DV-j * Vnode)

    return fV, V

def customPlot(x: object, y: object, labelx: object, labely: object, title: object, args: object, filename: object) -> object:
    """Plot an array x, y"""
    plt.figure()
    plt.plot(x, y, *args)
    plt.title(title)
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.savefig(filename)
    plt.show()

def customImPlot(x, labelx, labelc, title, color,L,filename):
        """Plot a image"""
        plt.imshow(x,cmap=color,extent=[0,L,0,L])
        plt.title(title)
        plt.xlabel(labelx)
        plt.colorbar(label=labelc)
        plt.savefig(filename)
        plt.show()


#parameters 2D
J0 = -2 #A/m - current density
rho = 677 #Ohm - sheet resistnace

#hole shape 2D
D = 10e-9 #m - hole diameter
length = 50e-9 #m - hole dimension along current direction
width = 90e-9#m - hole dimension perpendicular to current direction
a1 = 22.5   #degree- half of the triangle
x1 = 20e-9 #m - edge of one triangle
y1 = 5e-9#m - plotting window vertial shift
S = 2.3
# 0 means infinite resistance at this node
# 0 < S < 1 higher resistance than background
# S > 1  lower  resistance  than background

#create mesh
L =100e-9 #m - plotting window width and height is L
N = 60 #no of pixels
dL = L/N
V = np.zeros((N,N))
fV = np.zeros((N,N))
shape = np.zeros((N,N))
X = np.linspace(-L/2, L/2, N)
Z = X

# define the shape of resistor network
itx = np.nditer(X, order='C', flags=['f_index'])
for x in itx:
    itz = np.nditer(Z, order='C', flags=['f_index'])
    for z in itz:
       # shape[itz.index, itx.index] = spheredefine(x, z, D, S)
         shape[itz.index, itx.index] = Recdefine(x, z, length, width, S)
        # shape[itz.index, itx.index] = rhombus(x, z, a1, y1, S)
        # shape[itz.index, itx.index] = Triangdefine(x, z, a1, x1, y1, S)
        # shape[itz.index, itx.index] = Triedgdefine(x, z, a1, x1, y1, S)


path = 'Z:/intermag/projects/STM_lab/Tools/RHK Tesla SPM/Data - analyzed/SiC Li intercalated graphene/resistor network simulation/'
filename = path+'Defect geometry.png'
customImPlot(shape, 'Topography (nm)', 'Conductivity' ,'Defect geometry, '+'the simulation resolution is '+ '{:.2f} '.format(dL*1000000000) + 'nm', 'gray',L*1000000000,filename)
fV, V = Resistornetwork(N, L, rho, J0, shape)
filename = path+'ECP map.png'
customImPlot(V*1000000, 'Topography (nm)', 'ECP ($\mu$V)' ,'ECP map', 'cool',L*1000000000,filename)
filename = path+'Flattened map.png'
customImPlot(fV*1000000, 'Topography (nm)', 'ECP ($\mu$V)' ,'Flattened ECP map', 'cool',L*1000000000,filename)
filename = path+'ECP profile (Length' +'{:.0f} '.format(length*1000000000)+ 'nm, width '+'{:.0f} '.format(width*1000000000) +'nm).png'
customPlot(X*1000000000, V[int(N/2)-1]*1000000, 'profile (nm)', 'ECP ($\mu$V)', 'ECP profile','-',filename)
filename = path+'Flattened ECP profile (Length' +'{:.0f} '.format(length*1000000000)+ 'nm, width '+'{:.0f} '.format(width*1000000000) +'nm).png'
labelp = 'Dipole strength is '+ '{:.2f} '.format(max(fV[int(N/2)-1]*1000000-mean(fV[int(N/2)-1]*1000000)))+' $\mu V$'
customPlot(X*1000000000, fV[int(N/2)-1]*1000000-mean(fV[int(N/2)-1]*1000000), 'profile (nm)', 'ECP ($\mu$V)', 'Flattened ECP profile, '+labelp,'-',filename)
np.savetxt(path+"V.txt", np.c_[X*1000000000, V[int(N/2)-1]*1000000])
np.savetxt(path+"fV.txt", np.c_[X*1000000000, fV[int(N/2)-1]*1000000-mean(fV[int(N/2)-1]*1000000)])

