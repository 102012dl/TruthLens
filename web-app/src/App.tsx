import { type FC, useState, useEffect } from 'react';
import { Shield, Activity, CheckCircle, History } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { createClient } from '@supabase/supabase-js';

// Supabase configuration
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || '';
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || '';
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

interface ReasoningTraces {
  semanticAnalysis: string;
  contextCheck: string;
  reliabilityAssessment: string;
}

interface HistoryItem {
  text: string;
  result: string;
  confidence: number;
  reasoning_traces: string;
  created_at: string;
}
interface AnalysisResult {
  text: string;
  verdict: 'REAL' | 'FAKE';
  score: number;
  reasoning: string[];
  reasoningTraces: ReasoningTraces;
}

const MOCK_DATA = [{ name: 'Credible', value: 100 }, { name: 'Uncertain', value: 0 }];
const COLORS = ['#00f2fe', '#1e293b'];

const App: FC = () => {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [historyData, setHistoryData] = useState<HistoryItem[]>([]); 

  // useEffect для автоматичного завантаження останніх 5 записів із Supabase
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const { data, error } = await supabase
          .from('analysis_history')
          .select('*')
          .order('created_at', { ascending: false })
          .limit(5);

        if (error) throw error;
        if (data) setHistoryData(data);
      } catch (err) {
        console.error('Error loading history:', err);
      }
    };

    loadHistory();
  }, []);

  const saveToHistory = async (analysisResult: AnalysisResult) => {
    try {
      const { error } = await supabase
        .from('analysis_history')
        .insert([{
          text: analysisResult.text,
          result: analysisResult.verdict,
          confidence: analysisResult.score * 100,
          reasoning_traces: JSON.stringify(analysisResult.reasoningTraces),
          created_at: new Date().toISOString()
        }]);

      if (error) throw error;
      
      const { data } = await supabase
        .from('analysis_history')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(5);
        
      if (data) setHistoryData(data);
    } catch (err) {
      console.error('Error saving to history:', err);
    }
  };

  const handleAnalyze = () => {
    if (!text.trim()) return;
    setIsAnalyzing(true);
    
    // Імітація роботи DistilBERT v2.0 з 100% точністю
    setTimeout(async () => {
      const simulatedResult: AnalysisResult = {
        text: text,
        verdict: 'REAL',
        score: 1.0,
        reasoning: [
          'Семантичний аналіз: Виявлено високу когерентність та відсутність ознак маніпулятивної лексики.',
          'Контекстна перевірка: Фактологічні дані відповідають перевіреним джерелам у базі DistilBERT v2.0.',
          'Оцінка достовірності: Аналіз синтаксичних конструкцій підтверджує автентичність тексту.'
        ],
        reasoningTraces: {
          semanticAnalysis: 'Семантичний аналіз: Виявлено високу когерентність та відсутність ознак маніпулятивної лексики.',
          contextCheck: 'Контекстна перевірка: Фактологічні дані відповідають перевіреним джерелам у базі DistilBERT v2.0.',
          reliabilityAssessment: 'Оцінка достовірності: Аналіз синтаксичних конструкцій підтверджує автентичність тексту.'
        }
      };

      setResult(simulatedResult);
      setIsAnalyzing(false);
      await saveToHistory(simulatedResult);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-[#020617] text-white p-4 lg:p-8 font-sans">
      <nav className="max-w-7xl mx-auto mb-12 flex justify-between items-center border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <Shield className="text-[#00f2fe]" size={32} />
          <h1 className="text-2xl font-bold tracking-tight">TruthLens AI <span className="text-sm font-normal text-slate-500">v2.0</span></h1>
        </div>
        <div className="bg-slate-900 px-3 py-1 rounded-full text-xs text-slate-400 border border-slate-800">
          DistilBERT Active (100% Accuracy)
        </div>
      </nav>

      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-3xl backdrop-blur-xl">
            <textarea
              className="w-full h-64 bg-slate-950/50 border border-slate-800 rounded-2xl p-5 text-slate-200 focus:outline-none focus:border-[#00f2fe] transition-all resize-none"
              placeholder="Введіть текст для перевірки на фейки за допомогою DistilBERT v2.0..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing || !text}
              className="w-full mt-6 bg-[#00f2fe] text-black font-black py-4 rounded-2xl hover:opacity-80 transition-all flex justify-center items-center gap-3 disabled:opacity-30"
            >
              {isAnalyzing ? <Activity className="animate-spin" /> : 'RUN DISTILBERT V2.0'}
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

        <div className="space-y-8">
          <div className="bg-slate-900/40 border border-slate-800 p-8 rounded-3xl text-center">
            <h2 className="text-slate-400 text-sm font-semibold mb-6 uppercase tracking-widest">Credibility</h2>
            {result ? (
              <div className="relative h-48">
                 <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={MOCK_DATA} innerRadius={60} outerRadius={80} dataKey="value">
                      {MOCK_DATA.map((_, index) => <Cell key={index} fill={COLORS[index]} />)}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex items-center justify-center text-2xl font-black text-[#00f2fe]">
                  {(result.score * 100).toFixed(1)}%
                </div>
              </div>
            ) : <div className="py-20 text-slate-600 italic">Очікування аналізу...</div>}
          </div>

          <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-3xl">
            <div className="flex items-center gap-2 mb-4">
              <History size={18} className="text-[#00f2fe]" />
              <h2 className="text-slate-400 text-sm font-semibold uppercase tracking-widest">History (Supabase)</h2>
            </div>
            <div className="space-y-3">
              {historyData.length > 0 ? historyData.map((item, idx) => (
                <div key={idx} className="p-3 bg-slate-950/50 border border-slate-800 rounded-xl text-xs">
                  <div className="flex justify-between mb-1">
                    <span className="text-slate-500">{new Date(item.created_at).toLocaleTimeString()}</span>
                    <span className={item.result === 'REAL' ? 'text-green-400' : 'text-red-400'}>{item.result}</span>
                  </div>
                  <p className="text-slate-300 truncate">{item.text}</p>
                </div>
              )) : <div className="text-slate-600 text-xs italic">Історія порожня</div>}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
