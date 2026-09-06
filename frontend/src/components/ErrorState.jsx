import { AlertTriangle, RotateCcw } from "lucide-react";

export default function ErrorState({ onRetry }) {
  return (
    <div className="flex min-h-[22rem] flex-col items-center justify-center rounded-md border border-red-100 bg-red-50/60 px-6 py-10 text-center">
      <span className="flex h-10 w-10 items-center justify-center rounded-lg border border-red-100 bg-white text-red-500">
        <AlertTriangle className="h-5 w-5" aria-hidden="true" />
      </span>
      <h3 className="mt-4 text-sm font-semibold text-slate-900">
        Unable to review code
      </h3>
      <p className="mt-1 max-w-80 text-sm leading-5 text-slate-600">
        Something went wrong while analyzing your code. Please try again.
      </p>
      <button
        type="button"
        onClick={onRetry}
        className="mt-4 inline-flex items-center gap-2 rounded-md border border-slate-200 bg-white px-3.5 py-2 text-sm font-medium text-slate-700 shadow-sm transition-colors hover:bg-slate-50"
      >
        <RotateCcw className="h-4 w-4" aria-hidden="true" />
        Try again
      </button>
    </div>
  );
}