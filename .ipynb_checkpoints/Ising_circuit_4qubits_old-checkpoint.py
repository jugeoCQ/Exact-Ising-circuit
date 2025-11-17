import pennylane as qml
from pennylane import numpy as np

def theta_k(h, n, k): #the only place where h comes in is theta which determines how much the modes are mixed in the bogoliubov transform
    return np.arccos((h - np.cos(2 * np.pi * k / n)) /
                       np.sqrt((h - np.cos(2 * np.pi * k / n))**2 + np.sin(2 * np.pi * k / n)**2))


def B(wires, theta_k, n, h):
    q0 = wires[0]
    q1 = wires[1]
    
    qml.PauliX(wires = q1)
    qml.CNOT(wires = [q1, q0])
    qml.ctrl(qml.RX, control = q0)(theta_k, wires = q1)
    qml.CNOT(wires = [q1, q0])
    qml.PauliX(wires = q1)   

#Ok for some reason this works but I think
#FS = qml.FermionicSWAP(phi = np.pi, wires = [0,1]).matrix() #SWAP + CZ
#SE = qml.SingleExcitation(phi = np.pi/2, wires = [0, 1]).matrix()

#F2 = np.real(FS @ SE)
def Fdag(wires, k):
    q0 = wires[0]
    q1 = wires[1]
    
    #these two give F2 which is hermitian so F_2^dag = F_2
    #FIGURE OUT HOW THIS RELATES TO QFT BETTER
    qml.FermionicSWAP(phi = np.pi, wires = wires) 
    qml.SingleExcitation(phi = np.pi/2, wires = wires)

    #Twiddle factor for the odd sector (for k = 0, its just identity so ignore)
    #Take the dag because this one is not hermitian
    if k == 1: #for n = 4 specifically. Not general to all n       
        qml.adjoint(qml.S(wires = q0)) #pi/2

def Udis(h):
    theta = theta_k(h = h, n = 4, k = 1)
    B(wires = [0,1], theta_k = theta, n = 4, h = h) #dag?
    #B at k = 0 is identity at h > 1 so no need to include it 
    #FIGURE OUT WHATS UP AT h < 1 ?

    #Recursive QFT structure
    #This is essentially just standard QFT but the SWAP part has to be fermionic because of the JW transform
    Fdag(wires = [0,1], k = 1) #dag
    Fdag(wires = [2,3], k = 0) #dag #just F_2 no twiddle

    qml.FermionicSWAP(phi = np.pi, wires = [1,2])

    Fdag(wires = [0,1], k = 0) #dag #just F_2 no twiddle
    Fdag(wires = [2,3], k = 0) #dag #just F_2 no twiddle
    
    qml.FermionicSWAP(phi = np.pi, wires = [1,2])

def Ising(h):
     # For h > 1, prepare the state in |0000> so do nothing #even sector # APBC after JW ?
    if h < 1: #otherwise prepare the state in |0001> #odd sector. #PBC after JW?
        qml.PauliX(wires = 3)

    # Notation is sketchy but this is the reverse direction
    #So we're doing bogoliubov then fourier
    #cant remember if that's U_dis or U^dag_dis but it doesn't matter just notation
    Udis(h)