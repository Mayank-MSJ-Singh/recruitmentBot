import React, { useState, useEffect } from 'react';
import { Bot, FileText, Search, Play, Users, ChevronRight, UserCheck, Star, Clock } from 'lucide-react';

interface Employee {
  id: string;
  name: string;
  role: string;
  tenure_years: number;
  previous_industry: string;
  education: string;
  key_skills: string[];
  performance_rating: number;
  professional_summary: string;
}

interface Finalist {
  id: string;
  name: string;
  role_applied: string;
  previous_interview_date: string;
  education: string;
  experience_years: number;
  previous_industry: string;
  key_skills: string[];
  overall_interview_rating: number;
  reason_for_rejection: string;
  professional_summary: string;
}

export default function HiringManagerView() {
  const [prompt, setPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [currentStep, setCurrentStep] = useState<'input' | 'campaign' | 'pipeline'>('input');
  const [jdData, setJdData] = useState<any>(null);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [finalists, setFinalists] = useState<Finalist[]>([]);
  const [isSourcing, setIsSourcing] = useState(false);
  const [sourcingLogs, setSourcingLogs] = useState<string[]>([]);

  useEffect(() => {
    // Fetch employee & finalist DB
    fetch('http://localhost:8080/api/database')
      .then(r => r.json())
      .then(data => {
        if (data.employees) setEmployees(data.employees);
        if (data.finalists_not_selected) setFinalists(data.finalists_not_selected);
      })
      .catch(err => console.error("Error loading employee DB:", err));
  }, []);

  const topPerformers = employees.filter(emp => emp.performance_rating >= 8.5);

  const simulateJDGeneration = async () => {
    setIsProcessing(true);
    setLogs([]);
    
    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Accessing employee database to extract high-performer DNA...`]);
    await new Promise(r => setTimeout(r, 800));
    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Found ${topPerformers.length} top performers with rating >= 8.5/10.`]);
    await new Promise(r => setTimeout(r, 800));
    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Extracted key success vectors: Pharma background, high relationship focus, B.Sc.`]);
    await new Promise(r => setTimeout(r, 800));
    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Calling Gemini AI to generate Job Description...`]);

    try {
       const res = await fetch('http://localhost:8080/api/generate_jd', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ prompt })
       });
       if(res.ok) {
           const jd = await res.json();
           setJdData(jd);
           setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Job Description generated successfully.`]);
       } else {
           setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ❌ Failed to generate JD`]);
       }
    } catch(err) {
       setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ❌ Failed to generate JD: ${err}`]);
    }
    
    await new Promise(r => setTimeout(r, 800));
    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Structuring candidate profile specifications...`]);
    await new Promise(r => setTimeout(r, 800));

    setIsProcessing(false);
    setCurrentStep('campaign');
  };

  const startCandidateSourcing = async () => {
    setIsSourcing(true);
    setSourcingLogs([]);
    setSourcingLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Mining internal candidate repository (historical finalists)...`]);
    await new Promise(r => setTimeout(r, 1000));
    setSourcingLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Scanned 120 past candidates. Found ${finalists.length} high-probability matches.`]);
    await new Promise(r => setTimeout(r, 1000));
    setSourcingLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Sourcing completed. Candidate Pipeline hydrated.`]);
    await new Promise(r => setTimeout(r, 1000));
    
    setIsSourcing(false);
    setCurrentStep('pipeline');
  };

  return (
    <div className="p-6 space-y-6 text-gray-200">
      {/* Navigation / Progress Indicator */}
      <div className="flex items-center space-x-4 bg-gray-900 border border-gray-800 p-4 rounded-xl max-w-4xl mx-auto text-sm">
        <div className={`flex items-center space-x-2 ${currentStep === 'input' ? 'text-purple-400 font-bold' : 'text-gray-500'}`}>
          <Search className="w-4 h-4" />
          <span>1. Requisition Input</span>
        </div>
        <ChevronRight className="w-4 h-4 text-gray-700" />
        <div className={`flex items-center space-x-2 ${currentStep === 'campaign' ? 'text-purple-400 font-bold' : 'text-gray-500'}`}>
          <FileText className="w-4 h-4" />
          <span>2. Generated JD & Archetypes</span>
        </div>
        <ChevronRight className="w-4 h-4 text-gray-700" />
        <div className={`flex items-center space-x-2 ${currentStep === 'pipeline' ? 'text-purple-400 font-bold' : 'text-gray-500'}`}>
          <Users className="w-4 h-4" />
          <span>3. Sourced Candidates</span>
        </div>
      </div>

      {currentStep === 'input' && (
        <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-2xl">
            <h2 className="text-2xl font-bold mb-4 flex items-center text-white"><Search className="mr-3 text-purple-500" /> Start New Requisition</h2>
            <p className="text-gray-400 mb-6">Describe the role, and the AI Orchestrator will handle sourcing, screening, and matching.</p>
            <div className="space-y-4">
              <textarea 
                className="w-full bg-gray-950 border border-gray-800 rounded-lg p-4 text-white focus:outline-none focus:border-purple-500 transition-colors h-32"
                placeholder="e.g., Need 3 Insurance Sales Leads in Delhi. Fluent in Hindi. Must have 3+ years experience..."
                value={prompt}
                onChange={e => setPrompt(e.target.value)}
              />
              <button 
                onClick={simulateJDGeneration}
                disabled={isProcessing || !prompt}
                className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-700 disabled:text-gray-500 text-white font-medium py-3 px-6 rounded-lg transition-all flex items-center justify-center w-full"
              >
                {isProcessing ? <span className="animate-pulse">Processing...</span> : <><Play className="w-4 h-4 mr-2" /> Generate Job Campaign</>}
              </button>
            </div>
          </div>

          {isProcessing && (
            <div className="bg-black border border-gray-800 rounded-xl p-6 font-mono text-sm text-green-400 h-64 overflow-y-auto shadow-inner">
              <div className="flex items-center mb-4 text-purple-400 border-b border-gray-800 pb-2">
                <Bot className="w-5 h-5 mr-2 animate-bounce" /> AI Orchestrator Live Feed
              </div>
              {logs.map((log, i) => (
                <div key={i} className="mb-2 animate-fade-in-up">{log}</div>
              ))}
              <div className="animate-pulse mt-2">_</div>
            </div>
          )}
        </div>
      )}

      {currentStep === 'campaign' && (
        <div className="max-w-6xl mx-auto space-y-8 animate-fade-in">
          {/* Top Action Panel */}
          <div className="bg-purple-950/20 border border-purple-800/40 rounded-xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
             <div>
                <h3 className="text-xl font-bold text-white flex items-center"><Bot className="text-purple-400 mr-2" /> Job Requisition Specs Ready</h3>
                <p className="text-gray-300 text-sm mt-1">AI has processed requirements against your database's high-performer profiles.</p>
             </div>
             <button 
               onClick={startCandidateSourcing}
               disabled={isSourcing}
               className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-lg font-bold flex items-center justify-center space-x-2 transition-all self-start md:self-auto shadow-lg shadow-purple-900/30"
             >
                {isSourcing ? <span className="animate-pulse">Sourcing...</span> : <><Users className="w-5 h-5" /> <span>Search & Match Candidates</span></>}
             </button>
          </div>

          {isSourcing && (
            <div className="bg-black border border-gray-800 rounded-xl p-6 font-mono text-sm text-green-400 shadow-inner max-w-4xl mx-auto">
              <div className="flex items-center mb-4 text-purple-400 border-b border-gray-800 pb-2">
                <Bot className="w-5 h-5 mr-2 animate-bounce" /> AI Sourcing Agent Logs
              </div>
              {sourcingLogs.map((log, i) => (
                <div key={i} className="mb-2">{log}</div>
              ))}
              <div className="animate-pulse mt-2">_</div>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
             {/* Left Column: Job Description details */}
             <div className="lg:col-span-2 space-y-6">
                <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl space-y-4">
                   <div>
                      <h2 className="text-2xl font-bold text-white">{jdData?.job_title || 'Sales Lead'}</h2>
                      <div className="text-sm text-purple-400 font-medium mt-1">Location: {jdData?.location || 'Delhi NCR'}</div>
                   </div>
                   <div className="border-t border-gray-800 pt-4">
                      <h4 className="text-sm font-semibold uppercase tracking-wider text-gray-400 mb-2">Role Overview</h4>
                      <p className="text-gray-300 leading-relaxed text-sm">{jdData?.description || 'No description generated.'}</p>
                   </div>
                   <div className="border-t border-gray-800 pt-4">
                      <h4 className="text-sm font-semibold uppercase tracking-wider text-gray-400 mb-2">Key Requirements</h4>
                      <ul className="list-disc list-inside text-sm text-gray-300 space-y-2">
                         {(jdData?.requirements || []).map((req: string, i: number) => (
                             <li key={i}>{req}</li>
                         ))}
                      </ul>
                   </div>
                </div>
             </div>

             {/* Right Column: Employee DNA Profile */}
             <div className="space-y-6">
                <h4 className="text-lg font-bold text-white flex items-center"><UserCheck className="w-5 h-5 text-green-400 mr-2" /> Employee Database Archetype</h4>
                <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 space-y-6">
                   <div>
                      <div className="text-xs text-purple-400 uppercase tracking-wider font-semibold">Identified Top Performers</div>
                      <div className="mt-2 space-y-2 max-h-48 overflow-y-auto pr-1">
                         {topPerformers.slice(0, 5).map((emp, i) => (
                            <div key={i} className="flex justify-between items-center bg-gray-950 p-2.5 rounded border border-gray-800">
                               <div>
                                  <div className="text-sm font-semibold text-white">{emp.name}</div>
                                  <div className="text-xs text-gray-400">{emp.role} • {emp.previous_industry}</div>
                                </div>
                                <div className="flex items-center text-yellow-400 bg-yellow-950/40 border border-yellow-900/60 px-1.5 py-0.5 rounded text-xs">
                                   <Star className="w-3 h-3 mr-1 fill-yellow-400" /> {emp.performance_rating}
                                </div>
                            </div>
                         ))}
                      </div>
                   </div>

                   <div className="border-t border-gray-800 pt-4">
                      <div className="text-xs text-purple-400 uppercase tracking-wider font-semibold">AI Archetype Extract</div>
                      <div className="mt-2 text-sm text-gray-300 bg-purple-950/10 border border-purple-900/30 p-3 rounded-lg leading-relaxed font-mono">
                         <strong>Ideal DNA Matches:</strong> B.Sc/MBA, 3+ years experience, previous domain background matching existing high performers (e.g. Pharma or Finance).
                      </div>
                   </div>
                </div>
             </div>
          </div>
        </div>
      )}

      {currentStep === 'pipeline' && (
        <div className="max-w-6xl mx-auto space-y-8 animate-fade-in">
           <div className="flex justify-between items-center">
              <div>
                 <h2 className="text-2xl font-bold text-white">Matched Talent Pipeline</h2>
                 <p className="text-gray-400 text-sm mt-1">Showing matched profiles extracted from internal candidate databases.</p>
              </div>
              <button 
                 onClick={() => setCurrentStep('input')}
                 className="bg-gray-900 hover:bg-gray-800 border border-gray-800 px-4 py-2 rounded-lg text-sm transition-colors text-white"
              >
                 New Requisition
              </button>
           </div>

           {/* Pipeline Grid */}
           <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Candidates Column */}
              <div className="lg:col-span-2 space-y-4">
                 <h3 className="text-lg font-bold text-white flex items-center"><Users className="w-5 h-5 mr-2 text-purple-500" /> Matched Candidates</h3>
                 
                 {finalists.map((cand, idx) => (
                   <div key={cand.id} className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-purple-500 transition-colors">
                     <div className="flex justify-between items-start mb-4">
                       <div>
                         <h4 className="text-lg font-bold text-white">{cand.name}</h4>
                         <div className="text-sm text-gray-400 mt-1 flex flex-wrap gap-2">
                            <span className="bg-blue-900/40 text-blue-300 px-2 py-0.5 rounded text-xs border border-blue-800/60">Silver Medalist</span>
                            <span className="bg-purple-900/40 text-purple-300 px-2 py-0.5 rounded text-xs border border-purple-800/60">{cand.previous_industry}</span>
                         </div>
                       </div>
                       <div className="text-right">
                          <div className="text-2xl font-bold text-green-400">{Math.round(cand.overall_interview_rating * 10)}%</div>
                          <div className="text-xs text-gray-500 uppercase tracking-wide">Interview Match</div>
                       </div>
                     </div>
                     <p className="text-sm text-gray-400 mb-3">{cand.professional_summary}</p>
                     
                     <div className="bg-gray-950 p-3 rounded text-sm text-gray-300 border border-gray-800">
                       <span className="text-red-400 font-semibold">Previous Status:</span> {cand.reason_for_rejection}
                     </div>
                   </div>
                 ))}
              </div>

              {/* Statistics Column */}
              <div className="space-y-6">
                 <h3 className="text-lg font-bold text-white flex items-center"><FileText className="w-5 h-5 mr-2 text-purple-500" /> Pipeline Stats</h3>
                 <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 space-y-4">
                    <div className="flex justify-between items-center border-b border-gray-800 pb-2">
                      <span className="text-gray-400">Total Sourced Candidates</span>
                      <span className="text-xl font-bold text-white">{finalists.length}</span>
                    </div>
                    <div className="flex justify-between items-center border-b border-gray-800 pb-2">
                      <span className="text-gray-400">Database Size</span>
                      <span className="text-xl font-bold text-white">{employees.length}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400">Top Performers Highlighted</span>
                      <span className="text-xl font-bold text-green-400">{topPerformers.length}</span>
                    </div>
                 </div>
              </div>
           </div>
        </div>
      )}
    </div>
  );
}
