import React, { useState, useEffect, useRef, useMemo } from 'react';
import {
  Activity,
  Cpu,
  Layers,
  Plus,
  RefreshCw,
  AlertTriangle,
  Clock,
  Database,
  Zap,
  ChevronRight,
  Play,
  Brain,
  ShieldAlert,
  Moon,
  Coffee,
  Sparkles,
  Radio,
  Gauge,
  Trash2,
  Filter,
  ChevronDown,
  ArrowRight,
  ShieldCheck,
  Layers3,
  BarChart3,
  CheckCircle2,
  TrendingUp,
  Sliders,
  Sun,
  Eye,
  Check
} from 'lucide-react';
import {
  AreaChart,
  Area,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  XAxis,
  YAxis
} from 'recharts';

const INITIAL_TASKS = [
  {
    id: 101,
    title: 'OPTIMIZE_DUCKDB_INDEXES',
    description: 'Re-index analytical telemetry vectors in local columnar engine for sub-10ms query scans',
    estimated_minutes: 45,
    cognitive_weight: 0.85,
    category: 'DATABASE',
    status: 'QUEUED'
  },
  {
    id: 102,
    title: 'ASYNC_WEBSOCKET_QUEUE_DECOUPLING',
    description: 'Migrate blocking event handlers into non-blocking asyncio event loops with backpressure',
    estimated_minutes: 60,
    cognitive_weight: 0.78,
    category: 'BACKEND',
    status: 'QUEUED'
  },
  {
    id: 103,
    title: 'EVALUATE_LIGHTGBM_SHAP_ATTRIBUTION',
    description: 'Calculate feature importance attribution across sleep HRV decay and circadian inputs',
    estimated_minutes: 30,
    cognitive_weight: 0.42,
    category: 'ML_PIPELINE',
    status: 'QUEUED'
  },
  {
    id: 104,
    title: 'EMBEDDING_TRANSFORM_CACHE_WARMING',
    description: 'Pre-warm Sentence-Transformers embedding vectors in persistent SQLite cache layer',
    estimated_minutes: 15,
    cognitive_weight: 0.31,
    category: 'NLP',
    status: 'COMPLETED'
  },
  {
    id: 105,
    title: 'OR_TOOLS_ILP_RECONCILIATION',
    description: 'Verify 32-slot solver branch-and-bound constraint parameters for multi-worker schedules',
    estimated_minutes: 90,
    cognitive_weight: 0.92,
    category: 'SOLVER',
    status: 'QUEUED'
  }
];

const INITIAL_SCHEDULE = [
  { slot: 0, time: '09:00 AM', title: 'OR_TOOLS_ILP_RECONCILIATION', avg_predicted_energy: 94.2, cognitive_weight: 0.92, status: 'OPTIMAL' },
  { slot: 1, time: '10:30 AM', title: 'OPTIMIZE_DUCKDB_INDEXES', avg_predicted_energy: 88.5, cognitive_weight: 0.85, status: 'OPTIMAL' },
  { slot: 2, time: '11:15 AM', title: 'ASYNC_WEBSOCKET_QUEUE_DECOUPLING', avg_predicted_energy: 79.1, cognitive_weight: 0.78, status: 'STABLE' },
  { slot: 3, time: '01:00 PM', title: 'EVALUATE_LIGHTGBM_SHAP_ATTRIBUTION', avg_predicted_energy: 68.4, cognitive_weight: 0.42, status: 'STABLE' },
  { slot: 4, time: '02:30 PM', title: 'EMBEDDING_TRANSFORM_CACHE_WARMING', avg_predicted_energy: 55.0, cognitive_weight: 0.31, status: 'STABLE' },
  { slot: 5, time: '03:30 PM', title: 'CIRCADIAN_REST_BUFFER', avg_predicted_energy: 42.1, cognitive_weight: 0.10, status: 'RECOVERY' },
  { slot: 6, time: '04:00 PM', title: 'REFRACTOR_TEST_SUITE', avg_predicted_energy: 36.8, cognitive_weight: 0.50, status: 'HAZARD_RISK' }
];

function useScrollObserver(options = {}) {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setIsVisible(true);
      }
    }, { threshold: 0.15, ...options });

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return [ref, isVisible];
}

function Navigation({ activeSection, isLive, onIngestClick }) {
  const navLinks = [
    { id: 'intro', label: 'Intro' },
    { id: 'telemetry', label: 'Telemetry' },
    { id: 'backlog', label: 'Backlog' },
    { id: 'solver', label: 'ILP Solver' },
    { id: 'biometrics', label: 'Biometrics' },
    { id: 'hazard', label: 'Hazard Engine' },
    { id: 'decomposition', label: 'Decomposition' }
  ];

  const scrollToSection = (id) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <header className="fixed top-6 left-0 right-0 z-50 px-4 md:px-8 max-w-7xl mx-auto">
      <div className="bg-white/80 backdrop-blur-2xl border border-slate-200/80 rounded-full px-6 py-3.5 shadow-[0_10px_35px_rgba(0,0,0,0.06)] flex items-center justify-between transition-all duration-300 hover:border-indigo-300">
        
        {/* Brand Logo */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-indigo-600 via-violet-600 to-cyan-500 p-[2px] shadow-[0_4px_15px_rgba(79,70,229,0.25)]">
            <div className="w-full h-full bg-white rounded-full flex items-center justify-center">
              <Zap className="w-4 h-4 text-indigo-600" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-slate-900 text-sm tracking-tight font-sans">Cognitive Pulse</span>
            </div>
          </div>
        </div>

        {/* Navigation Bar Links */}
        <nav className="hidden lg:flex items-center gap-1 bg-slate-100/70 p-1.5 rounded-full border border-slate-200/60">
          {navLinks.map((link) => {
            const isActive = activeSection === link.id;
            return (
              <button
                key={link.id}
                onClick={() => scrollToSection(link.id)}
                className={`px-4 py-1.5 rounded-full text-xs font-sans font-semibold transition-all duration-300 ${
                  isActive
                    ? 'bg-white text-indigo-600 shadow-[0_4px_12px_rgba(0,0,0,0.08)] border border-slate-200/80'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                }`}
              >
                {link.label}
              </button>
            );
          })}
        </nav>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-xs font-sans font-semibold px-3.5 py-1.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
            <span className="relative flex h-2 w-2">
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full ${isLive ? 'bg-emerald-400' : 'bg-rose-400'} opacity-75`}></span>
              <span className={`relative inline-flex rounded-full h-2 w-2 ${isLive ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
            </span>
            <span className="hidden sm:inline">{isLive ? 'SYSTEM ONLINE' : 'OFFLINE'}</span>
          </div>

          <button
            onClick={onIngestClick}
            className="px-4 py-1.5 rounded-full text-xs font-sans font-bold text-white bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-700 hover:to-violet-700 shadow-[0_4px_15px_rgba(79,70,229,0.3)] transition-all duration-300 flex items-center gap-1.5 active:scale-95"
          >
            <Plus className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Ingest Task</span>
          </button>
        </div>
      </div>
    </header>
  );
}

function HeroIntroSection({ onExplore, onRunSolver }) {
  const [ref, isVisible] = useScrollObserver();

  return (
    <section id="intro" ref={ref} className="min-h-screen pt-32 pb-20 flex flex-col justify-center relative overflow-hidden">
      <div className="absolute top-12 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-gradient-to-tr from-indigo-200/40 via-sky-200/40 to-violet-200/40 blur-[120px] rounded-full pointer-events-none -z-10"></div>
      <div className="absolute top-1/3 right-10 w-[400px] h-[300px] bg-emerald-200/30 blur-[100px] rounded-full pointer-events-none -z-10"></div>

      <div className={`grid grid-cols-1 lg:grid-cols-12 gap-12 items-center transition-all duration-1000 transform ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}>
        
        {/* Hero Left Briefing Text */}
        <div className="lg:col-span-7 space-y-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-50 border border-indigo-200/80 text-indigo-700 text-xs font-sans font-semibold uppercase tracking-wider shadow-sm">
            <Sparkles className="w-4 h-4 text-indigo-600 animate-pulse" />
            <span>Next-Gen Human Ergonomics & Biometric Orchestration</span>
          </div>

          <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-slate-900 tracking-tight font-sans leading-[1.08]">
            Cognitive Pulse. <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-600">
              Biological Focus Control.
            </span>
          </h1>

          <div className="space-y-4 text-base md:text-lg text-slate-600 leading-relaxed font-sans max-w-2xl">
            <p>
              Cognitive Pulse is a modern real-time telemetry platform engineered to align high-density software production with individual biological focus capacity.
            </p>
            <p className="text-slate-500 text-sm md:text-base">
              By fusing wearable biometric metrics (circadian sleep architecture, HRV decay, deep rest ratios) with active IDE typing dynamics and <strong>Google OR-Tools Integer Linear Programming (ILP)</strong>, Cognitive Pulse calculates predicted cognitive energy <span className="text-indigo-600 font-semibold">E(t)</span> to schedule heavy architectural engineering tasks precisely when focus is at its biological peak.
            </p>
          </div>

          {/* Action Triggers */}
          <div className="pt-4 flex flex-wrap items-center gap-4">
            <button
              onClick={onRunSolver}
              className="px-8 py-4 rounded-full text-sm font-sans font-bold text-white bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-600 hover:shadow-[0_8px_25px_rgba(79,70,229,0.35)] transition-all duration-300 flex items-center gap-2.5 active:scale-95"
            >
              <Play className="w-4 h-4 fill-white" />
              <span>DISPATCH ILP SOLVER</span>
            </button>

            <button
              onClick={onExplore}
              className="px-8 py-4 rounded-full text-sm font-sans font-semibold text-slate-700 bg-white border border-slate-200 hover:border-indigo-300 hover:text-indigo-600 transition shadow-sm flex items-center gap-2 group"
            >
              <span>Explore Telemetry Matrix</span>
              <ChevronDown className="w-4 h-4 text-indigo-600 group-hover:translate-y-1 transition" />
            </button>
          </div>
        </div>

        {/* Hero Right Showcase Card */}
        <div className="lg:col-span-5 relative">
          <div className="bg-white/80 backdrop-blur-2xl border border-slate-200/90 rounded-3xl p-6 shadow-[0_20px_50px_rgba(0,0,0,0.08)] space-y-6 relative overflow-hidden group hover:shadow-[0_25px_60px_rgba(79,70,229,0.15)] transition-all duration-500">
            
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-rose-400"></div>
                <div className="w-3 h-3 rounded-full bg-amber-400"></div>
                <div className="w-3 h-3 rounded-full bg-emerald-400"></div>
              </div>
              <span className="text-xs font-sans text-slate-500 font-semibold">Cognitive Telemetry Engine</span>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-center text-xs font-sans">
                <span className="text-slate-500 font-semibold flex items-center gap-1.5">
                  <Activity className="w-4 h-4 text-indigo-600 animate-pulse" /> Live Energy Trajectory E(t)
                </span>
                <span className="text-emerald-600 font-bold bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 rounded-full">
                  92.4% Optimal
                </span>
              </div>

              <div className="h-32 bg-slate-50/80 rounded-2xl border border-slate-100 p-3 relative flex items-end justify-between gap-1 overflow-hidden">
                {[88, 92, 95, 91, 86, 78, 84, 89, 93, 87, 82, 75, 79, 85, 91, 88].map((val, i) => (
                  <div
                    key={i}
                    className="w-full bg-gradient-to-t from-indigo-600 to-violet-500 rounded-t-md transition-all duration-500"
                    style={{ height: `${val}%` }}
                  ></div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 pt-2">
              <div className="p-3.5 rounded-2xl bg-indigo-50/60 border border-indigo-100">
                <span className="text-[11px] font-bold text-indigo-700 block uppercase">OR-Tools ILP</span>
                <span className="text-xs text-indigo-900 font-medium">32-Slot Optimization</span>
              </div>
              <div className="p-3.5 rounded-2xl bg-purple-50/60 border border-purple-100">
                <span className="text-[11px] font-bold text-purple-700 block uppercase">LightGBM Engine</span>
                <span className="text-xs text-purple-900 font-medium">Circadian Fatigue Decay</span>
              </div>
            </div>

          </div>
        </div>

      </div>
    </section>
  );
}

function TelemetrySection({ tasks, avgWeight, isLive }) {
  const [ref, isVisible] = useScrollObserver();

  return (
    <section id="telemetry" ref={ref} className="py-28 border-t border-slate-200/60">
      <div className={`space-y-12 transition-all duration-1000 transform ${isVisible ? 'translate-x-0 opacity-100' : '-translate-x-24 opacity-0'}`}>
        
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 text-indigo-700 text-xs font-sans font-bold uppercase tracking-widest bg-indigo-50 px-3.5 py-1 rounded-full border border-indigo-200">
            <Radio className="w-3.5 h-3.5 text-indigo-600 animate-pulse" />
            <span>Live Telemetry Matrix</span>
          </div>
          <h2 className="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight font-sans">
            Real-Time Telemetry Pipeline
          </h2>
          <p className="text-slate-600 text-base max-w-xl font-sans">
            Metrics synced directly with local DuckDB columnar logs and active developer worker queues.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          
          <div className="bg-white border border-slate-200/80 rounded-3xl p-8 hover:border-indigo-400 hover:shadow-xl hover:shadow-indigo-500/5 transition-all duration-500 group">
            <div className="flex items-center justify-between mb-6">
              <span className="text-xs font-sans font-semibold text-slate-500 uppercase tracking-wider">Pending Backlog</span>
              <div className="p-3 rounded-2xl bg-indigo-50 text-indigo-600 border border-indigo-100 group-hover:scale-110 transition">
                <Database className="w-5 h-5" />
              </div>
            </div>
            <div className="space-y-1">
              <div className="text-4xl font-extrabold text-slate-900 font-sans tracking-tight">{tasks.length}</div>
              <p className="text-xs text-indigo-600 font-semibold">Active Work Vectors</p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
              <span>Status: Synced</span>
              <span className="text-emerald-600 font-semibold">99.8% Uptime</span>
            </div>
          </div>

          <div className="bg-white border border-slate-200/80 rounded-3xl p-8 hover:border-purple-400 hover:shadow-xl hover:shadow-purple-500/5 transition-all duration-500 group">
            <div className="flex items-center justify-between mb-6">
              <span className="text-xs font-sans font-semibold text-slate-500 uppercase tracking-wider">Mean Weight Wj</span>
              <div className="p-3 rounded-2xl bg-purple-50 text-purple-600 border border-purple-100 group-hover:scale-110 transition">
                <Brain className="w-5 h-5" />
              </div>
            </div>
            <div className="space-y-1">
              <div className="text-4xl font-extrabold text-slate-900 font-sans tracking-tight">{avgWeight}</div>
              <p className="text-xs text-purple-600 font-semibold">Cognitive Demand Load</p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
              <span>Max Threshold: 1.00</span>
              <span className="text-purple-600 font-semibold">Optimal Window</span>
            </div>
          </div>

          <div className="bg-white border border-slate-200/80 rounded-3xl p-8 hover:border-sky-400 hover:shadow-xl hover:shadow-sky-500/5 transition-all duration-500 group">
            <div className="flex items-center justify-between mb-6">
              <span className="text-xs font-sans font-semibold text-slate-500 uppercase tracking-wider">Solver Convergence</span>
              <div className="p-3 rounded-2xl bg-sky-50 text-sky-600 border border-sky-100 group-hover:scale-110 transition">
                <Cpu className="w-5 h-5" />
              </div>
            </div>
            <div className="space-y-1">
              <div className="text-4xl font-extrabold text-slate-900 font-sans tracking-tight">11.8 <span className="text-lg font-normal text-slate-400">ms</span></div>
              <p className="text-xs text-sky-600 font-semibold">OR-Tools Branch & Bound</p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
              <span>Variables: 1,024</span>
              <span className="text-emerald-600 font-semibold">Zero Conflicts</span>
            </div>
          </div>

          <div className="bg-white border border-slate-200/80 rounded-3xl p-8 hover:border-rose-400 hover:shadow-xl hover:shadow-rose-500/5 transition-all duration-500 group">
            <div className="flex items-center justify-between mb-6">
              <span className="text-xs font-sans font-semibold text-slate-500 uppercase tracking-wider">Hazard Spike</span>
              <div className="p-3 rounded-2xl bg-rose-50 text-rose-600 border border-rose-100 group-hover:scale-110 transition">
                <ShieldAlert className="w-5 h-5" />
              </div>
            </div>
            <div className="space-y-1">
              <div className="text-4xl font-extrabold text-rose-600 font-sans tracking-tight">+18.4%</div>
              <p className="text-xs text-rose-600 font-semibold">Syntax Exception Risk</p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
              <span>Correlation: High</span>
              <span className="text-rose-600 font-semibold">E(t) &lt; 35%</span>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}

function BacklogSection({ tasks, onAddTask, onDeleteTask }) {
  const [ref, isVisible] = useScrollObserver();

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [estimatedMinutes, setEstimatedMinutes] = useState(30);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredTasks = useMemo(() => {
    return tasks.filter(
      (t) =>
        t.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.description.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [tasks, searchTerm]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    onAddTask({
      id: Date.now(),
      title: title.toUpperCase().replace(/\s+/g, '_'),
      description: description || 'User defined workload parameter vector',
      estimated_minutes: parseInt(estimatedMinutes, 10),
      cognitive_weight: parseFloat((Math.random() * 0.5 + 0.45).toFixed(2)),
      category: 'CUSTOM',
      status: 'QUEUED'
    });
    setTitle('');
    setDescription('');
    setEstimatedMinutes(30);
  };

  return (
    <section id="backlog" ref={ref} className="py-28 border-t border-slate-200/60">
      <div className={`space-y-12 transition-all duration-1000 transform ${isVisible ? 'translate-x-0 opacity-100' : 'translate-x-24 opacity-0'}`}>
        
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 text-purple-700 text-xs font-sans font-bold uppercase tracking-widest bg-purple-50 px-3.5 py-1 rounded-full border border-purple-200">
            <Database className="w-3.5 h-3.5 text-purple-600" />
            <span>Workload Management</span>
          </div>
          <h2 className="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight font-sans">
            Task Backlog Matrix
          </h2>
          <p className="text-slate-600 text-base max-w-xl font-sans">
            Commit engineering task vectors with cognitive demand weight parameters (Wj) and target execution windows.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          <div className="lg:col-span-5 bg-white border border-slate-200/80 rounded-3xl p-8 space-y-6 shadow-xl shadow-slate-200/50">
            <div className="flex items-center gap-2 pb-4 border-b border-slate-100">
              <Plus className="w-5 h-5 text-indigo-600" />
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider font-sans">Commit Task Vector</h3>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-xs font-bold text-slate-600 mb-2 font-sans">TASK IDENTIFIER</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g., REFACTOR_ASYNC_DISPATCH"
                  className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-4 py-3 text-xs text-slate-900 focus:outline-none focus:border-indigo-600 transition"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-600 mb-2 font-sans">SCOPE & COMPLEXITY</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe scope, architectural complexity, and dependency boundaries..."
                  rows={3}
                  className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-4 py-3 text-xs text-slate-900 focus:outline-none focus:border-indigo-600 transition resize-none"
                />
              </div>

              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-xs font-bold text-slate-600 font-sans">ALLOCATED TIME WINDOW</label>
                  <span className="text-xs font-bold text-indigo-600">{estimatedMinutes} MINS</span>
                </div>
                <input
                  type="range"
                  min="15"
                  max="120"
                  step="15"
                  value={estimatedMinutes}
                  onChange={(e) => setEstimatedMinutes(e.target.value)}
                  className="w-full accent-indigo-600 bg-slate-200 rounded-lg cursor-pointer h-2"
                />
                <div className="flex justify-between text-[11px] text-slate-400 mt-1">
                  <span>15m</span>
                  <span>60m</span>
                  <span>120m</span>
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-4 rounded-2xl text-xs font-sans font-bold text-white bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-600 hover:shadow-[0_6px_20px_rgba(79,70,229,0.3)] transition-all duration-300 flex items-center justify-center gap-2 active:scale-95"
              >
                <Sparkles className="w-4 h-4" />
                <span>COMMIT TASK TO QUEUE</span>
              </button>
            </form>
          </div>

          <div className="lg:col-span-7 bg-white border border-slate-200/80 rounded-3xl p-8 space-y-6 shadow-xl shadow-slate-200/50">
            <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <Filter className="w-4 h-4 text-purple-600" />
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider font-sans">Active Queue ({filteredTasks.length})</h3>
              </div>

              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search vectors..."
                className="bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-1.5 text-xs text-slate-900 focus:outline-none focus:border-purple-600"
              />
            </div>

            <div className="space-y-3 max-h-[380px] overflow-y-auto pr-1">
              {filteredTasks.length === 0 ? (
                <div className="p-8 text-center text-xs font-sans text-slate-400">
                  No matching task vectors found in queue.
                </div>
              ) : (
                filteredTasks.map((task) => (
                  <div
                    key={task.id}
                    className="group p-4 rounded-2xl bg-slate-50/80 border border-slate-200/80 hover:border-indigo-400 hover:bg-white transition-all duration-300 flex items-center justify-between gap-4"
                  >
                    <div className="space-y-1 flex-1">
                      <div className="flex items-center gap-2.5">
                        <span className="text-[10px] text-slate-400 font-mono">#{task.id}</span>
                        <h4 className="text-xs font-bold text-slate-900 group-hover:text-indigo-600 transition">
                          {task.title}
                        </h4>
                        <span className="text-[9px] font-semibold px-2 py-0.5 rounded-full bg-slate-200/80 text-slate-600">
                          {task.category || 'WORKLOAD'}
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 line-clamp-1 font-sans">{task.description}</p>
                    </div>

                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <span className="text-[11px] font-bold text-purple-700 bg-purple-50 border border-purple-200 px-2.5 py-1 rounded-lg block mb-1">
                          Wj: {task.cognitive_weight}
                        </span>
                        <span className="text-[10px] text-slate-400">{task.estimated_minutes} mins</span>
                      </div>

                      <button
                        onClick={() => onDeleteTask(task.id)}
                        className="p-2 rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition"
                        title="Delete Task"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}

function SolverSection({ schedule, onSolve, isSolving }) {
  const [ref, isVisible] = useScrollObserver();

  return (
    <section id="solver" ref={ref} className="py-28 border-t border-slate-200/60">
      <div className={`space-y-12 transition-all duration-1000 transform ${isVisible ? 'translate-x-0 opacity-100' : '-translate-x-24 opacity-0'}`}>
        
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div className="space-y-3">
            <div className="inline-flex items-center gap-2 text-indigo-700 text-xs font-sans font-bold uppercase tracking-widest bg-indigo-50 px-3.5 py-1 rounded-full border border-indigo-200">
              <Cpu className="w-3.5 h-3.5 text-indigo-600" />
              <span>Optimization Engine</span>
            </div>
            <h2 className="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight font-sans">
              ILP Workload Scheduler
            </h2>
            <p className="text-slate-600 text-base max-w-xl font-sans">
              Integer Linear Programming branch-and-bound solver mapping task vectors onto predicted mental energy windows E(t).
            </p>
          </div>

          <button
            onClick={onSolve}
            disabled={isSolving}
            className="px-8 py-4 rounded-full text-xs font-sans font-bold text-white bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-600 hover:shadow-[0_6px_20px_rgba(79,70,229,0.3)] transition-all duration-300 flex items-center gap-2 disabled:opacity-50 active:scale-95"
          >
            <RefreshCw className={`w-4 h-4 ${isSolving ? 'animate-spin' : ''}`} />
            <span>{isSolving ? 'DISPATCHING SOLVER...' : 'EXECUTE OR-TOOLS SOLVER'}</span>
          </button>
        </div>

        <div className="bg-white border border-slate-200/80 rounded-3xl p-8 space-y-4 shadow-xl shadow-slate-200/50">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-600 uppercase tracking-wider flex items-center gap-2 font-sans">
              <Clock className="w-4 h-4 text-indigo-600" />
              32 Forecast Slots Ribbon (Scroll Horizontal)
            </span>
            <span className="text-[11px] text-slate-400 font-mono">8-HOUR HORIZON</span>
          </div>

          <div className="flex gap-4 overflow-x-auto pb-4 pt-1">
            {schedule.map((item, idx) => (
              <div
                key={idx}
                className="min-w-[180px] p-4 rounded-2xl bg-slate-50 border border-slate-200 hover:border-indigo-400 hover:bg-white transition-all duration-300 space-y-2 flex-shrink-0"
              >
                <div className="flex justify-between items-center text-[10px] text-slate-400">
                  <span>SLOT #{idx + 1}</span>
                  <span className="text-indigo-600 font-bold">{item.time}</span>
                </div>
                <p className="text-xs font-bold text-slate-900 truncate font-sans">{item.title}</p>
                <div className="flex items-center justify-between text-[11px] pt-1 border-t border-slate-200 font-sans">
                  <span className="text-emerald-600 font-semibold">E(t): {item.avg_predicted_energy}%</span>
                  <span className="text-purple-600 font-semibold">W: {item.cognitive_weight}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white border border-slate-200/80 rounded-3xl p-8 space-y-4 shadow-xl shadow-slate-200/50">
          <div className="flex justify-between items-center pb-2 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900 font-sans">Predicted Energy E(t) vs Task Weight Wj</h3>
              <p className="text-xs text-slate-500">Objective function: Maximize cumulative focus utility without fatigue overload</p>
            </div>
            <div className="flex items-center gap-4 text-xs font-sans">
              <span className="flex items-center gap-1.5 text-indigo-600 font-semibold">
                <span className="w-2.5 h-2.5 rounded-full bg-indigo-600"></span> Energy E(t)
              </span>
              <span className="flex items-center gap-1.5 text-purple-600 font-semibold">
                <span className="w-2.5 h-2.5 rounded-full bg-purple-600"></span> Weight Wj
              </span>
            </div>
          </div>

          <div className="h-72 pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={schedule} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="lightIndigo" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#4f46e5" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="lightPurple" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#9333ea" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#9333ea" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                <XAxis dataKey="time" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    borderColor: '#cbd5e1',
                    borderRadius: '1rem',
                    fontSize: '12px',
                    boxShadow: '0 10px 25px rgba(0,0,0,0.08)'
                  }}
                />
                <Area type="monotone" dataKey="avg_predicted_energy" name="Capacity E(t)" stroke="#4f46e5" strokeWidth={3} fillOpacity={1} fill="url(#lightIndigo)" />
                <Area type="monotone" dataKey="cognitive_weight" name="Task Weight Wj" stroke="#9333ea" strokeWidth={2} fillOpacity={1} fill="url(#lightPurple)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </section>
  );
}

function BiometricsSection() {
  const [ref, isVisible] = useScrollObserver();

  const [sleepHours, setSleepHours] = useState(7.5);
  const [deepSleepPct, setDeepSleepPct] = useState(22);
  const [hrvMs, setHrvMs] = useState(65);

  const [caffeineSlot, setCaffeineSlot] = useState(2);
  const [meetingHours, setMeetingHours] = useState(2.0);

  const calculatedEnergy = useMemo(() => {
    return Math.min(100, Math.max(30, sleepHours * 8.5 + deepSleepPct * 0.8 + hrvMs * 0.25)).toFixed(1);
  }, [sleepHours, deepSleepPct, hrvMs]);

  const simulatedCurve = useMemo(() => {
    const base = parseFloat(calculatedEnergy);
    return Array.from({ length: 12 }, (_, i) => {
      const hour = 8 + i * 1;
      let energy = base - i * 4.5 + (i === caffeineSlot ? 18 : 0) - meetingHours * 2.2;
      energy = Math.max(15, Math.min(100, energy));
      return {
        time: `${String(hour).padStart(2, '0')}:00`,
        energy: parseFloat(energy.toFixed(1))
      };
    });
  }, [calculatedEnergy, caffeineSlot, meetingHours]);

  return (
    <section id="biometrics" ref={ref} className="py-28 border-t border-slate-200/60">
      <div className={`space-y-12 transition-all duration-1000 transform ${isVisible ? 'translate-x-0 opacity-100' : 'translate-x-24 opacity-0'}`}>
        
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 text-emerald-700 text-xs font-sans font-bold uppercase tracking-widest bg-emerald-50 px-3.5 py-1 rounded-full border border-emerald-200">
            <Brain className="w-3.5 h-3.5 text-emerald-600" />
            <span>Biometric Intelligence</span>
          </div>
          <h2 className="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight font-sans">
            Biometric Simulation Lab
          </h2>
          <p className="text-slate-600 text-base max-w-xl font-sans">
            Simulate wearable circadian sleep metrics and exogenous counterfactual interventions (caffeine timing & meeting load).
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          <div className="lg:col-span-5 bg-white border border-slate-200/80 rounded-3xl p-8 space-y-6 shadow-xl shadow-slate-200/50">
            <div className="flex justify-between items-center pb-4 border-b border-slate-100">
              <span className="text-xs font-bold text-slate-900 uppercase tracking-wider font-sans">WEARABLE INPUTS</span>
              <span className="text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full">
                Baseline E(0) = {calculatedEnergy}%
              </span>
            </div>

            <div className="space-y-5 font-sans">
              <div>
                <div className="flex justify-between text-xs mb-2">
                  <span className="text-slate-600 flex items-center gap-1.5 font-medium"><Moon className="w-3.5 h-3.5 text-indigo-600" /> Sleep Duration</span>
                  <span className="text-slate-900 font-bold">{sleepHours} hrs</span>
                </div>
                <input
                  type="range"
                  min="4"
                  max="12"
                  step="0.5"
                  value={sleepHours}
                  onChange={(e) => setSleepHours(parseFloat(e.target.value))}
                  className="w-full accent-indigo-600 bg-slate-200 rounded-lg cursor-pointer h-2"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-2">
                  <span className="text-slate-600 flex items-center gap-1.5 font-medium"><Activity className="w-3.5 h-3.5 text-cyan-600" /> Deep Sleep Ratio</span>
                  <span className="text-slate-900 font-bold">{deepSleepPct}%</span>
                </div>
                <input
                  type="range"
                  min="5"
                  max="40"
                  step="1"
                  value={deepSleepPct}
                  onChange={(e) => setDeepSleepPct(parseInt(e.target.value, 10))}
                  className="w-full accent-indigo-600 bg-slate-200 rounded-lg cursor-pointer h-2"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-2">
                  <span className="text-slate-600 flex items-center gap-1.5 font-medium"><Gauge className="w-3.5 h-3.5 text-emerald-600" /> HRV RMSSD</span>
                  <span className="text-slate-900 font-bold">{hrvMs} ms</span>
                </div>
                <input
                  type="range"
                  min="20"
                  max="140"
                  step="2"
                  value={hrvMs}
                  onChange={(e) => setHrvMs(parseInt(e.target.value, 10))}
                  className="w-full accent-indigo-600 bg-slate-200 rounded-lg cursor-pointer h-2"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-2">
                  <span className="text-slate-600 flex items-center gap-1.5 font-medium"><Coffee className="w-3.5 h-3.5 text-amber-600" /> Caffeine Timing Boost</span>
                  <span className="text-slate-900 font-bold">Slot #{caffeineSlot} (10:00 AM)</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="8"
                  step="1"
                  value={caffeineSlot}
                  onChange={(e) => setCaffeineSlot(parseInt(e.target.value, 10))}
                  className="w-full accent-amber-500 bg-slate-200 rounded-lg cursor-pointer h-2"
                />
              </div>
            </div>
          </div>

          <div className="lg:col-span-7 bg-white border border-slate-200/80 rounded-3xl p-8 space-y-4 shadow-xl shadow-slate-200/50">
            <div className="flex justify-between items-center pb-2 border-b border-slate-100">
              <h3 className="text-sm font-bold text-slate-900 font-sans">Counterfactual Energy Decay Projection</h3>
              <span className="text-xs font-semibold text-emerald-600">12-HOUR DECAY FORECAST</span>
            </div>

            <div className="h-72 pt-4">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={simulatedCurve} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="emeraldGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                  <XAxis dataKey="time" stroke="#64748b" fontSize={11} />
                  <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#ffffff',
                      borderColor: '#cbd5e1',
                      borderRadius: '1rem',
                      fontSize: '12px'
                    }}
                  />
                  <Area type="monotone" dataKey="energy" name="Simulated E(t) %" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#emeraldGrad)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}

function HazardSection() {
  const [ref, isVisible] = useScrollObserver();

  const [energyState, setEnergyState] = useState(35);

  const hazardStats = useMemo(() => {
    const syntaxSpike = Math.max(0, (50 - energyState) * 1.45).toFixed(1);
    const backspaceSpike = Math.max(0, (50 - energyState) * 2.1).toFixed(1);
    let riskProtocol = 'OPTIMAL FOCUS WINDOW';
    let riskClass = 'text-emerald-700 border-emerald-300 bg-emerald-50';

    if (energyState < 35) {
      riskProtocol = 'CRITICAL: HIGH EXCEPTION RISK';
      riskClass = 'text-rose-700 border-rose-300 bg-rose-50';
    } else if (energyState < 50) {
      riskProtocol = 'MODERATE: RECOMMEND MICRO-BREAK';
      riskClass = 'text-amber-700 border-amber-300 bg-amber-50';
    }

    return { syntaxSpike, backspaceSpike, riskProtocol, riskClass };
  }, [energyState]);

  return (
    <section id="hazard" ref={ref} className="py-28 border-t border-slate-200/60">
      <div className={`space-y-12 transition-all duration-1000 transform ${isVisible ? 'translate-x-0 opacity-100' : '-translate-x-24 opacity-0'}`}>
        
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 text-rose-700 text-xs font-sans font-bold uppercase tracking-widest bg-rose-50 px-3.5 py-1 rounded-full border border-rose-200">
            <ShieldAlert className="w-3.5 h-3.5 text-rose-600" />
            <span>Defect Risk Engine</span>
          </div>
          <h2 className="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight font-sans">
            Statistical Defect Hazard
          </h2>
          <p className="text-slate-600 text-base max-w-xl font-sans">
            Correlate low biological capacity states with software defect probabilities and IDE typing cadence degradation.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          <div className="lg:col-span-6 bg-white border border-slate-200/80 rounded-3xl p-8 space-y-6 shadow-xl shadow-slate-200/50">
            <div className="space-y-3 font-sans">
              <div className="flex justify-between items-center font-sans">
                <span className="text-xs text-slate-500 font-bold">SIMULATED CAPACITY E(t)</span>
                <span className="text-2xl font-extrabold text-cyan-600">{energyState}%</span>
              </div>
              <input
                type="range"
                min="10"
                max="100"
                step="1"
                value={energyState}
                onChange={(e) => setEnergyState(parseInt(e.target.value, 10))}
                className="w-full accent-cyan-600 bg-slate-200 rounded-lg cursor-pointer h-3"
              />
            </div>

            <div className={`p-5 rounded-2xl border ${hazardStats.riskClass} space-y-1 font-sans`}>
              <div className="flex items-center gap-2 text-xs font-bold">
                <AlertTriangle className="w-4 h-4" />
                <span>{hazardStats.riskProtocol}</span>
              </div>
              <p className="text-xs opacity-80 leading-relaxed">
                Automated safety protocol dispatched to local IDE extension when capacity drops below threshold.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4 font-sans">
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                <span className="text-[11px] font-bold text-slate-500 uppercase block mb-1">Syntax Error Spike</span>
                <span className="text-2xl font-extrabold text-rose-600">+{hazardStats.syntaxSpike}%</span>
              </div>
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                <span className="text-[11px] font-bold text-slate-500 uppercase block mb-1">Backspace Ratio</span>
                <span className="text-2xl font-extrabold text-amber-600">+{hazardStats.backspaceSpike}%</span>
              </div>
            </div>
          </div>

          <div className="lg:col-span-6 bg-white border border-slate-200/80 rounded-3xl p-8 flex flex-col items-center justify-center text-center space-y-4 shadow-xl shadow-slate-200/50">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest font-sans">Depletion Gauge Index</span>
            
            <div className="relative w-48 h-48 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90">
                <circle cx="96" cy="96" r="75" stroke="#e2e8f0" strokeWidth="12" fill="transparent" />
                <circle
                  cx="96"
                  cy="96"
                  r="75"
                  stroke={energyState < 35 ? '#e11d48' : energyState < 50 ? '#d97706' : '#10b981'}
                  strokeWidth="12"
                  fill="transparent"
                  strokeDasharray="471"
                  strokeDashoffset={471 - (471 * energyState) / 100}
                  strokeLinecap="round"
                  className="transition-all duration-500"
                />
              </svg>
              <div className="absolute text-center font-sans">
                <span className="text-4xl font-extrabold text-slate-900">{energyState}%</span>
                <span className="block text-[10px] text-slate-400 uppercase mt-1">Capacity</span>
              </div>
            </div>

            <p className="text-xs text-slate-500 max-w-xs leading-relaxed font-sans">
              Real-time statistical hazard multiplier updated via active telemetry event stream.
            </p>
          </div>

        </div>
      </div>
    </section>
  );
}

function DecompositionSection({ tasks }) {
  const [ref, isVisible] = useScrollObserver();

  const [selectedTaskId, setSelectedTaskId] = useState(tasks[0]?.id || 101);
  const [chunks, setChunks] = useState(null);
  const [isChunking, setIsChunking] = useState(false);

  const selectedTask = useMemo(() => {
    return tasks.find((t) => t.id === Number(selectedTaskId)) || tasks[0];
  }, [selectedTaskId, tasks]);

  const handleDecompose = () => {
    if (!selectedTask) return;
    setIsChunking(true);
    setTimeout(() => {
      const count = Math.ceil(selectedTask.estimated_minutes / 15);
      const generated = Array.from({ length: count }, (_, i) => ({
        idx: i + 1,
        title: `[Chunk ${i + 1}/${count}] ${selectedTask.title}`,
        time: '15 mins',
        weight: parseFloat((selectedTask.cognitive_weight * 0.72).toFixed(2))
      }));
      setChunks(generated);
      setIsChunking(false);
    }, 600);
  };

  return (
    <section id="decomposition" ref={ref} className="py-28 border-t border-slate-200/60">
      <div className={`space-y-12 transition-all duration-1000 transform ${isVisible ? 'translate-x-0 opacity-100' : 'translate-x-24 opacity-0'}`}>
        
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div className="space-y-3">
            <div className="inline-flex items-center gap-2 text-cyan-700 text-xs font-sans font-bold uppercase tracking-widest bg-cyan-50 px-3.5 py-1 rounded-full border border-cyan-200">
              <Layers className="w-3.5 h-3.5 text-cyan-600" />
              <span>Workload Chunking</span>
            </div>
            <h2 className="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight font-sans">
              Subtask Vector Decomposition
            </h2>
            <p className="text-slate-600 text-base max-w-xl font-sans">
              Break down heavy cognitive tasks (Wj &gt; 0.70) into optimized 15-minute sub-vectors to prevent burnout.
            </p>
          </div>

          <button
            onClick={handleDecompose}
            disabled={isChunking}
            className="px-8 py-4 rounded-full text-xs font-sans font-bold text-white bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-600 hover:shadow-[0_6px_20px_rgba(79,70,229,0.3)] transition-all duration-300 flex items-center gap-2 disabled:opacity-50 active:scale-95"
          >
            <Sparkles className={`w-4 h-4 ${isChunking ? 'animate-spin' : ''}`} />
            <span>{isChunking ? 'CHUNKING VECTOR...' : 'GENERATE SUBTASK CHUNKS'}</span>
          </button>
        </div>

        <div className="bg-white border border-slate-200/80 rounded-3xl p-8 space-y-6 shadow-xl shadow-slate-200/50">
          <div className="max-w-xl space-y-2 font-sans">
            <label className="block text-xs font-bold text-slate-600">SELECT HEAVY TASK VECTOR</label>
            <select
              value={selectedTaskId}
              onChange={(e) => {
                setSelectedTaskId(e.target.value);
                setChunks(null);
              }}
              className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-4 py-3.5 text-xs text-slate-900 focus:outline-none focus:border-indigo-600"
            >
              {tasks.map((t) => (
                <option key={t.id} value={t.id}>
                  #{t.id} - {t.title} [Weight Wj: {t.cognitive_weight}]
                </option>
              ))}
            </select>
          </div>

          {chunks && (
            <div className="pt-6 border-t border-slate-100 space-y-4">
              <span className="text-xs font-bold text-cyan-700 uppercase tracking-wider block font-sans">
                Decomposed Micro-Vector Schedule ({chunks.length} Chunks Generated)
              </span>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-5 font-sans">
                {chunks.map((chunk) => (
                  <div
                    key={chunk.idx}
                    className="p-6 rounded-2xl bg-slate-50 border border-slate-200 hover:border-cyan-400 transition-all duration-300 space-y-3"
                  >
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-bold text-cyan-600">CHUNK #{chunk.idx}</span>
                      <span className="text-xs text-slate-400">{chunk.time}</span>
                    </div>
                    <p className="text-xs font-bold text-slate-900 leading-snug">{chunk.title}</p>
                    <div className="pt-2 border-t border-slate-200 flex justify-between items-center text-xs">
                      <span className="text-slate-400">Target Duration</span>
                      <span className="text-purple-600 font-bold">Wj: {chunk.weight}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

      </div>
    </section>
  );
}

export default function App() {
  const [tasks, setTasks] = useState(INITIAL_TASKS);
  const [schedule, setSchedule] = useState(INITIAL_SCHEDULE);
  const [activeSection, setActiveSection] = useState('intro');
  const [isLive, setIsLive] = useState(true);
  const [isSolving, setIsSolving] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const sections = ['intro', 'telemetry', 'backlog', 'solver', 'biometrics', 'hazard', 'decomposition'];
      const scrollPos = window.scrollY + 250;

      for (const section of sections) {
        const el = document.getElementById(section);
        if (el) {
          const top = el.offsetTop;
          const height = el.offsetHeight;
          if (scrollPos >= top && scrollPos < top + height) {
            setActiveSection(section);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleSolve = () => {
    setIsSolving(true);
    setTimeout(() => {
      setSchedule([...INITIAL_SCHEDULE].sort(() => Math.random() - 0.5));
      setIsSolving(false);
    }, 800);
  };

  const handleAddTask = (newTask) => {
    setTasks((prev) => [newTask, ...prev]);
  };

  const handleDeleteTask = (id) => {
    setTasks((prev) => prev.filter((t) => t.id !== id));
  };

  const scrollToSection = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const avgWeight = useMemo(() => {
    if (!tasks.length) return '0.00';
    return (tasks.reduce((a, b) => a + b.cognitive_weight, 0) / tasks.length).toFixed(2);
  }, [tasks]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 font-sans antialiased selection:bg-indigo-100 selection:text-indigo-900 px-6 md:px-12">
      
      {/* Floating Glass Navbar */}
      <Navigation
        activeSection={activeSection}
        isLive={isLive}
        onIngestClick={() => scrollToSection('backlog')}
      />

      {/* Main Spaced Layout */}
      <main className="max-w-7xl mx-auto space-y-12">
        <HeroIntroSection
          onExplore={() => scrollToSection('telemetry')}
          onRunSolver={handleSolve}
        />
        <TelemetrySection tasks={tasks} avgWeight={avgWeight} isLive={isLive} />
        <BacklogSection tasks={tasks} onAddTask={handleAddTask} onDeleteTask={handleDeleteTask} />
        <SolverSection schedule={schedule} onSolve={handleSolve} isSolving={isSolving} />
        <BiometricsSection />
        <HazardSection />
        <DecompositionSection tasks={tasks} />
      </main>

      {/* Footer */}
      <footer className="mt-32 py-12 border-t border-slate-200 font-sans text-xs text-slate-500 max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
        <div>Cognitive Pulse Platform — All Systems Operational</div>
        <div>Optimization Engine: Google OR-Tools ILP</div>
      </footer>
    </div>
  );
}