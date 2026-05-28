import { useState, useEffect, useCallback } from 'react';

export interface DocumentInfo {
  filename: string;
  size_bytes: number;
  status: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  standalone_query?: string;
  citations?: Array<{ filename: string; page_number: number }>;
}

const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '') + '/api';

export function useAPI() {
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isChatting, setIsChatting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [serverOnline, setServerOnline] = useState<boolean | null>(null);

  // Ping Server Health Status
  const checkHealth = useCallback(async () => {
    try {
      const response = await fetch(API_BASE_URL.replace('/api', '/'));
      if (response.ok) {
        setServerOnline(true);
      } else {
        setServerOnline(false);
      }
    } catch {
      setServerOnline(false);
    }
  }, []);

  // Fetch all uploaded documents
  const fetchDocuments = useCallback(async () => {
    try {
      setError(null);
      const response = await fetch(`${API_BASE_URL}/documents`);
      if (!response.ok) {
        throw new Error(`Failed to fetch documents: ${response.statusText}`);
      }
      const data = await response.json();
      setDocuments(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Failed to list documents.');
    }
  }, []);

  // Upload document
  const uploadDocument = async (file: File) => {
    setIsUploading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to upload document.');
      }

      await fetchDocuments(); // Refresh document inventory list
      return await response.json();
    } catch (err: any) {
      setError(err.message || 'An error occurred during upload.');
      throw err;
    } finally {
      setIsUploading(false);
    }
  };

  // Delete document
  const deleteDocument = async (filename: string) => {
    setError(null);
    try {
      // Optimistic state update for instant responsive click feedback
      setDocuments(prev => prev.filter(doc => doc.filename !== filename));

      const response = await fetch(`${API_BASE_URL}/documents/${encodeURIComponent(filename)}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        // Rollback optimistic state on error
        await fetchDocuments();
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to delete document.');
      }

      return await response.json();
    } catch (err: any) {
      setError(err.message || 'An error occurred during deletion.');
      throw err;
    }
  };

  // Clear Chat History
  const clearChat = () => {
    setChatHistory([]);
  };

  // Send message in the chat Q&A session
  const sendChatMessage = async (message: string, selectedFiles: string[]) => {
    if (!message.trim()) return;

    setIsChatting(true);
    setError(null);

    // 1. Add user message instantly to visual chat thread
    const userMsg: ChatMessage = { role: 'user', content: message };
    setChatHistory(prev => [...prev, userMsg]);

    try {
      // Map chatHistory to expected API message formats
      const apiHistory = chatHistory.map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      const payload = {
        message,
        history: apiHistory,
        filenames: selectedFiles.length > 0 ? selectedFiles : null
      };

      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to generate answer.');
      }

      const data = await response.json();

      // 2. Add AI response details to history
      const assistantMsg: ChatMessage = {
        role: 'assistant',
        content: data.answer,
        standalone_query: data.standalone_query,
        citations: data.citations
      };

      setChatHistory(prev => [...prev, assistantMsg]);
    } catch (err: any) {
      setError(err.message || 'An error occurred during conversational retrieval.');
      // Append a special assistant message displaying the error for clean dialog context
      const errorMsg: ChatMessage = {
        role: 'assistant',
        content: `Error: ${err.message || 'Could not communicate with the RAG server.'}`
      };
      setChatHistory(prev => [...prev, errorMsg]);
    } finally {
      setIsChatting(false);
    }
  };

  // Run health check and fetch doc list on mount
  useEffect(() => {
    checkHealth();
    fetchDocuments();
  }, [checkHealth, fetchDocuments]);

  return {
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
    refreshDocuments: fetchDocuments,
    checkHealth
  };
}
