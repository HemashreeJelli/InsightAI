import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, Trash2, Loader, BookOpen, Sparkles } from 'lucide-react';
import type { DocumentInfo } from '../hooks/useAPI';

interface DocumentManagerProps {
  documents: DocumentInfo[];
  isUploading: boolean;
  onUpload: (file: File) => Promise<any>;
  onDelete: (filename: string) => Promise<any>;
}

export default function DocumentManager({
  documents,
  isUploading,
  onUpload,
  onDelete
}: DocumentManagerProps) {
  const [isDragActive, setIsDragActive] = useState(false);
  const [deletingFile, setDeletingFile] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Trigger file browser click
  const triggerFileSelect = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      await processUpload(e.target.files[0]);
    }
  };

  // Drag and Drop triggers
  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragActive(true);
    } else if (e.type === "dragleave") {
      setIsDragActive(false);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === "application/pdf" || file.name.endsWith(".pdf")) {
        await processUpload(file);
      } else {
        alert("Only PDF documents are currently supported.");
      }
    }
  };

  const processUpload = async (file: File) => {
    if (documents.length >= 5) {
      alert("Library limit reached: You can index a maximum of 5 research papers. Please delete a paper below to free up space.");
      return;
    }
    try {
      await onUpload(file);
    } catch (err: any) {
      console.error(err);
      alert(err.message || "Failed to process research document.");
    }
  };

  const handleDeleteClick = async (e: React.MouseEvent, filename: string) => {
    e.stopPropagation();
    if (confirm(`Are you sure you want to purge "${filename}" and all its index chunks from the database?`)) {
      try {
        setDeletingFile(filename);
        await onDelete(filename);
      } catch (err: any) {
        alert(err.message || "Failed to delete document.");
      } finally {
        setDeletingFile(null);
      }
    }
  };

  // Helper to format bytes into readable scale
  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = 2;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  };

  return (
    <div className="flex flex-col gap-6 w-full h-full font-sans animate-fade-in-up">
      {/* Upload Section */}
      <div className="editorial-card p-6 rounded-lg relative overflow-hidden flex flex-col items-center justify-center">
        {/* Upload overlay */}
        {isUploading && (
          <div className="absolute inset-0 bg-paper-light z-10 flex flex-col items-center justify-center p-6 text-center animate-fade-in">
            <Loader className="w-10 h-10 text-accent-orange animate-spin mb-4" />
            <h3 className="font-serif font-bold text-lg text-charcoal">Ingesting Research Document</h3>
            <p className="text-xs text-charcoal/60 max-w-[280px] leading-relaxed mt-2">
              Running text extraction, splitting content into semantic blocks, and storing vector embeddings...
            </p>
          </div>
        )}

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="hidden"
        />

        <div
          onDragEnter={documents.length >= 5 ? undefined : handleDrag}
          onDragOver={documents.length >= 5 ? undefined : handleDrag}
          onDragLeave={documents.length >= 5 ? undefined : handleDrag}
          onDrop={documents.length >= 5 ? undefined : handleDrop}
          onClick={documents.length >= 5 ? () => alert("Library limit reached: Please delete a document below to upload a new one.") : triggerFileSelect}
          className={`w-full py-8 border-2 border-dashed rounded-lg flex flex-col items-center justify-center p-4 transition-all duration-300 ${
            documents.length >= 5
              ? 'border-paper-dark/60 bg-paper-dark/25 cursor-not-allowed opacity-70'
              : isDragActive 
                ? 'border-accent-orange bg-accent-orange/5 scale-[1.01]' 
                : 'border-paper-dark hover:border-accent-orange/50 hover:bg-paper-light'
          }`}
          role="button"
        >
          <UploadCloud className={`w-12 h-12 mb-3 transition-transform duration-300 ${
            documents.length >= 5 ? 'text-charcoal/30' : 'text-accent-orange hover:scale-110'
          }`} />
          <h3 className="font-serif font-bold text-base text-charcoal">
            {documents.length >= 5 ? 'Library Limit Reached' : 'Upload PDF Paper'}
          </h3>
          <p className="text-xs text-charcoal/50 mt-1 max-w-[240px] text-center leading-relaxed">
            {documents.length >= 5 
              ? 'You have uploaded 5/5 papers. Delete a paper below to free up space.' 
              : 'Drag and drop your research manuscript here, or click to browse files.'}
          </p>
          <div className="flex items-center gap-1 mt-4 px-2.5 py-1 rounded bg-paper-dark border border-paper-dark/10">
            <Sparkles className={`w-3.5 h-3.5 ${documents.length >= 5 ? 'text-charcoal/45' : 'text-accent-orange'}`} />
            <span className="text-[10px] font-bold text-charcoal/60 uppercase tracking-wider">
              {documents.length >= 5 ? 'Limit: 5/5 Papers' : 'Indexed Instantly'}
            </span>
          </div>
        </div>
      </div>

      {/* Inventory Section */}
      <div className="flex flex-col flex-1 gap-4 min-h-[300px]">
        <div className="flex items-center gap-2 border-b border-paper-dark pb-2">
          <BookOpen className="w-4 h-4 text-accent-orange" />
          <h2 className="font-serif font-extrabold text-lg text-charcoal my-0 select-none">
            Research Library
          </h2>
        </div>

        {documents.length === 0 ? (
          <div className="flex-1 border border-dashed border-paper-dark/60 rounded-lg flex flex-col items-center justify-center p-8 text-center text-charcoal/40 bg-paper-light/30">
            <FileText className="w-10 h-10 stroke-1 mb-2 opacity-50" />
            <span className="text-sm font-semibold tracking-wide">Library is empty</span>
            <p className="text-[11px] max-w-[200px] leading-relaxed mt-1">
              Add your first PDF document above to index its data for Q&A.
            </p>
          </div>
        ) : (
          <div className="flex flex-col gap-2 overflow-y-auto max-h-[400px] pr-1">
            {documents.map((doc, idx) => (
              <div
                key={doc.filename}
                className="group flex justify-between items-center p-3 rounded-lg border border-paper-dark bg-paper-light/60 hover:bg-paper-light hover:border-accent-orange/30 shadow-paper-sm transition-all duration-300 animate-fade-in-up"
                style={{ animationDelay: `${idx * 0.05}s` }}
              >
                <div className="flex items-center gap-3 overflow-hidden">
                  <div className="p-2 rounded bg-accent-orange/5 border border-accent-orange/10 text-accent-orange">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div className="flex flex-col text-left overflow-hidden">
                    <span 
                      className="font-sans font-bold text-xs text-charcoal truncate max-w-[200px] hover:text-accent-orange transition-colors"
                      title={doc.filename}
                    >
                      {doc.filename.replace(/\.pdf$/i, '')}
                    </span>
                    <span className="text-[10px] font-semibold text-charcoal/45 mt-0.5">
                      {formatBytes(doc.size_bytes)}
                    </span>
                  </div>
                </div>

                <button
                  onClick={(e) => handleDeleteClick(e, doc.filename)}
                  disabled={deletingFile === doc.filename}
                  className="p-2 rounded-md border border-paper-dark hover:border-rose-200 hover:bg-rose-50 text-charcoal/40 hover:text-rose-600 transition-all duration-300"
                  aria-label="Purge Document"
                >
                  {deletingFile === doc.filename ? (
                    <Loader className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <Trash2 className="w-3.5 h-3.5" />
                  )}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
