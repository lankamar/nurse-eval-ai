import { useMemo } from "react";
import AdminDashboard from "./pages/AdminDashboard";
import ChatbotPage from "./pages/ChatbotPage";
import LoginPage from "./pages/LoginPage";
import { AuthProvider } from "./context/AuthContext";
import { EvaluationProvider } from "./context/EvaluationContext";

function App() {
  const isAuthed = useMemo(() => false, []);

  return (
    <AuthProvider>
      <EvaluationProvider>
        <main className="min-h-screen flex flex-col gap-6 p-6">
          <header className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-semibold">NurseEval AI</h1>
              <p className="text-sm text-gray-300">Evaluación conversacional con rúbrica oficial</p>
            </div>
          </header>

          {!isAuthed ? (
            <LoginPage />
          ) : (
            <div className="grid md:grid-cols-2 gap-4">
              <ChatbotPage />
              <AdminDashboard />
            </div>
          )}
        </main>
      </EvaluationProvider>
    </AuthProvider>
  );
}

export default App;
