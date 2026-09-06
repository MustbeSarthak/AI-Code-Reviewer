import { Loader2 } from "lucide-react";

export default function LoadingState() {
  return (
    <div className="flex min-h-[22rem] flex-col items-center justify-center px-6 py-10 text-center">
      <Loader2 className="h-5 w-5 animate-spin text-slate-400" aria-hidden="true" />
      <h3 className="mt-4 text-sm font-semibold text-slate-900">
        Reviewing your code
      </h3>
      <p className="mt-1 text-sm text-slate-500">
        Analyzing readability, security, and bug risk…
      </p>
    </div>
  );
}