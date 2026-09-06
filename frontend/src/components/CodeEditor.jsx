import { useMemo, useState } from "react";
import { ChevronDown, Eraser } from "lucide-react";
import { LANGUAGES } from "../data/languages";
import ReviewButton from "./ReviewButton";

const TAB_SIZE = 2;

export default function CodeEditor({
  code,
  language,
  isLoading = false,
  onCodeChange,
  onLanguageChange,
  onReview,
  onClear,
}) {
  const [scrollTop, setScrollTop] = useState(0);

  const lineNumbers = useMemo(
    () => Array.from({ length: Math.max(code.split("\n").length, 1) }, (_, i) => i + 1),
    [code],
  );

  const handleKeyDown = (event) => {
    if (event.key !== "Tab") return;
    event.preventDefault();
    const textarea = event.currentTarget;
    const { selectionStart, selectionEnd } = textarea;
    const indentation = " ".repeat(TAB_SIZE);
    const next = code.slice(0, selectionStart) + indentation + code.slice(selectionEnd);
    onCodeChange(next);
    requestAnimationFrame(() => {
      textarea.selectionStart = textarea.selectionEnd = selectionStart + indentation.length;
    });
  };

  return (
    <section className="flex flex-col rounded-lg border border-slate-200 bg-white shadow-sm">
      <header className="flex flex-wrap items-center justify-between gap-x-4 gap-y-2 border-b border-slate-100 px-4 py-3">
        <h2 className="text-sm font-semibold text-slate-900">Your Code</h2>
        <label className="flex items-center gap-2 text-xs font-medium text-slate-500">
          <span className="sr-only sm:not-sr-only">Language</span>
          <span className="relative inline-flex">
            <select
              value={language}
              onChange={(event) => onLanguageChange(event.target.value)}
              disabled={isLoading}
              className="h-8 cursor-pointer appearance-none rounded-md border border-slate-200 bg-white pl-2.5 pr-8 text-sm text-slate-800 shadow-sm outline-none transition-colors hover:border-slate-300 focus-visible:border-indigo-400 focus-visible:ring-2 focus-visible:ring-indigo-500/20 disabled:cursor-not-allowed disabled:bg-slate-50"
            >
              {LANGUAGES.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <ChevronDown
              className="pointer-events-none absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
              aria-hidden="true"
            />
          </span>
        </label>
      </header>

      <div className="flex h-72 overflow-hidden border-b border-slate-100 sm:h-96">
        {/* Line numbers gutter, scroll-synced with the textarea. */}
        <div
          aria-hidden="true"
          className="w-11 shrink-0 select-none overflow-hidden border-r border-slate-100 bg-slate-50/70"
        >
          <div className="py-3" style={{ transform: `translateY(${-scrollTop}px)` }}>
            {lineNumbers.map((number) => (
              <div
                key={number}
                className="px-2 text-right text-xs leading-6 tabular-nums text-slate-400"
              >
                {number}
              </div>
            ))}
          </div>
        </div>

        <textarea
          value={code}
          onChange={(event) => onCodeChange(event.target.value)}
          onScroll={(event) => setScrollTop(event.target.scrollTop)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          spellCheck={false}
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="off"
          wrap="off"
          rows={8}
          placeholder="Paste your code here..."
          aria-label="Code to review"
          className="h-full min-w-0 flex-1 resize-none overflow-auto whitespace-pre bg-white px-4 py-3 font-mono text-sm leading-6 text-slate-800 caret-indigo-500 outline-none placeholder:text-slate-400 disabled:cursor-not-allowed"
        />
      </div>

      <footer className="flex items-center justify-between gap-3 px-4 py-3">
        <button
          type="button"
          onClick={onClear}
          disabled={isLoading || !code.trim()}
          className="inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-sm font-medium text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <Eraser className="h-4 w-4" aria-hidden="true" />
          Clear
        </button>
        <ReviewButton
          onClick={onReview}
          isLoading={isLoading}
          disabled={!code.trim()}
        />
      </footer>
    </section>
  );
}