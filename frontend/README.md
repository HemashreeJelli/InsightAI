# InsightAI - React Web App Client

This is the user dashboard frontend client for **InsightAI**, a premium, glassmorphic conversational dashboard designed for interaction with research documents.

---

## ✨ Features & Architecture

* **Glassmorphic UI**: High-fidelity dark mode containing Harmonious gradients, custom scrollbars, and dynamic glowing overlays.
* **Micro-Animations**: Features custom cursor tracking interactive effects (`components/CustomCursor.tsx`) and high-performance React transitions.
* **Document Dashboard (`components/DocumentManager.tsx`)**: Easily upload documents, track file-size metadata, check process statuses, and delete indexed items.
* **Interactive Chat (`components/ChatInterface.tsx`)**: Fully scrollable message list with markdown support, active prompt history, standalone query previews, and citation links.
* **API Connector (`hooks/useAPI.ts`)**: Custom TypeScript hooks wrapping fetch logic for talking to the FastAPI backend, utilizing full error handling and loading indicators.

---

## 🛠️ Tech Stack & Styling

* **Framework**: React (v19) + Vite + TypeScript (v6)
* **Styling**: Tailwind CSS (v4) with PostCSS and custom modern properties
* **Icons**: Lucide React
* **Code Editor Configs**: ESLint & TypeScript App configurations loaded for rigid type safety

---

## 🚀 Local Setup & Installation

### **1. Prerequisites**
* Node.js (v18 or higher)
* Active backend server running (typically on `http://localhost:8000`)

### **2. Navigate and Install**
Navigate to this directory:
```bash
cd frontend
```
Install the package dependencies:
```bash
npm install
```

### **3. Environment Configuration**
By default, the client talks to `http://localhost:8000` as the backend URL. To customize this, Vite reads the `VITE_API_URL` environment variable.
Create a `.env` file inside the `frontend` folder:
```env
VITE_API_URL=http://localhost:8000
```

### **4. Start Development Server**
Launch the hot-reloading development server:
```bash
npm run dev
```
Open the provided browser address (usually **`http://localhost:5173`**) to see your application!

---

## 📦 Build for Production

To bundle the application for production (which outputs optimized assets into the `dist/` directory):
```bash
npm run build
```

To preview the built production bundle locally:
```bash
npm run preview
```
