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

## 🛠️ API Endpoint Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check & system status |
| `GET` | `/api/v1/tasks` | Fetch active task backlog queue |
| `POST` | `/api/v1/tasks` | Ingest new task vector |
| `DELETE` | `/api/v1/tasks/{id}` | Permanently delete a specific task |
| `DELETE` | `/api/v1/tasks` | Clear entire workload queue |
| `GET` | `/api/v1/analytics/error-correlation` | Fetch predicted syntax exception spikes |
| `POST` | `/api/v1/schedule/optimize` | Execute OR-Tools Branch-and-Bound solver |


## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed on your machine:
- **Python 3.10+**
- **Node.js 18+** & **npm**
- **Git**

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/diljin463/cognitivepulse_pro.git](https://github.com/diljin463/cognitivepulse_pro.git)
   cd cognitivepulse_pro

   1.Create and Activate Python Virtual Environment:
   # On Windows CMD / Git Bash
python -m venv venv

# Activate on Git Bash:
source venv/Scripts/activate

# Activate on Windows CMD:
# venv\Scripts\activate

2.Install Backend Dependencies:
pip install fastapi uvicorn ortools pydantic

3.Install Frontend Dependencies:
cd frontend
npm install
cd ..

⚡ Running the Stack
To launch the backend API (http://127.0.0.1:8000) and the React dashboard (http://localhost:5173) simultaneously in a single terminal, run:
python run_all.py

Press Ctrl + C in your terminal to perform a graceful shutdown of both services.

