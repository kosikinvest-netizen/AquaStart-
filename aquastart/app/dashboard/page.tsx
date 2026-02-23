'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';

export default function Dashboard() {
  const [pdfs, setPdfs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );

  useEffect(() => {
    fetchPdfs();
  }, []);

  async function fetchPdfs() {
    const { data } = await supabase
      .from('pdf_publications')
      .select('*')
      .order('created_at', { ascending: false });

    if (data) {
      setPdfs(data);
    }
    setLoading(false);
  }

  async function handleGenerate() {
    setIsGenerating(true);
    try {
      const response = await fetch('/api/generate', { method: 'POST' });
      if (response.ok) {
        await fetchPdfs(); // Odświeża tabelę po wygenerowaniu
      }
    } catch (error) {
      console.error("Błąd podczas generowania:", error);
    }
    setIsGenerating(false);
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-slate-800">AquaStart - Panel Publikacji</h1>
          <button 
            onClick={handleGenerate}
            disabled={isGenerating}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-2 rounded-lg font-medium transition-colors"
          >
            {isGenerating ? 'Generowanie...' : '+ Nowy PDF'}
          </button>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-gray-100 text-slate-600 text-sm">
                <th className="p-4 font-medium">Tytuł publikacji</th>
                <th className="p-4 font-medium">Typ</th>
                <th className="p-4 font-medium">Data wygenerowania</th>
                <th className="p-4 font-medium text-right">Akcje</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={4} className="p-8 text-center text-slate-500">Ładowanie bazy danych...</td>
                </tr>
              ) : pdfs.length === 0 ? (
                <tr>
                  <td colSpan={4} className="p-8 text-center text-slate-500">
                    Brak publikacji. Wygeneruj swój pierwszy e-book.
                  </td>
                </tr>
              ) : (
                pdfs.map((pdf) => (
                  <tr key={pdf.id} className="border-b border-gray-50 hover:bg-slate-50 transition-colors">
                    <td className="p-4 font-medium text-slate-800">{pdf.title}</td>
                    <td className="p-4">
                      <span className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm font-medium">
                        {pdf.type}
                      </span>
                    </td>
                    <td className="p-4 text-slate-600">
                      {new Date(pdf.created_at).toLocaleDateString('pl-PL')}
                    </td>
                    <td className="p-4 text-right">
                      <button className="text-blue-600 hover:text-blue-800 font-medium text-sm">
                        Pobierz
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
