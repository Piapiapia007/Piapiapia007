import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
from lmfit.models import LinearModel
from scipy import optimize

def openfile(path,start):
    """read data from path and start from the 'start' line."""
    data = list(open(path, "rb"))
    # print(data)
    value = []
    for i in range(start, len(data)-1):
        value.append(data[i].decode('utf-8').split())
    # print(value)
    x = []
    y = []
    xx = []
    yy = []
    for i in range(len(value)):
        x.append(value[i][0])
        y.append(value[i][1])
    # print(x)
    # float the elements
    for i in x:
        xx.append(float(i))
    # print(xx)
    for i in y:
        yy.append(float(i))
    # print(ECP)
    # convert list to array
    xxx = np.array(yy)
    yyy = np.array(xx)
    return xxx, yyy

def index_of(arrval, value):
    """Return index of array *at or below* value."""
    if value < min(arrval):
        return 0
    return max(np.where(arrval <= value)[0])

def index_within(start, stop):
    """Return index of array between these two values."""
    index1 = index_of(x1, start)
    index2 = index_of(x1, stop)
    return index1, index2

def fitting_parameter(x,y, parameter_name, parameter_value,parameter_error,mode,pars):

    out = mode.fit(y, pars, x=x)
    for i in out.params:
        parameter_name.append(out.params[i].name)
        parameter_value.append(out.params[i].value)
        parameter_error.append(out.params[i].stderr)
        # error of each value
        # print(out.params[i].stderr)
        # print(out.params[i].min)
        # print(out.params[i].max)
        # experssions of each data
        # print(out.params[i].expr)
    # return a full reports about all the data
    # print(out.fit_report(min_correl=0.25))
    # return a dictionary about using parameters
    # print(out.best_values)
    # return a set of tuple of individual data
    # print(out.params)
    return out

def dipole_fitting(x,y,z,shift,filename):
    x = x - mean(x) + shift
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Profile (nm)')
    ax1.set_ylabel('ECP(uV)')
    ax1.plot(x, y, '.')
    ax1.tick_params(axis='y')

    p, e = optimize.curve_fit(piecewise_linear, x, y)
    # print(p[1])
    ax1.plot(x, piecewise_linear(x, *p),
             label='Dipole strength: ' + "{:.2f} ".format(p[1] / (-p[0])) + " $\pm$ {:.2f} ".format(
                 np.sqrt(np.diag(e))[1] / ((p[0]))) + " $\mu V$ \nfitting shift " + "{:.2f} ".format(shift))
    # np.sqrt(np.diag(e))[0]+abs(shift)
    plt.legend(loc=(0, 0.9), prop={"size": 9})
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Topography(nm)')
    ax2.plot(x, z, 'k')
    ax2.tick_params(axis='y')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(filename + '.png')

def MFPkf(n, kf, rho):
    G0 = 7.748091729e-5
    """ the unit for rho should be Ohm"""
    """ the unit for n should be cm^-2"""
    MFP = (kf)/(G0*np.pi*n*rho)
    print('Mean free path is '+"{:.4f} ".format(MFP*1e14)+'nm')
    return MFP

def MFPk1(J, d, n, k1, rho):
    G0 = 7.748091729e-5
    """ the unit for d should be nm, which is the diameter of hole"""
    """ the unit for J should be A/m"""
    """ the unit for k1 should be uV*nm"""
    """ the unit for rho should be Ohm"""
    """ the unit for n should be cm^-2"""
    MFP = - (8*J*d*1e11)/(3*G0*G0*np.pi*np.pi*n*k1*rho)
    print('Mean free path is '+"{:.4f} ".format(MFP)+'nm')
    kf = - (8*J*d*1e-3)/(3*G0*np.pi*k1)
    print('wavevector is '+"{:.4f} ".format(kf)+'nm-1')
    return MFP,kf

""" fit flatted ECP."""
def piecewise_linear_flat(x, x0, k1, x2):
    condlist = [x < -x0+x2, (x >= -x0+x2) & (x < x0+x2), x >= x0+x2]
    funclist = [lambda x: k1/(x-x2), lambda x: (k1/(x0*x0))*(x-x2) , lambda x: k1/(x-x2) ]
    return np.piecewise(x, condlist, funclist)

""" fit original ECP."""
def piecewise_linear(x, x0, k1, x1, k2, b):
    condlist = [x < -x0+x1, (x >= -x0+x1) & (x < x0+x1), x >= x0+x1]
    funclist = [lambda x: k1/(x-x1) +k2 * x+ b, lambda x: (k1/(x0*x0))*(x-x1)+ k2 * x + b , lambda x: k1/(x-x1)+k2*x+ b ]
    return np.piecewise(x, condlist, funclist)

Address = "Z:/intermag/projects/STM_lab/Tools/RHK Tesla SPM/Data - analyzed/graphene holes ECP 202103/"
file = "InContacts_2021_02_12_15_29_02_689"
# path = Address + "ECP/flatted data/" + file + ".txt"
path = Address + "ECP/" + file + ".txt"
# path = Address + "Thermal/" + file + ".txt"
path2 = Address + "Topography/" + file + ".txt"

Address2 = "Z:/intermag/projects/STM_lab/Tools/RHK Tesla SPM/Data - analyzed/graphene holes ECP 202103/resistor network simulation/"
file1 = "fV.txt"
# file2 = "V.txt"
path11 = Address2 + "sphere/15nm 200nm range, 0.001/" + file1
# path22 = Address2 + "45degree 30nm,200nm, 0.001,flip/" + file2

"""define empty matrix including several lists for data storage"""
parameter_value = [[0 for i in range(0)] for j in range(9)]
parameter_error = [[0 for i in range(0)] for j in range(9)]
parameter_name = [[0 for i in range(0)] for j in range(9)]

# The unit is mA
current = 2

"""x1, and y refer to ECP data, x2,z refer to Topography data"""
x1 = []
x2 = []
y = []
z = []
FV =[]
V = []
X = []

shift = 2

y, x1 = openfile(path,4)
z, x2 = openfile(path2,4)
FV, X = openfile(path11,0)
# V, X = openfile(path22,0)

""" rescale x from m to nm, y from V to uV"""
x1 = (x1-mean(x1))*1e9 + shift
x2 = (x2-mean(x2))*1e9 + shift
y = (y-mean(y))*1e6
z = (z-min(z))*1e9
X = X + shift

""" plot ECP."""
fig, ax1 = plt.subplots()
ax1.set_xlabel('Profile (nm)')
ax1.set_ylabel('ECP(uV)')
# ax1.set_ylabel('Thermal voltage (uV)')
ax1.plot(x1, y, 'o')
# ax1.plot(X, FV,'r',label='resistor network simulation')
ax1.tick_params(axis='y')

""" fit dipole"""
p , e = optimize.curve_fit(piecewise_linear, x1, y)
# print(p)
print(np.sqrt(np.diag(e)))
ax1.plot(x1, piecewise_linear(x1, *p), label = 'Dipole strength: ' + "{:.2f} ".format(p[1]/(-p[0])) +" $\pm$ {:.2f} ".format(np.sqrt(np.diag(e))[1]/((p[0]))) + " $\mu V$ \nfitting shift " + "{:.2f} ".format(shift))
print( 'sheet resistance: ' + "{:.2f} ".format(p[3]) +" $\pm$ {:.2f} ".format(np.sqrt(np.diag(e))[3]))
# np.sqrt(np.diag(e))[0]+abs(shift)

""" calculate the mean free path for ballistic"""
# MFP,kf = MFPk1(4, 22.35, 5e12, p[1], 150)
# MFP = MFPkf(5e12, 0.67, 150)

""" fit linear ECP."""
# get index of a region from the image where I want to fit the data
i, j =index_within(-22,-10)
a, b =index_within(-100,100)

# linear fit
line_mod = LinearModel(prefix='line_')
pars = line_mod.make_params(intercept=y.min(), slope=0)
mode = line_mod
# out = fitting_parameter(x1[i:j],y[i:j], parameter_name[0], parameter_value[0],parameter_error[0],mode,pars)
# out1 = fitting_parameter(x1[a:b],y[a:b], parameter_name[1], parameter_value[1],parameter_error[1],mode,pars)
# ax1.plot(x1[i:j], out.best_fit, 'm-', label = '$\\rho$ = ' + "{:.2f} ".format(-parameter_value[0][0]*500/current) +" $\pm$ {:.2f} ".format(parameter_error[0][0]*500/current) + 'Ohm')
# ax1.plot(x1[a:b], out1.best_fit, 'g-', label = '$\\rho$ = ' + "{:.2f} ".format(-parameter_value[1][0]*500/current) +" $\pm$ {:.2f} ".format(parameter_error[1][0]*500/current) + 'Ohm')


""" plot. topography"""
plt.legend(loc=(0.04, 0.00),prop={"size":9})
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('Topography(nm)')
ax2.plot(x2, z,'k')
ax2.tick_params(axis='y')
fig.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.savefig(Address+file+'.png')

# np.savetxt(path.replace( file + ".txt", 'Topo.txt') ,np.c_[x2, z])
# np.savetxt(path.replace( file + ".txt", 'ECP.txt') ,np.c_[x1, y])
# np.savetxt(path.replace( file + ".txt", 'FIT.txt') ,np.c_[x1, piecewise_linear(x1, *p)])

plt.show()



