"use client";
import { useState, useEffect } from "react";

interface SongSuggestion {
  id: number;
  title: string;
  artist: string;
  art: string;
}

export default function Home() {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState<SongSuggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch live suggestions from backend when typing
  useEffect(() => {
    if (query.trim().length < 2) {
      setSuggestions([]);
      return;
    }

    const timer = setTimeout(async () => {
      setIsLoading(true);
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        if (data.results) {
          setSuggestions(data.results);
        }
      } catch (err) {
        console.error("Search error:", err);
      } finally {
        setIsLoading(false);
      }
    }, 300); // 300ms debounce to avoid spamming the API

    return () => clearTimeout(timer);
  }, [query]);

  return (
    <main className="min-h-screen bg-[#0a0a0c] text-white flex flex-col items-center pt-32 px-4 font-sans">
      
      {/* Hero Section */}
      <div className="text-center mb-10">
        <h1 className="text-5xl font-extrabold tracking-widest mb-2">
          ALGO<span className="text-red-500">RHYTHM</span>
        </h1>
        <p className="text-zinc-400 italic tracking-wide">
          The Code Behind the Culture.
        </p>
      </div>

      {/* Smart Search Bar Container */}
      <div className="w-full max-w-2xl relative">
        <div className="flex bg-[#121216] border border-zinc-800 rounded-xl overflow-hidden shadow-2xl focus-within:border-red-500 transition-colors">
          <input
            type="text"
            className="flex-1 bg-transparent py-4 px-6 text-lg outline-none placeholder-zinc-500"
            placeholder="Search a track (e.g., Runaway Kanye West or Devara)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button className="bg-red-600 hover:bg-red-700 text-white font-bold py-4 px-8 transition-colors">
            DECODE
          </button>
        </div>

        {/* Live Suggestions Dropdown */}
        {suggestions.length > 0 && (
          <div className="absolute top-full left-0 right-0 mt-2 bg-[#121216] border border-zinc-800 rounded-xl overflow-hidden shadow-2xl z-50 max-h-80 overflow-y-auto">
            {suggestions.map((song) => (
              <div 
                key={song.id}
                onClick={() => {
                  setQuery(`${song.title} ${song.artist}`);
                  setSuggestions([]);
                }}
                className="py-3 px-6 hover:bg-zinc-800 cursor-pointer flex justify-between items-center transition-colors border-b border-zinc-800/50 last:border-0"
              >
                <div className="flex items-center gap-3">
                  {song.art && (
                    <img src={song.art} alt={song.title} className="w-10 h-10 rounded object-cover" />
                  )}
                  <div>
                    <div className="font-bold">{song.title}</div>
                    <div className="text-zinc-400 text-xs">{song.artist}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {isLoading && (
          <div className="absolute top-full left-0 right-0 mt-2 bg-[#121216] p-4 text-center text-zinc-500 text-sm rounded-xl border border-zinc-800">
            Searching archives...
          </div>
        )}
      </div>

    </main>
  );
}