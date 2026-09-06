import { Loader2, Play } from "lucide-react";

export default function ReviewButton({ onClick, isLoading = false, disabled = false }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled || isLoading}
      className="inline-flex min-w-36 items-center justify-center gap-2 rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition-colors hover:bg-indigo-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:cursor-not-allowed disabled:opacity-60"
    >
      {isLoading ? (
        <>
          <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
          Reviewing...
        </>
      ) : (
        <>
          <Play className="h-4 w-4" aria-hidden="true" />
          Review Code
        </>
      )}
    </button>
  );
}