# Exact Ising Circuit

This repo contains PennyLane code to create **exact eigenstates of the transverse-field Ising model** on a 4-qubit chain using a quantum circuit. The construction is based on the methods described in [Verstraete et al., 2008](https://arxiv.org/pdf/0804.1888) and [Cervera-Lierta, 2018](https://arxiv.org/abs/1807.07112). 

Note : for 4 qubits you can just do exact diagonalization to get the eigenstates and dont really need a circuit . But this is more fun. You can run it on quantum hardware and study the circuit in its own right.

## Installation
This project uses the Python library [PennyLane](https://pennylane.ai/). Install it with:

```bash
pip install pennylane
```

## Usage

Import the module and create a device:

```python
import pennylane as qml
from pennylane import numpy as np
from Ising_circuit_4qubits import Ising

n_qubits = 4
dev = qml.device("default.qubit", wires=n_qubits)
```

Define a QNode to return the reduced density matrix of a chosen subregion:

```python
@qml.qnode(dev)
def gs_circuit(h, subregion):
    # Generate the eigenstate for transverse field h
    Ising(h)
    # Return the density matrix of the subregion
    return qml.density_matrix(wires=subregion)
```

Example for studying the first two qubits:

```python
rho = gs_circuit(h=1.0, subregion=[0,1])
print(rho)
```

Once the eigenstates are prepared, you can compute various observables like the magnetization or any correlation function. You can also study the entanglement entropy of a subregion or the negativity via the partial transpose of the density matrix. These are studied in some of the extra notebooks.

