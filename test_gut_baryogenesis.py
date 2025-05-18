import unittest
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

class TestGutBaryogenesis(unittest.TestCase):
    """Test class for GUT baryogenesis quantum circuit simulation."""
    
    def create_initial_state(self, x_boson=1, quark=0, lepton=0, antiquark=0, antilepton=0):
        """Create the initial state with specified particle configuration."""
        # Create a 5-qubit system
        # Qubit 0: X boson
        # Qubit 1: quark (0=none, 1=present)
        # Qubit 2: antiquark (0=none, 1=present)
        # Qubit 3: lepton (0=none, 1=present)
        # Qubit 4: antilepton (0=none, 1=present)
        
        qc = QuantumCircuit(5)
        
        # Set X boson
        if x_boson:
            qc.x(0)
        
        # Set quark or antiquark
        if quark:
            qc.x(1)
        if antiquark:
            qc.x(2)
            
        # Set lepton or antilepton
        if lepton:
            qc.x(3)
        if antilepton:
            qc.x(4)
            
        return qc
    
    def create_gut_decay_circuit(self, epsilon=0.1):
        """Create a circuit that models X boson decay with CP violation."""
        # Calculate probabilities based on CP violation
        # X → q + l with probability (1+epsilon)/2
        # X → q̄ + l̄ with probability (1-epsilon)/2
        
        p_ql = (1 + epsilon)/2
        p_qlbar = (1 - epsilon)/2
        
        # Convert probabilities to rotation angles
        theta = 2 * np.arcsin(np.sqrt(p_ql))
        
        # Create the circuit
        qc = QuantumCircuit(5)
        
        # First, create a superposition of quark+lepton vs antiquark+antilepton
        # based on the CP violation parameter
        qc.cry(theta, 0, 1)  # Rotate quark based on epsilon
        
        # Now ensure lepton follows quark (they must be created together)
        qc.cx(1, 3)  # If quark is created, lepton must be created
        
        # If no quark was created, then we need antiquark+antilepton
        # Use a NOT on quark to determine this
        qc.x(1)
        qc.cx(1, 2)  # Create antiquark if quark was not created
        qc.cx(1, 4)  # Create antilepton if quark was not created
        qc.x(1)  # Restore quark state
        
        # X boson is annihilated after decay
        # If either decay happened, the X boson should be gone
        qc.cx(1, 0)  # If quark is created, X is annihilated
        qc.cx(2, 0)  # If antiquark is created, X is annihilated
        qc.x(0)      # Flip the X boson qubit (now X=0 means it has decayed)
        
        return qc
    
    def run_gut_simulation(self, epsilon=0.1, num_shots=1000):
        """Run the GUT baryogenesis simulation and return results."""
        # Create the initial state
        qc = self.create_initial_state(x_boson=1)
        
        # Add the decay circuit
        decay_circuit = self.create_gut_decay_circuit(epsilon)
        qc = qc.compose(decay_circuit)
        
        # Measure all qubits
        qc.measure_all()
        
        # Run the simulation
        simulator = AerSimulator()
        transpiled_qc = transpile(qc, simulator)
        job = simulator.run(transpiled_qc, shots=num_shots)
        result = job.result()
        counts = result.get_counts()
        
        return counts, qc
    
    def analyze_gut_results(self, counts):
        """
        Analyze the results to calculate baryon asymmetry.
        
        Parameters:
        -----------
        counts : dict
            Result counts from the simulation
        
        Returns:
        --------
        asymmetry : float
            The baryon asymmetry (N_q - N_qbar)/(N_q + N_qbar)
        quark_count : int
            Number of quarks produced
        antiquark_count : int
            Number of antiquarks produced
        """
        quark_count = 0
        antiquark_count = 0
        
        # Format is |antilepton, lepton, antiquark, quark, X>
        for outcome, count in counts.items():
            # Check if quark exists (4th bit from right is 1)
            if outcome[-2] == '1':
                quark_count += count
            
            # Check if antiquark exists (3rd bit from right is 1)
            if outcome[-3] == '1':
                antiquark_count += count
        
        total = quark_count + antiquark_count
        if total > 0:
            asymmetry = (quark_count - antiquark_count) / total
        else:
            asymmetry = 0
            
        return asymmetry, quark_count, antiquark_count
    
    def test_initial_state(self):
        """Test that the initial state has X boson and nothing else."""
        qc = self.create_initial_state(x_boson=1)
        qc.measure_all()
        
        simulator = AerSimulator()
        result = simulator.run(qc).result()
        counts = result.get_counts()
        
        # Should have X boson (rightmost bit = 1) and nothing else
        self.assertTrue('00001' in counts)
        self.assertEqual(len(counts), 1)  # Only one outcome should be possible
    
    def test_cp_violation_asymmetry(self):
        """Test that CP violation parameter creates the expected asymmetry."""
        # Test with epsilon = 0.2 (strong CP violation)
        epsilon = 0.2
        counts, _ = self.run_gut_simulation(epsilon=epsilon, num_shots=10000)
        asymmetry, quark_count, antiquark_count = self.analyze_gut_results(counts)
        
        # Asymmetry should be approximately epsilon (within reasonable statistical fluctuation)
        # For 10000 runs, we expect to be within about 0.05 of the true value
        self.assertAlmostEqual(asymmetry, epsilon, delta=0.05)
        
        # Total quarks and antiquarks should be non-zero
        self.assertGreater(quark_count + antiquark_count, 0)
        
        # More quarks than antiquarks with positive epsilon
        self.assertGreater(quark_count, antiquark_count)
    
    def test_zero_cp_violation(self):
        """Test that zero CP violation produces no asymmetry."""
        epsilon = 0.0
        counts, _ = self.run_gut_simulation(epsilon=epsilon, num_shots=10000)
        asymmetry, quark_count, antiquark_count = self.analyze_gut_results(counts)
        
        # Asymmetry should be approximately zero (within statistical fluctuation)
        self.assertAlmostEqual(asymmetry, 0.0, delta=0.05)
        
        # Quarks and antiquarks should be roughly equal
        self.assertAlmostEqual(quark_count / (quark_count + antiquark_count), 0.5, delta=0.05)
    
    def test_negative_cp_violation(self):
        """Test that negative CP violation produces negative asymmetry."""
        epsilon = -0.2
        counts, _ = self.run_gut_simulation(epsilon=epsilon, num_shots=10000)
        asymmetry, quark_count, antiquark_count = self.analyze_gut_results(counts)
        
        # Asymmetry should be approximately epsilon (within reasonable statistical fluctuation)
        self.assertAlmostEqual(asymmetry, epsilon, delta=0.05)
        
        # More antiquarks than quarks with negative epsilon
        self.assertGreater(antiquark_count, quark_count)
    
    def test_conservation_laws(self):
        """Test that baryon and lepton numbers are conserved in each decay."""
        counts, _ = self.run_gut_simulation(num_shots=10000)
        
        # Format is |antilepton, lepton, antiquark, quark, X>
        for outcome, count in counts.items():
            # Skip cases where X boson still exists
            if outcome[-1] == '1':
                continue
                
            has_quark = outcome[-2] == '1'
            has_antiquark = outcome[-3] == '1'
            has_lepton = outcome[-4] == '1'
            has_antilepton = outcome[-5] == '1'
            
            # If decay happened, it should be q+l or qbar+lbar
            if has_quark:
                self.assertTrue(has_lepton, f"Found quark without lepton in outcome {outcome}")
                self.assertFalse(has_antiquark, f"Found quark with antiquark in outcome {outcome}")
                self.assertFalse(has_antilepton, f"Found quark with antilepton in outcome {outcome}")
            
            if has_antiquark:
                self.assertTrue(has_antilepton, f"Found antiquark without antilepton in outcome {outcome}")
                self.assertFalse(has_quark, f"Found antiquark with quark in outcome {outcome}")
                self.assertFalse(has_lepton, f"Found antiquark with lepton in outcome {outcome}")

if __name__ == '__main__':
    unittest.main() 