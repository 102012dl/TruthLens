import React, { useState } from 'react';
import { Shield, Search, BarChart3, Activity, AlertTriangle, CheckCircle } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

const MOCK_DATA = [{ name: 'Credible', value: 98.5 }, { name: 'Uncertain', value: 1.5 }];
const COLORS = ['#00f2fe', '#1e293b'];

export default function App() {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    setTimeout(() => {
      setResult({
        verdict: 'REAL',
        score: 0.985,
        reasoning: [
          "Контекстуальний аналіз підтверджує нейтральний тон звітності.",
          "Семантична відповідність перевіреним джерелам становить 98.5%.",
          "Відсутні ознаки маніпулятивної емоційності, характерної для фейків."
        ]
      });
      setIsAnalyzing(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-[#020617] text-white p-4 lg:p-8 font-sans">
      <nav className="max-w-7xl mx-auto mb-12 flex justify-between items-center border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <Shield className="text-[#00f2fe]" size={32} />
          <h1 className="text-2xl font-bold tracking-tight">TruthLens <span className="text-sm font-light text-slate-500">AI Factory</span></h1>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-400 bg-slate-900 px-3 py-1 rounded-full border border-slate-800">
          <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
          DistilBERT v2.0 Active
        </div>
      </nav>

      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-3xl backdrop-blur-xl">
            <h2 className="text-slate-400 text-sm font-semibold mb-4 uppercase tracking-widest">Input Analysis</h2>
            <textarea 
              className="w-full h-64 bg-slate-950/50 border border-slate-800 rounded-2xl p-5 text-slate-200 focus:outline-none focus:border-[#00f2fe] transition-all resize-none"
              placeholder="Вставте текст новини..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <button 
              onClick={handleAnalyze}
              disabled={isAnalyzing || !text}
              className="w-full mt-6 bg-[#00f2fe] text-black font-black py-4 rounded-2xl hover:scale-[1.01] transition-all flex justify-center items-center gap-3 disabled:opacity-30"
            >
              {isAnalyzing ? <Activity className="animate-spin" /> : 'RUN MULTI-AGENT ANALYSIS'}
            </button>
          </div>

          {result && (
            <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-3xl animate-in fade-in duration-500">
              <h2 className="text-slate-400 text-sm font-semibold mb-4 uppercase tracking-widest">Reasoning Traces</h2>
              <div className="space-y-4">
                {result.reasoning.map((trace: string, i: number) => (
                  <div key={i} className="flex gap-4 p-4 bg-slate-950/80 rounded-xl border-l-2 border-[#00f2fe]/50">
                    <CheckCircle size={18} className="text-[#00f2fe] shrink-0 mt-1" />
                    <p className="text-slate-300 text-sm">{trace}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="bg-slate-900/40 border border-slate-800 p-8 rounded-3xl text-center h-fit">
          <h2 className="text-slate-400 text-sm font-semibold mb-6 uppercase tracking-widest">Veracity Metrics</h2>
          {result ? (
            <div className="relative h-48">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={MOCK_DATA} innerRadius={60} outerRadius={80} paddingAngle={8} dataKey="value">
                    {MOCK_DATA.map((_, index) => <Cell key={index} fill={COLORS[index]} />)}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex items-center justify-center text-2xl font-black text-[#00f2fe]">98.5%</div>
            </div>
          ) : <div className="py-20 text-slate-600 italic">Waiting for analysis...</div>}
        </div>
      </main>
    </div>
  );
}
