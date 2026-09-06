import { FileCode2 } from "lucide-react";

export default function Header() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex w-full max-w-6xl items-center gap-3 px-4 py-5 sm:px-6 lg:px-8">
        <span className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-indigo-100 bg-indigo-50 text-indigo-600">
          <FileCode2 className="h-5 w-5" aria-hidden="true" />
        </span>
        <div className="min-w-0">
          <h1 className="text-base font-semibold tracking-tight text-slate-900 sm:text-lg">
            Code Reviewer
          </h1>
          <p className="truncate text-sm text-slate-500">
            Analyze your code for readability, security, and potential bugs.
          </p>
        </div>
      </div>
    </header>
  );
}