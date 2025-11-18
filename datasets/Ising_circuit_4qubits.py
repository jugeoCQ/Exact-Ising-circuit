import pennylane as qml
from pennylane import numpy as np

def theta_k(h, n, k): #the only place where h comes in is theta which determines how much the modes are mixed in the bogoliubov transform
    return np.arccos((h - np.cos(2 * np.pi * k / n)) /
                       np.sqrt((h - np.cos(2 * np.pi * k / n))**2 + np.sin(2 * np.pi * k / n)**2))


def B_dag(q0, q1, theta_k, n, h): # 
    qml.PauliX(wires = q1)
    qml.CNOT(wires = [q1, q0])
    qml.ctrl(qml.RX, control = q0)(-theta_k, wires = q1) #Use -theta_k in the dag operation
    qml.CNOT(wires = [q1, q0])
    qml.PauliX(wires = q1)   

def F_kn_dag(q0, q1, k, n): #dagged so taking - 2pi k/n in the phase shift
    if k!= 0:
        qml.PhaseShift(-2*np.pi*k/n, wires = q0) 
    qml.CNOT(wires = [q0, q1])
    qml.ctrl(qml.Hadamard, control = q1)(q0)
    qml.CNOT(wires = [q0, q1])
    qml.CZ(wires = [q0, q1])

def Udis(h):
    theta = theta_k(h = h, n = 4, k = 1)
    B_dag(0,1, theta_k = theta, n = 4, h = h) 
    #B at k = 0 is identity at h > 1 so no need to include it 
    #FIGURE OUT WHATS UP AT h < 1 ?

    #Recursive QFT structure
    #This is essentially just standard QFT but the SWAP part has to be fermionic because of the JW transform
    F_kn_dag(0,1, k = 1, n = 4) 
    F_kn_dag(2,3, k = 0, n = 4) 

    qml.FermionicSWAP(phi = np.pi, wires = [1,2])

    F_kn_dag(0,1, k = 0, n = 4) 
    F_kn_dag(2,3, k = 0, n = 4) 
    
    qml.FermionicSWAP(phi = np.pi, wires = [1,2])

def Ising(h):
     # For h > 1, prepare the state in |0000> so do nothing #even sector # APBC after JW ?
    if h < 1: #otherwise prepare the state in |0001> #odd sector. #PBC after JW?
        qml.PauliX(wires = 3)

    # Notation is confusing but this is the dagged direction (take computational basis states to Ising eigenstates)
    #So we're doing bogoliubov then fourier
    Udis(h)