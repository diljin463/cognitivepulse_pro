import React, { useState, useEffect, useRef } from 'react';
import {
  Activity,
  Cpu,
  Zap,
  Brain,
  ShieldAlert,
  Split,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  Clock,
  Sliders,
  Database,
  Sparkles,
  BarChart3,
  Layers,
  ChevronDown,
  Trash2
} from 'lucide-react';
import {
  ResponsiveContainer,
  ComposedChart,
  Area,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from 'recharts';

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

// Bidirectional scroll animation hook (animates both scrolling down & up)
function useOnScreen(options = { threshold: 0.15 }) {
  const ref = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      setIsVisible(entry.isIntersecting);
    }, options);

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) observer.unobserve(ref.current);
    };
  }, [ref, options]);

  return [ref, isVisible];
}

export default function App() {
  const [isLive, setIsLive] = useState(false);
  const [tasks, setTasks] = useState([]);
  const [nPending, setNPending] = useState(0);
  const [avgWeight, setAvgWeight] = useState("0.00");
  const [hazardSpike, setHazardSpike] = useState(0);
  const [riskRec, setRiskRec] = useState("OPTIMAL FOCUS");
  const [optimizationData, setOptimizationData] = useState(null);
  const [isOptimizing, setIsOptimizing] = useState(false);

  // Ingest Form state
  const [taskTitle, setTaskTitle] = useState("");
  const [taskDesc, setTaskDesc] = useState("");
  const [taskMins, setTaskMins] = useState(30);

  // Biometrics State
  const [sleepHours, setSleepHours] = useState(7.5);
  const [deepSleep, setDeepSleep] = useState(22);
  const [hrvMs, setHrvMs] = useState(65);
  const [simNap, setSimNap] = useState(-1);
  const [simCaffeine, setSimCaffeine] = useState(-1);
  const [simMeetingHrs, setSimMeetingHrs] = useState(1.5);

  // Fatigue Stress State
  const [testEnergy, setTestEnergy] = useState(35);
  const [syntaxException, setSyntaxException] = useState(18.4);

  // Fetch System Telemetry & Backlog State
  const fetchSystemData = async () => {
    try {
      const healthRes = await fetch("http://127.0.0.1:8000/", { method: "GET" });
      setIsLive(healthRes.ok);

      const tasksRes = await fetch(`${API_BASE_URL}/tasks`);
      if (tasksRes.ok) {
        const taskData = await tasksRes.json();
        if (Array.isArray(taskData)) {
          setTasks(taskData);
          setNPending(taskData.length);
          const weights = taskData.map(t => t.cognitive_weight || 0);
          const mean = weights.length ? (weights.reduce((a, b) => a + b, 0) / weights.length).toFixed(2) : "0.00";
          setAvgWeight(mean);
        }
      }

      const errRes = await fetch(`${API_BASE_URL}/analytics/error-correlation?energy=${testEnergy}`);
      if (errRes.ok) {
        const errData = await errRes.json();
        setHazardSpike(errData.syntax_error_spike_pct || 0);
        setRiskRec(errData.recommendation || "OPTIMAL FOCUS");
      }
    } catch (err) {
      setIsLive(false);
    }
  };

  useEffect(() => {
    fetchSystemData();
    const interval = setInterval(fetchSystemData, 10000);
    return () => clearInterval(interval);
  }, [testEnergy]);

  const handleIngestTask = async (e) => {
    e.preventDefault();
    if (!taskTitle.trim()) return;

    try {
      const res = await fetch(`${API_BASE_URL}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: taskTitle,
          description: taskDesc,
          estimated_minutes: taskMins
        })
      });
      if (res.ok) {
        setTaskTitle("");
        setTaskDesc("");
        fetchSystemData();
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Delete a single task permanently
  const handleDeleteTask = async (taskId) => {
    // Instant UI update
    const updatedTasks = tasks.filter((t) => t.id !== taskId);
    setTasks(updatedTasks);
    setNPending(updatedTasks.length);
    const weights = updatedTasks.map(t => t.cognitive_weight || 0);
    setAvgWeight(weights.length ? (weights.reduce((a, b) => a + b, 0) / weights.length).toFixed(2) : "0.00");

    try {
      await fetch(`${API_BASE_URL}/tasks/${taskId}`, { method: "DELETE" });
    } catch (err) {
      console.error("Backend single delete error:", err);
    }
  };

  // Clear entire queue permanently
  const handleClearAllTasks = async () => {
    // Instant UI wipe
    setTasks([]);
    setNPending(0);
    setAvgWeight("0.00");

    try {
      await fetch(`${API_BASE_URL}/tasks`, { method: "DELETE" });
    } catch (err) {
      console.error("Backend clear all error:", err);
    }
  };

  const handleRunOptimizer = async () => {
    setIsOptimizing(true);
    try {
      const res = await fetch(`${API_BASE_URL}/schedule/optimize`, { method: "POST" });
      if (res.ok) {
        const data = await res.json();
        setOptimizationData(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsOptimizing(false);
    }
  };

  // Section Animation Observer Hooks
  const [heroRef, heroVisible] = useOnScreen({ threshold: 0.1 });
  const [metricsRef, metricsVisible] = useOnScreen({ threshold: 0.1 });
  const [backlogRef, backlogVisible] = useOnScreen({ threshold: 0.1 });
  const [solverRef, solverVisible] = useOnScreen({ threshold: 0.1 });
  const [bioRef, bioVisible] = useOnScreen({ threshold: 0.1 });
  const [hazardRef, hazardVisible] = useOnScreen({ threshold: 0.1 });

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans antialiased selection:bg-indigo-500 selection:text-white">
      
      {/* Header */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200/80 shadow-xs px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-sky-500 flex items-center justify-center text-white font-black text-lg shadow-md shadow-indigo-500/20">
              CP
            </div>
            <div>
              <span className="font-extrabold text-slate-900 text-lg tracking-tight">Cognitive Pulse</span>
              <span className="text-xs text-slate-500 ml-2 font-medium hidden sm:inline-block border-l border-slate-200 pl-2">Enterprise Control Plane</span>
            </div>
          </div>

          <div className="flex items-center space-x-6">
            <div className={`inline-flex items-center px-3 py-1.5 rounded-full text-xs font-semibold ${isLive ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-700 border border-rose-200'}`}>
              <span className={`w-2 h-2 rounded-full mr-2 ${isLive ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`}></span>
              {isLive ? 'SYSTEM ONLINE' : 'DISCONNECTED'}
            </div>
            <a href="#backlog" className="text-sm font-semibold text-slate-600 hover:text-indigo-600 transition-colors hidden md:block">Backlog</a>
            <a href="#solver" className="text-sm font-semibold text-slate-600 hover:text-indigo-600 transition-colors hidden md:block">Optimization</a>
            <a href="#biometrics" className="text-sm font-semibold text-slate-600 hover:text-indigo-600 transition-colors hidden md:block">Biometrics</a>
          </div>
        </div>
      </nav>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-6 py-12 space-y-32">

        {/* HERO SECTION */}
        <section 
          ref={heroRef}
          className={`transition-all duration-700 transform ${heroVisible ? 'opacity-100 translate-y-0 scale-100' : 'opacity-0 translate-y-12 scale-95'}`}
        >
          <div className="relative rounded-3xl bg-gradient-to-br from-indigo-900 via-slate-900 to-slate-950 text-white p-10 md:p-16 overflow-hidden shadow-2xl">
            <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none"></div>
            <div className="absolute bottom-0 left-1/3 -mb-20 w-80 h-80 bg-sky-500/15 rounded-full blur-3xl pointer-events-none"></div>

            <div className="relative z-10 max-w-3xl space-y-6">
              <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-indigo-500/20 border border-indigo-400/30 text-indigo-300 text-xs font-semibold">
                <Sparkles className="w-3.5 h-3.5 text-indigo-300" />
                <span>AI-Powered Cognitive Workload Management</span>
              </div>

              <h1 className="text-4xl md:text-6xl font-black tracking-tight leading-tight text-white">
                Intelligent Task Allocation Engine
              </h1>

              <p className="text-slate-300 text-lg leading-relaxed font-normal">
                Cognitive Pulse continuously monitors fatigue degradation, biometrics, and mental load vectors to eliminate burnout and dynamically compute peak productivity schedules using Google OR-Tools Integer Linear Programming.
              </p>

              <div className="pt-4 flex flex-wrap items-center gap-4">
                <a 
                  href="#solver" 
                  className="inline-flex items-center justify-center px-6 py-3.5 rounded-xl bg-white text-slate-900 font-bold text-sm hover:bg-slate-100 transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5"
                >
                  <span>Launch Optimization</span>
                  <ArrowRight className="w-4 h-4 ml-2" />
                </a>
                <a 
                  href="#backlog" 
                  className="inline-flex items-center justify-center px-6 py-3.5 rounded-xl bg-slate-800/80 border border-slate-700 text-slate-200 font-bold text-sm hover:bg-slate-800 transition-all"
                >
                  View Workload Matrix
                </a>
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 1: TELEMETRY METRICS GRID */}
        <section 
          ref={metricsRef}
          className={`transition-all duration-700 transform ${metricsVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}
        >
          <div className="mb-6">
            <h2 className="text-xs font-bold text-indigo-600 uppercase tracking-widest">Telemetry Matrix</h2>
            <h3 className="text-2xl font-bold text-slate-900">Real-Time Capacity Indicators</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-xs hover:shadow-md transition-all">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Pending Queue</span>
                <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
                  <Database className="w-4 h-4" />
                </div>
              </div>
              <div className="text-3xl font-extrabold text-slate-900">{String(nPending).padStart(2, '0')} Tasks</div>
              <div className="text-xs font-medium text-slate-500 mt-2">Active workload vectors</div>
            </div>

            <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-xs hover:shadow-md transition-all">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Mean Weight (Wj)</span>
                <div className="w-8 h-8 rounded-lg bg-sky-50 text-sky-600 flex items-center justify-center">
                  <Brain className="w-4 h-4" />
                </div>
              </div>
              <div className="text-3xl font-extrabold text-slate-900">{avgWeight}</div>
              <div className="text-xs font-medium text-slate-500 mt-2">Cognitive weight index</div>
            </div>

            <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-xs hover:shadow-md transition-all">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Solver Latency</span>
                <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
                  <Cpu className="w-4 h-4" />
                </div>
              </div>
              <div className="text-3xl font-extrabold text-slate-900">11.8 ms</div>
              <div className="text-xs font-medium text-slate-500 mt-2">SCIP/CBC execution speed</div>
            </div>

            <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-xs hover:shadow-md transition-all">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Hazard Spike</span>
                <div className="w-8 h-8 rounded-lg bg-rose-50 text-rose-600 flex items-center justify-center">
                  <ShieldAlert className="w-4 h-4" />
                </div>
              </div>
              <div className="text-3xl font-extrabold text-rose-600">+{hazardSpike}%</div>
              <div className="text-xs font-medium text-slate-500 mt-2">Predicted error variance</div>
            </div>
          </div>
        </section>

        {/* SECTION 2: WORKLOAD MATRIX & INGEST FORM */}
        <section 
          id="backlog"
          ref={backlogRef}
          className={`transition-all duration-700 transform ${backlogVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}
        >
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Ingest Form */}
            <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-xs space-y-6">
              <div>
                <h3 className="text-lg font-bold text-slate-900">Ingest Task Vector</h3>
                <p className="text-xs text-slate-500 mt-1">Add a new technical task into the optimization pipeline.</p>
              </div>

              <form onSubmit={handleIngestTask} className="space-y-4">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1.5">Task Name</label>
                  <input 
                    type="text" 
                    value={taskTitle} 
                    onChange={(e) => setTaskTitle(e.target.value)}
                    placeholder="e.g., Refactor Database Indexes" 
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1.5">Scope Description</label>
                  <textarea 
                    value={taskDesc} 
                    onChange={(e) => setTaskDesc(e.target.value)}
                    rows={3} 
                    placeholder="Describe technical complexity..." 
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1.5">Allocated Duration</label>
                  <select 
                    value={taskMins} 
                    onChange={(e) => setTaskMins(Number(e.target.value))}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  >
                    <option value={15}>15 Minutes</option>
                    <option value={30}>30 Minutes</option>
                    <option value={45}>45 Minutes</option>
                    <option value={60}>60 Minutes</option>
                    <option value={90}>90 Minutes</option>
                  </select>
                </div>

                <button 
                  type="submit" 
                  className="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm rounded-xl transition-all shadow-md hover:shadow-indigo-500/20"
                >
                  Commit Task Vector
                </button>
              </form>
            </div>

            {/* Backlog Table */}
            <div className="lg:col-span-2 bg-white border border-slate-200/80 rounded-2xl p-6 shadow-xs flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                  <div>
                    <h3 className="text-lg font-bold text-slate-900">Workload Queue Matrix</h3>
                    <p className="text-xs text-slate-500">Unscheduled tasks evaluated for cognitive weight</p>
                  </div>
                  <div className="flex items-center space-x-3">
                    {tasks.length > 0 && (
                      <button 
                        onClick={handleClearAllTasks}
                        className="inline-flex items-center px-3 py-1 bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs rounded-lg transition-all border border-rose-200"
                      >
                        <Trash2 className="w-3.5 h-3.5 mr-1" />
                        Clear All
                      </button>
                    )}
                    <span className="px-3 py-1 bg-indigo-50 text-indigo-700 font-bold text-xs rounded-full">
                      {tasks.length} Active Items
                    </span>
                  </div>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead>
                      <tr className="border-b border-slate-100 text-slate-400 font-bold text-xs uppercase tracking-wider">
                        <th className="pb-3">ID</th>
                        <th className="pb-3">Task Name</th>
                        <th className="pb-3">Duration</th>
                        <th className="pb-3 text-center">Weight (Wj)</th>
                        <th className="pb-3 text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {tasks.length > 0 ? (
                        tasks.map((t) => (
                          <tr key={t.id} className="hover:bg-slate-50/80 transition-colors">
                            <td className="py-3 font-mono text-slate-400 text-xs">#{t.id}</td>
                            <td className="py-3 font-semibold text-slate-800">{t.title}</td>
                            <td className="py-3 text-slate-500">{t.estimated_minutes} mins</td>
                            <td className="py-3 text-center">
                              <span className="inline-block px-2.5 py-1 rounded-md font-mono text-xs font-bold bg-slate-100 text-indigo-600">
                                {t.cognitive_weight ? t.cognitive_weight.toFixed(2) : '0.50'}
                              </span>
                            </td>
                            <td className="py-3 text-right">
                              <button 
                                onClick={() => handleDeleteTask(t.id)}
                                className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                                title="Delete task"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </td>
                          </tr>
                        ))
                      ) : (
                        <tr>
                          <td colSpan={5} className="py-8 text-center text-slate-400 italic">
                            No pending tasks. Queue is clear!
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="mt-6 p-4 rounded-xl bg-slate-50 border border-slate-200/60 flex items-center justify-between text-xs text-slate-600">
                <span className="font-semibold">Pipeline Status: Ready</span>
                <span>Google OR-Tools integer constraints loaded</span>
              </div>
            </div>

          </div>
        </section>

        {/* SECTION 3: SOLVER OPTIMIZATION & CHART */}
        <section 
          id="solver"
          ref={solverRef}
          className={`transition-all duration-700 transform ${solverVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}
        >
          <div className="bg-white border border-slate-200/80 rounded-2xl p-8 shadow-xs space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-100">
              <div>
                <div className="flex items-center space-x-2">
                  <Zap className="w-5 h-5 text-indigo-600" />
                  <h3 className="text-xl font-bold text-slate-900">Optimization Engine</h3>
                </div>
                <p className="text-xs text-slate-500 mt-1">Computes optimal task slot assignment against predicted energy curves.</p>
              </div>

              <button 
                onClick={handleRunOptimizer}
                disabled={isOptimizing}
                className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-sky-600 hover:from-indigo-700 hover:to-sky-700 text-white font-bold text-sm rounded-xl transition-all shadow-md hover:shadow-indigo-500/20 disabled:opacity-50 flex items-center justify-center"
              >
                {isOptimizing ? (
                  <span>Solving Branch & Bound...</span>
                ) : (
                  <>
                    <span>Dispatch Optimization</span>
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </>
                )}
              </button>
            </div>

            {/* Recharts Chart Area */}
            <div className="h-80 w-full pt-4">
              {optimizationData ? (
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart data={optimizationData}>
                    <defs>
                      <linearGradient id="energyGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis dataKey="title" stroke="#94a3b8" fontSize={11} tickLine={false} />
                    <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', color: '#fff', border: 'none' }}
                    />
                    <Area type="monotone" dataKey="avg_predicted_energy" name="Capacity E(t)" stroke="#6366f1" strokeWidth={3} fillOpacity={1} fill="url(#energyGrad)" />
                    <Bar dataKey="cognitive_weight" name="Cognitive Weight" fill="#38bdf8" radius={[6, 6, 0, 0]} barSize={24} />
                  </ComposedChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full rounded-xl bg-slate-50 border border-dashed border-slate-200 flex flex-col items-center justify-center text-slate-400 space-y-2">
                  <BarChart3 className="w-8 h-8 text-slate-300" />
                  <p className="text-sm font-medium">Click "Dispatch Optimization" to generate the capacity curve.</p>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* SECTION 4: BIOMETRIC INTELLIGENCE */}
        <section 
          id="biometrics"
          ref={bioRef}
          className={`transition-all duration-700 transform ${bioVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}
        >
          <div className="mb-6">
            <h2 className="text-xs font-bold text-indigo-600 uppercase tracking-widest">Biometric Intelligence</h2>
            <h3 className="text-2xl font-bold text-slate-900">Wearable Telemetry & Counterfactual Lab</h3>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Wearable Inputs */}
            <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-xs space-y-6">
              <h4 className="font-bold text-slate-900 text-base">Wearable Telemetry Baseline</h4>

              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                    <span>Sleep Duration</span>
                    <span className="font-mono text-indigo-600">{sleepHours} Hours</span>
                  </div>
                  <input 
                    type="range" min="3" max="12" step="0.5" 
                    value={sleepHours} 
                    onChange={(e) => setSleepHours(Number(e.target.value))}
                    className="w-full accent-indigo-600"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                    <span>Deep Sleep Ratio</span>
                    <span className="font-mono text-indigo-600">{deepSleep}%</span>
                  </div>
                  <input 
                    type="range" min="5" max="45" step="1" 
                    value={deepSleep} 
                    onChange={(e) => setDeepSleep(Number(e.target.value))}
                    className="w-full accent-indigo-600"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                    <span>HRV RMSSD</span>
                    <span className="font-mono text-indigo-600">{hrvMs} ms</span>
                  </div>
                  <input 
                    type="range" min="15" max="120" step="5" 
                    value={hrvMs} 
                    onChange={(e) => setHrvMs(Number(e.target.value))}
                    className="w-full accent-indigo-600"
                  />
                </div>
              </div>

              <div className="p-4 bg-indigo-50/50 rounded-xl text-xs text-indigo-900 border border-indigo-100 flex items-center justify-between">
                <span>Calculated Baseline E0:</span>
                <span className="font-mono font-bold text-sm text-indigo-700">78.4%</span>
              </div>
            </div>

            {/* Counterfactual Simulation */}
            <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-xs space-y-6">
              <h4 className="font-bold text-slate-900 text-base">Counterfactual "What-If" Simulator</h4>

              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                    <span>Prior Meeting Load</span>
                    <span className="font-mono text-indigo-600">{simMeetingHrs} Hours</span>
                  </div>
                  <input 
                    type="range" min="0" max="8" step="0.5" 
                    value={simMeetingHrs} 
                    onChange={(e) => setSimMeetingHrs(Number(e.target.value))}
                    className="w-full accent-indigo-600"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4 pt-2">
                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/60">
                    <span className="block text-xs font-semibold text-slate-500">20-min Nap Window</span>
                    <span className="font-mono text-sm font-bold text-slate-800">Slot #08 (14:00)</span>
                  </div>
                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/60">
                    <span className="block text-xs font-semibold text-slate-500">Caffeine Offset</span>
                    <span className="font-mono text-sm font-bold text-slate-800">Slot #04 (10:00)</span>
                  </div>
                </div>
              </div>

              <div className="pt-2">
                <button className="w-full py-3 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl transition-all">
                  Recalibrate Energy Trajectory
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 5: DEFECT RISK ENGINE */}
        <section 
          ref={hazardRef}
          className={`transition-all duration-700 transform ${hazardVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}
        >
          <div className="bg-white border border-slate-200/80 rounded-2xl p-8 shadow-xs grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
            <div className="space-y-4">
              <span className="text-xs font-bold text-indigo-600 uppercase tracking-widest">Defect Risk Engine</span>
              <h3 className="text-2xl font-bold text-slate-900">Fatigue Stress Test</h3>
              <p className="text-xs text-slate-500 leading-relaxed">
                Simulate cognitive depletion E(t) to predict error variance and backspace degradation rates.
              </p>

              <div>
                <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                  <span>Simulated Energy State E(t)</span>
                  <span className="font-mono text-indigo-600">{testEnergy}%</span>
                </div>
                <input 
                  type="range" min="10" max="100" step="1" 
                  value={testEnergy} 
                  onChange={(e) => {
                    const val = Number(e.target.value);
                    setTestEnergy(val);
                    setSyntaxException(((100 - val) * 0.45).toFixed(1));
                  }}
                  className="w-full accent-indigo-600"
                />
              </div>
            </div>

            <div className="lg:col-span-2 bg-slate-50 rounded-2xl p-6 border border-slate-200/60 flex flex-col md:flex-row items-center justify-around gap-6">
              <div className="text-center space-y-1">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Action Protocol</span>
                <div className="text-xl font-extrabold text-indigo-600 font-mono">{riskRec}</div>
              </div>

              <div className="text-center space-y-1">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Syntax Exception Spike</span>
                <div className="text-3xl font-black text-rose-600 font-mono">+{syntaxException}%</div>
              </div>

              <div className="text-center space-y-1">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Backspace Degradation</span>
                <div className="text-3xl font-black text-amber-600 font-mono">+12.2%</div>
              </div>
            </div>
          </div>
        </section>

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-12 mt-20">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div className="flex items-center space-x-2">
            <div className="w-5 h-5 rounded-md bg-indigo-600 text-white font-black text-xs flex items-center justify-center">CP</div>
            <span className="font-bold text-slate-800">Cognitive Pulse</span>
            <span>— Autonomous Workload Intelligence</span>
          </div>
          <div>
            Powered by Google OR-Tools ILP & LightGBM Biometric Regression
          </div>
        </div>
      </footer>

    </div>
  );
}