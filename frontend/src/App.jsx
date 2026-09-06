import { useState } from "react";
import Header from "./components/Header";
import CodeEditor from "./components/CodeEditor";
import ReviewResults from "./components/ReviewResults";
import { useReview } from "./hooks/useReview";

export default function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const { status, result, runReview, reset } = useReview();

  const handleReview = () => {
    if (!code.trim() || status === "loading") return;
    runReview({ code, language });
  };

  const handleClear = () => {
    setCode("");
    setLanguage("python");
    reset();
  };

  return (
    <div className="flex min-h-screen flex-col bg-background text-slate-800">
      <Header />

      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        <div className="grid items-start gap-5 lg:grid-cols-2 lg:gap-6">
          <CodeEditor
            code={code}
            language={language}
            isLoading={status === "loading"}
            onCodeChange={setCode}
            onLanguageChange={setLanguage}
            onReview={handleReview}
            onClear={handleClear}
          />
          <ReviewResults
            status={status}
            result={result}
            onRetry={handleReview}
          />
        </div>
      </main>

      <footer className="border-t border-slate-200 bg-white py-4">
        <p className="mx-auto w-full max-w-6xl px-4 text-center text-xs text-slate-400 sm:px-6 lg:px-8">
          Code Reviewer · Measures readability, security, and bug risk.
        </p>
      </footer>
    </div>
  );
}