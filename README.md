![Banner](https://raw.githubusercontent.com/quantamu/qtamu-ibm-fliq-challenge/refs/heads/main/images/banner.png)
### Team : vivek
#### Member: 1. mk0dz (Mukul Kumar), Github- vivekpal1, email - 31vivekpal@gmail.com
#### Member: 2. viv31 (Vivel pal), Github- mk0dz, email - Mukulpal108@hotmail.com


# Quantum GUT Baryogenesis Simulation

This project simulates Grand Unified Theory (GUT) baryogenesis using quantum circuits through Qiskit.

## Overview

The simulation models early-universe baryogenesis, the process that generated the matter-antimatter asymmetry in our universe. According to Sakharov's conditions, baryogenesis requires:

1. Baryon number violation
2. C-symmetry and CP-symmetry violation 
3. Departure from thermal equilibrium

This project implements a quantum circuit model that represents these conditions and simulates the decay of X bosons into quarks and leptons with a built-in CP violation parameter.

## Files

- `gut_baryogenesis.ipynb`: Main Jupyter notebook with the simulation implementation and visualizations
- `test_gut_baryogenesis.py`: Test script to verify the correctness of the quantum circuit

## Requirements

- Python 3.7+
- Qiskit
- Qiskit-Aer
- NumPy
- Matplotlib

## Installation

```bash
# Create and activate a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install required packages
pip install qiskit qiskit-aer numpy matplotlib
```

## Usage

### Running the Notebook

Open and run the Jupyter notebook:

```bash
jupyter notebook gut_baryogenesis.ipynb
```

### Running Tests

To verify the correctness of the simulation:

```bash
# Activate virtual environment if not already activated
source env/bin/activate

# Run the tests
python test_gut_baryogenesis.py
```

## Key Components

### Quantum Circuit Structure

The simulation uses a 5-qubit system:
- Qubit 0: X boson
- Qubit 1: quark
- Qubit 2: antiquark
- Qubit 3: lepton
- Qubit 4: antilepton

### Initial State Creation

Creates an initial state with only X bosons present.

### Decay Circuit

Implements the X boson decay with CP violation parameter (epsilon):
- X → quark + lepton with probability (1+epsilon)/2
- X → antiquark + antilepton with probability (1-epsilon)/2

The decay respects conservation laws, ensuring quarks are created with leptons, and antiquarks with antileptons.

### Analysis

The simulation measures the resulting baryon asymmetry as:
- Baryon asymmetry = (N_q - N_qbar) / (N_q + N_qbar)

## Results

With the default CP violation parameter (ε = 0.1), the simulation produces a baryon asymmetry of approximately 0.118, matching theoretical expectations.

## Testing

The test script verifies:
- Initial state preparation
- CP violation asymmetry
- Zero CP violation case
- Negative CP violation case
- Conservation laws (baryon and lepton number)

## License

This project is available under the MIT License.

## Citation

If you use this code for academic purposes, please cite:

```
@misc{quantum_gut_baryogenesis,
  author = {vivek},
  title = {Quantum GUT Baryogenesis Simulation},
  year = {2025},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/yourusername/quantum-gut-baryogenesis}}
}
```

## Acknowledgements

This simulation was inspired by concepts from quantum field theory and early universe cosmology. 
