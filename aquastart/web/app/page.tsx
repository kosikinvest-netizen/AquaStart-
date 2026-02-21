'use client';

import { createBrowserClient } from '@supabase/ssr';
import { useState } from 'react';

export default function AquaStartLogin() {
  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setMessage('⚠️ Wprowadź e-mail i hasło.');
      return;
    }

    setIsLoading(true);
    const { error } = await supabase.auth.signUp({ email, password });
    setIsLoading(false);

    if (error) {
      setMessage(`Błąd: ${error.message}`);
    } else {
      setMessage('✅ Sukces! Sprawdź zakładkę Users w panelu Supabase.');
    }
  };

  return (
    <div className="min-h-screen bg-[#040814] flex flex-col items-center justify-center p-6 text-slate-200 font-sans relative overflow-hidden">
      {/* Tło i efekty świetlne */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_rgba(6,182,212,0.15)_0%,_transparent_70%)] pointer-events-none z-0"></div>
      
      {/* Nagłówek systemowy */}
      <div className="text-center space-y-4 relative z-10 mb-12">
        <div className="inline-flex items-center gap-3 border border-cyan-500/30 bg-cyan-500/10 px-4 py-1.5 rounded-full shadow-[0_0_20px_rgba(6,182,212,0.2)]">
          <span className="w-2 h-2 rounded-full bg-cyan-500 animate-ping"></span>
          <span className="text-cyan-500 text-[9px] font-black uppercase tracking-[0.3em]">Tryb Diagnostyczny</span>
        </div>
        <h2 className="text-4xl md:text-5xl font-black uppercase tracking-tighter text-white">
          Weryfikacja <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 to-teal-400">Bazy</span>
        </h2>
      </div>

      {/* Główny panel (Glassmorphism) */}
      <div className="w-full max-w-md bg-slate-800/40 backdrop-blur-xl p-10 md:p-12 relative overflow-hidden shadow-[0_0_50px_rgba(6,182,212,0.2)] border border-cyan-500/30 rounded-[2rem] text-center flex flex-col justify-center">
        <div className="absolute inset-0 bg-gradient-to-b from-cyan-500/5 via-transparent to-transparent pointer-events-none z-0"></div>
        
        <form onSubmit={handleSignUp} className="space-y-6 relative z-10">
          <div className="space-y-4">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-[#0b0f19] border border-slate-700 rounded-2xl p-4 text-center text-cyan-400 font-bold text-sm tracking-widest uppercase focus:border-cyan-500 focus:shadow-[0_0_20px_rgba(6,182,212,0.3)] focus:outline-none transition-all placeholder:text-slate-600"
              placeholder="ADRES E-MAIL"
              disabled={isLoading}
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-[#0b0f19] border border-slate-700 rounded-2xl p-4 text-center text-cyan-400 font-black text-2xl tracking-[0.5em] uppercase focus:border-cyan-500 focus:shadow-[0_0_20px_rgba(6,182,212,0.3)] focus:outline-none transition-all placeholder:text-slate-600"
              placeholder="••••••••"
              disabled={isLoading}
            />
            
            {message && (
              <p className={`text-[10px] font-black uppercase tracking-widest mt-2 ${message.includes('Sukces') ? 'text-emerald-400' : 'text-rose-500'}`}>
                {message}
              </p>
            )}
          </div>

          <button 
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-[#0f172a] font-black py-5 px-6 rounded-2xl uppercase text-xs tracking-[0.2em] transition-all duration-300 shadow-[0_0_20px_rgba(6,182,212,0.4)] disabled:opacity-50"
          >
            {isLoading ? 'ŁADOWANIE...' : 'ZAŁÓŻ KONTO TESTOWE'}
          </button>
        </form>
      </div>
    </div>
  );
}