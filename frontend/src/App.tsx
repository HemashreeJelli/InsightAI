import { useAPI } from './hooks/useAPI';
import Header from './components/Header';
import DocumentManager from './components/DocumentManager';
import ChatInterface from './components/ChatInterface';
import CustomCursor from './components/CustomCursor';
import { AlertCircle, RotateCw } from 'lucide-react';

export default function App() {
  const {
    documents,
    chatHistory,
    isUploading,
    isChatting,
    error,
    serverOnline,
    uploadDocument,
    deleteDocument,
    sendChatMessage,
    clearChat,
    checkHealth,
    refreshDocuments
  } = useAPI();

  return (
    <div className="min-h-screen bg-paper flex flex-col items-center relative overflow-hidden select-none font-sans">
      {/* Floating custom pointer follower */}
      <CustomCursor />

      {/* Grid Dashboard Wrapper */}
      <div className="w-full max-w-7xl mx-auto px-2 sm:px-4 md:px-8 py-4 lg:py-6 flex flex-col gap-4 lg:gap-6 flex-1 h-auto lg:h-screen lg:overflow-hidden">
        {/* Editorial Brand Header */}
        <Header serverOnline={serverOnline} documentsCount={documents.length} />

        {/* Global Error Banner */}
        {error && (
          <div className="w-full flex items-center justify-between p-3.5 bg-rose-50 border border-rose-200 rounded-lg text-rose-800 text-xs font-semibold tracking-wide animate-fade-in">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0" />
              <span>{error}</span>
            </div>
            <button 
              onClick={() => { refreshDocuments(); checkHealth(); }}
              className="flex items-center gap-1 text-[10px] text-accent-orange hover:text-accent-orange-dark uppercase tracking-wider font-bold transition-all"
            >
              <RotateCw className="w-3.5 h-3.5" />
              <span>Retry</span>
            </button>
          </div>
        )}

        {/* Offline Overlay Banner */}
        {serverOnline === false && (
          <div className="w-full flex items-center justify-center p-3 bg-amber-50 border border-amber-200 rounded-lg text-amber-800 text-xs font-semibold tracking-wide animate-fade-in text-center">
            <span className="w-2 h-2 rounded-full bg-amber-600 animate-ping mr-2" />
            <span>FastAPI Server seems unreachable. Make sure your Python backend is running locally at port 8000.</span>
          </div>
        )}

        {/* Split Screen 12-Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1 min-h-0">
          {/* Left Column: Library Management (4 Columns) */}
          <div className="lg:col-span-4 flex flex-col min-h-0">
            <DocumentManager
              documents={documents}
              isUploading={isUploading}
              onUpload={uploadDocument}
              onDelete={deleteDocument}
            />
          </div>

          {/* Right Column: Q&A Retrieval Chat (8 Columns) */}
          <div className="lg:col-span-8 flex flex-col min-h-0">
            <ChatInterface
              chatHistory={chatHistory}
              documents={documents}
              isChatting={isChatting}
              onSendMessage={sendChatMessage}
              onClearChat={clearChat}
            />
          </div>
        </div>

        {/* Editorial Footer */}
        <footer className="w-full py-4 text-center border-t border-paper-dark text-[10px] font-bold text-charcoal/40 uppercase tracking-widest animate-fade-in mt-auto flex flex-col sm:flex-row justify-between items-center px-2 gap-2 sm:gap-0">
          <span>InsightAI — Editorial Intelligence System</span>
          <span>© 2026 Hemashree Jelli</span>
        </footer>
      </div>
    </div>
  );
}
