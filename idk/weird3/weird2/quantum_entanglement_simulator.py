import numpy as np
from qiskit import QuantumCircuit, Aer, execute

class QuantumEntanglementSimulator:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.circuit = QuantumCircuit(num_qubits, num_qubits)

    def create_bell_state(self):
        self.circuit.h(0)  # Apply Hadamard gate to the first qubit
        self.circuit.cx(0, 1)  # CNOT with control qubit 0 and target qubit 1

    def measure(self):
        self.circuit.measure_all()

    def run_simulation(self, shots=1000):
        backend = Aer.get_backend('qasm_simulator')
        job = execute(self.circuit, backend, shots=shots)
        result = job.result()
        counts = result.get_counts(self.circuit)
        return counts

    def entanglement_entropy(self, density_matrix):
        eigenvalues = np.linalg.eigvals(density_matrix)
        entropy = -np.sum(eigenvalues * np.log2(eigenvalues + 1e-10))
        return entropy.real

quantum_sim = QuantumEntanglementSimulator(2)
quantum_sim.create_bell_state()
quantum_sim.measure()
results = quantum_sim.run_simulation()
