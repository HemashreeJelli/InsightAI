import { Server, Wifi, WifiOff } from 'lucide-react';

interface HeaderProps {
  serverOnline: boolean | null;
  documentsCount: number;
}

export default function Header({ serverOnline, documentsCount }: HeaderProps) {
  return (
    <header className="w-full border-b border-paper-dark py-4 md:py-6 px-4 md:px-8 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-paper-light shadow-paper-sm animate-fade-in">
      <div className="flex flex-col">
        <h1 className="font-serif font-black text-2xl md:text-3xl tracking-tight text-charcoal select-none my-0 py-0 flex items-center gap-2">
          Insight<span className="text-accent-orange">AI</span>
        </h1>
        <p className="font-sans font-medium text-[10px] md:text-xs tracking-wider text-charcoal/50 uppercase mt-0.5">
          Smart RAG Research Workspace
        </p>
      </div>

      <div className="flex flex-wrap items-center gap-3 sm:gap-6 font-sans">
        {/* Document Stats Badge */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-paper border border-paper-dark">
          <span className="w-1.5 h-1.5 rounded-full bg-accent-orange animate-ping" />
          <span className="text-xs font-semibold text-charcoal/70 uppercase tracking-wider">
            {documentsCount} {documentsCount === 1 ? 'Paper' : 'Papers'} Loaded
          </span>
        </div>

        {/* Server Connection Heartbeat Badge */}
        <div 
          className={`flex items-center gap-2 px-3.5 py-1.5 rounded-md border text-xs font-bold uppercase tracking-wider transition-all duration-300 ${
            serverOnline === true 
              ? 'bg-[#f0fdf4] border-[#bbf7d0] text-emerald-700 shadow-sm'
              : serverOnline === false
                ? 'bg-[#fef2f2] border-[#fecaca] text-rose-700 animate-pulse'
                : 'bg-paper border-paper-dark text-charcoal/45'
          }`}
        >
          {serverOnline === true ? (
            <>
              <Wifi className="w-4 h-4" />
              <span>RAG Engine Online</span>
            </>
          ) : serverOnline === false ? (
            <>
              <WifiOff className="w-4 h-4" />
              <span>Engine Offline</span>
            </>
          ) : (
            <>
              <Server className="w-4 h-4 animate-bounce" />
              <span>Pinging Status...</span>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
