# CognitivePulse Pro 🧠⚡

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/OR--Tools-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="OR-Tools" />
</p>

> **Autonomous Workload Intelligence & Cognitive Capacity Optimization Platform**

CognitivePulse Pro is a full-stack, enterprise control plane engineered to mitigate developer fatigue, prevent mental burnout, and dynamically schedule complex technical tasks. By processing biometric telemetry signals alongside task complexity metrics, CognitivePulse Pro uses **Integer Linear Programming (ILP)** via Google OR-Tools to assign high-demand tasks against real-time cognitive energy capacity curves ($E(t)$).

---

## 📸 Key Features & Capabilities

- **🧠 Algorithmic Cognitive Weighting:** Automatically computes task friction scores ($W_j$) based on time constraints, technical complexity, and mental context-switching penalties.
- **⚙️ Single-Command Orchestration:** Native python supervisor (`run_all.py`) launches both the FastAPI backend server and Vite dev server concurrently with unified process management.
- **📊 Real-Time Telemetry & Optimization:** Interactive chart engine powered by **Recharts** displaying capacity curves $E(t)$ overlaid with assigned task weights.
- **🧪 Biometric & Counterfactual Simulator:** Dynamic sliders modeling Sleep Duration, HRV RMSSD, Deep Sleep ratios, and "What-If" meeting load impact.
- **🗑️ Persistent Workload Backlog:** Real-time queue table with single-item deletion, total queue wiping, and instant CORS-enabled state sync.
- **✨ Bidirectional Motion Engine:** Smooth viewport enter/exit scroll animations on all control cards.

---

## 🧮 Mathematical Model

The cognitive weight $W_j$ for any ingested task $j$ is calculated as a bounded heuristic function of time duration $T_j$:

$$W_j = \min\left(1.0, \max\left(0.2, \frac{T_j}{60}\right)\right)$$

The optimization engine computes task assignment matrix $x_{j,t} \in \{0, 1\}$ across time slots $t$ to maximize total productivity while respecting maximum energy constraints:

$$\max \sum_{j} \sum_{t} W_j \cdot E(t) \cdot x_{j,t}$$

---

## 📁 Repository Structure

```text
cognitivepulse_pro/
├── backend/
│   ├── __init__.py           # Package marker
│   └── main.py               # FastAPI application, OR-Tools solver & CORS setup
├── frontend/
│   ├── index.html            # Vite HTML document root
│   ├── package.json          # Node dependencies & dev scripts
│   ├── vite.config.js        # React plugin configuration
│   └── src/
│       ├── main.jsx          # React DOM mounting entry point
│       └── App.jsx           # Enterprise Control Plane UI
├── venv/                     # Python 3 virtual environment
├── run_all.py                # Dual-service orchestrator script
├── .gitignore                # Version control exclusions
└── README.md                 # System documentation