# Q-Dx — SIH26139 Prototype

Q-Dx is a research prototype for **Smart India Hackathon 2026, SIH26139: Hybrid Quantum Machine Learning Platform for Early Disease Detection**. It combines classical ML baselines with a variational quantum classifier (VQC), a Streamlit dashboard, benchmark reporting, and explainability views.

> **Clinical safety:** This is a research and demonstration system only. It uses the Wisconsin Diagnostic Breast Cancer benchmark dataset and must not be used for diagnosis, triage, or clinical decision-making.

## What is included

- Reproducible preprocessing for 569 breast-cancer benchmark samples and 30 input features.
- Classical baselines: Logistic Regression, SVM, Random Forest, and XGBoost.
- A 4-qubit, 2-layer PennyLane VQC running on the local simulator.
- A Streamlit dashboard for prediction, benchmarking, explainability, circuit inspection, and backend status.
- Optional IBM Quantum credential detection. The dashboard never claims a local simulation was executed on hardware.

## Quick start (Windows PowerShell)

Install Python 3.11 or newer, then run from the project root:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\run.ps1 -Setup
.\run.ps1 -Train
.\run.ps1
```

The first command creates a clean `.venv` independent of any checked-in virtual environment. The training command produces preprocessing artifacts, model files, metrics, a benchmark report, and quantum parameters. Launching `run.ps1` opens the dashboard.

For a fast classical-only demonstration:

```powershell
.\run.ps1 -Train -SkipQuantum
.\run.ps1
```

Run the automated checks with:

```powershell
.\run.ps1 -Test
```

## IBM Quantum

The platform works fully with its local simulator. To display available IBM backends, configure an IBM Quantum token before starting the dashboard:

```powershell
$env:IBM_QUANTUM_TOKEN = "your-token"
# Optional: $env:IBM_QUANTUM_INSTANCE = "hub/group/project"
```

The current prototype discovers and reports the hardware backend, but model execution remains local until the PennyLane VQC is explicitly transpiled and submitted through Qiskit Runtime. This limitation is deliberately surfaced in the UI and code.
