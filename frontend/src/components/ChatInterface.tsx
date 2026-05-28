import React, { useState, useEffect, useRef } from 'react';
import { Send, Loader, MessageSquare, Sparkles, Layers, CheckSquare, Square, Trash2 } from 'lucide-react';
import type { ChatMessage, DocumentInfo } from '../hooks/useAPI';

interface ChatInterfaceProps {
  chatHistory: ChatMessage[];
  documents: DocumentInfo[];
  isChatting: boolean;
  onSendMessage: (message: string, selectedFiles: string[]) => Promise<any>;
  onClearChat: () => void;
}

export default function ChatInterface({
  chatHistory,
  documents,
  isChatting,
  onSendMessage,
  onClearChat
}: ChatInterfaceProps) {
  const [input, setInput] = useState('');
  const [selectedFiles, setSelectedFiles] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat window when new messages arrive
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, isChatting]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isChatting) return;

    const messageToSend = input;
    setInput('');
    await onSendMessage(messageToSend, selectedFiles);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Toggle filtering specific documents
  const toggleFileFilter = (filename: string) => {
    setSelectedFiles(prev => 
      prev.includes(filename) 
        ? prev.filter(f => f !== filename) 
        : [...prev, filename]
    );
  };

  // Basic formatter to render bold, list items, and paragraph headers in research responses
  const renderFormattedText = (text: string) => {
    // Escape simple HTML characters to prevent XSS
    const paragraphs = text.split('\n\n');
    return (
      <div className="prose-custom">
        {paragraphs.map((p, idx) => {
          let line = p.trim();
          if (!line) return null;

          // Render bullet list blocks
          if (line.startsWith('- ') || line.startsWith('* ')) {
            const listItems = line.split(/\n[-*] /);
            return (
              <ul key={idx}>
                {listItems.map((item, itemIdx) => (
                  <li key={itemIdx}>{item.replace(/^[-*] /, '')}</li>
                ))}
              </ul>
            );
          }

          // Format subheadings (e.g. "### Heading" or "Heading:")
          if (line.startsWith('### ') || line.startsWith('## ') || line.startsWith('**') && line.endsWith('**')) {
            const headingText = line.replace(/^(###|##|\*\*)/, '').replace(/\*\*$/, '');
            return <h3 key={idx}>{headingText}</h3>;
          }

          // Format bold highlights (`**text**`)
          const parts = [];
          const regex = /\*\*([\s\S]*?)\*\*/g;
          let lastIndex = 0;
          let match;

          while ((match = regex.exec(line)) !== null) {
            // Append standard text before bold match
            if (match.index > lastIndex) {
              parts.push(line.substring(lastIndex, match.index));
            }
            // Append bold formatted text
            parts.push(<strong key={match.index} className="font-extrabold text-charcoal">{match[1]}</strong>);
            lastIndex = regex.lastIndex;
          }

          if (lastIndex < line.length) {
            parts.push(line.substring(lastIndex));
          }

          return <p key={idx}>{parts.length > 0 ? parts : line}</p>;
        })}
      </div>
    );
  };

  return (
    <div className="editorial-card rounded-lg flex flex-col h-[580px] overflow-hidden relative font-sans animate-fade-in-up">
      {/* Scope Filtering Panel */}
      {documents.length > 0 && (
        <div className="w-full bg-paper border-b border-paper-dark p-3 flex flex-col gap-2 transition-all duration-300">
          <div className="flex items-center gap-1.5 justify-between">
            <div className="flex items-center gap-1.5 text-xs font-extrabold uppercase tracking-wider text-charcoal/60">
              <Layers className="w-3.5 h-3.5 text-accent-orange" />
              <span>Target Scope Query Filters</span>
            </div>
            {selectedFiles.length > 0 && (
              <button 
                onClick={() => setSelectedFiles([])}
                className="text-[10px] font-bold text-accent-orange hover:text-accent-orange-dark uppercase tracking-wider transition-colors"
              >
                Clear Scoping
              </button>
            )}
          </div>
          <div className="flex gap-2 overflow-x-auto py-1 pr-1 select-none">
            {documents.map(doc => {
              const isSelected = selectedFiles.includes(doc.filename);
              return (
                <div
                  key={doc.filename}
                  onClick={() => toggleFileFilter(doc.filename)}
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs font-semibold cursor-pointer transition-all duration-300 select-none whitespace-nowrap ${
                    isSelected
                      ? 'bg-accent-orange/10 border-accent-orange text-accent-orange shadow-paper-sm scale-[1.01]'
                      : 'bg-paper-light border-paper-dark text-charcoal/60 hover:border-accent-orange/30 hover:text-charcoal'
                  }`}
                  role="checkbox"
                  aria-checked={isSelected}
                >
                  {isSelected ? (
                    <CheckSquare className="w-3.5 h-3.5" />
                  ) : (
                    <Square className="w-3.5 h-3.5 opacity-55" />
                  )}
                  <span>{doc.filename.replace(/\.pdf$/i, '')}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Main Conversation Stream */}
      <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-6 bg-paper-light/20 scroll-smooth">
        {chatHistory.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center text-charcoal/40 p-8">
            <div className="p-4 rounded-full bg-accent-orange/5 border border-accent-orange/10 text-accent-orange mb-4">
              <MessageSquare className="w-10 h-10 stroke-1" />
            </div>
            <h3 className="font-serif font-bold text-lg text-charcoal">Scholarly Chat Assistant</h3>
            <p className="text-xs text-charcoal/50 max-w-[280px] leading-relaxed mt-1">
              Ask deep questions, run comparative analysis across indexed papers, or analyze specific files using the scope filters above.
            </p>
          </div>
        ) : (
          chatHistory.map((msg, idx) => (
            <div
              key={idx}
              className={`flex flex-col max-w-[85%] ${
                msg.role === 'user' ? 'self-end items-end' : 'self-start items-start'
              } animate-fade-in-up`}
            >
              {/* Message Capsule */}
              <div
                className={`p-4 rounded-lg shadow-paper-sm border text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-paper border-paper-dark text-charcoal rounded-br-none'
                    : 'bg-paper-light border-paper-dark/60 text-charcoal rounded-bl-none font-body text-left'
                }`}
              >
                {msg.role === 'user' ? (
                  <p className="font-sans font-semibold text-charcoal">{msg.content}</p>
                ) : (
                  renderFormattedText(msg.content)
                )}

                {/* Citations section */}
                {msg.role === 'assistant' && msg.citations && msg.citations.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-paper-dark/60 flex flex-col gap-2">
                    <div className="flex items-center gap-1.5 text-[10px] font-bold text-accent-orange uppercase tracking-wider">
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Verified Citations</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {msg.citations.map((cite, citeIdx) => (
                        <div
                          key={citeIdx}
                          className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#fdfbf7] border border-paper-dark text-[10px] font-bold text-charcoal/70 shadow-sm"
                        >
                          <span className="text-accent-orange font-black">#</span>
                          <span className="truncate max-w-[120px]">{cite.filename.replace(/\.pdf$/i, '')}</span>
                          <span className="px-1.5 py-0.5 rounded bg-paper-dark text-charcoal/50 text-[9px] font-extrabold">
                            Page {cite.page_number}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))
        )}

        {/* Loading Spinner during Chat Ingestion */}
        {isChatting && (
          <div className="self-start flex flex-col max-w-[85%] items-start animate-fade-in-up">
            <div className="p-4 rounded-lg shadow-paper-sm border bg-paper-light border-paper-dark text-charcoal rounded-bl-none flex items-center gap-3">
              <Loader className="w-4 h-4 text-accent-orange animate-spin" />
              <span className="text-xs font-semibold font-sans text-charcoal/60 uppercase tracking-wider">
                Retrieving vector blocks and compiling scholarly answer...
              </span>
            </div>
          </div>
        )}
        <div ref={scrollRef} />
      </div>

      {/* Floating Input Frame */}
      <form 
        onSubmit={handleSubmit}
        className="w-full p-4 border-t border-paper-dark bg-paper flex items-center gap-3 relative"
      >
        {chatHistory.length > 0 && (
          <button
            type="button"
            onClick={onClearChat}
            className="p-3 rounded-lg border border-paper-dark hover:border-rose-200 hover:bg-rose-50 text-charcoal/45 hover:text-rose-600 transition-all duration-300"
            title="Clear Chat Thread"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        )}

        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a scholarly question about your research library..."
          className="flex-1 py-3 px-4 rounded-lg bg-paper-light border border-paper-dark text-xs leading-relaxed text-charcoal placeholder-charcoal/40 focus:outline-none focus:border-accent-orange/60 shadow-inner resize-none h-11"
        />

        <button
          type="submit"
          disabled={isChatting || !input.trim()}
          className={`p-3 rounded-lg flex items-center justify-center transition-all duration-300 ${
            input.trim() && !isChatting
              ? 'bg-accent-orange hover:bg-accent-orange-dark text-white shadow-paper-sm hover:scale-[1.03]'
              : 'bg-paper-dark border border-paper-dark text-charcoal/30 cursor-not-allowed'
          }`}
          aria-label="Send Message"
        >
          {isChatting ? (
            <Loader className="w-4 h-4 animate-spin" />
          ) : (
            <Send className="w-4 h-4" />
          )}
        </button>
      </form>
    </div>
  );
}
