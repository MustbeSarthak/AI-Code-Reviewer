import { Bug, ClipboardList, Gauge, Lightbulb, ShieldCheck } from "lucide-react";
import LoadingState from "./LoadingState";
import ErrorState from "./ErrorState";
import ScoreCard from "./ScoreCard";

const CATEGORIES = [
  {
    key: "readability",
    label: "Readability",
    icon: Lightbulb,
    iconClass: "border-indigo-100 bg-indigo-50 text-indigo-600",
    barClass: "bg-indigo-500",
    scoreClass: "text-indigo-600",
  },
  {
    key: "security",
    label: "Security",
    icon: ShieldCheck,
    iconClass: "border-blue-100 bg-blue-50 text-blue-600",
    barClass: "bg-blue-500",
    scoreClass: "text-blue-600",
  },
  {
    key: "bugs",
    label: "Bugs",
    icon: Bug,
    iconClass: "border-slate-200 bg-slate-100 text-slate-600",
    barClass: "bg-slate-600",
    scoreClass: "text-slate-700",
  },
];

function EmptyState() {
  return (
    <div className="flex min-h-[22rem] flex-col items-center justify-center rounded-md border border-dashed border-slate-200 bg-slate-50/50 px-6 py-10 text-center">
      <span className="flex h-10 w-10 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-400">
        <ClipboardList className="h-5 w-5" aria-hidden="true" />
      </span>
      <h3 className="mt-4 text-sm font-semibold text-slate-900">
        Ready to review
      </h3>
      <p className="mt-1 max-w-60 text-sm leading-5 text-slate-500">
        Paste your code and click "Review Code" to analyze it.
      </p>
    </div>
  );
}

function ResultView({ result }) {
  const overall = Math.round(
    CATEGORIES.reduce(
      (sum, category) => sum + (result[category.key]?.score ?? 0),
      0,
    ) / CATEGORIES.length,
  );
  return (
    <div className="grid gap-3">
      <section
        aria-label="Overall review"
        className="rounded-lg border border-slate-200 bg-slate-50/70 p-4"
      >
        <div className="flex items-center justify-between gap-3">
          <p className="flex items-center gap-2 text-sm font-semibold text-slate-900">
            <Gauge className="h-4 w-4 text-slate-400" aria-hidden="true" />
            Overall review
          </p>
          <p className="text-sm font-semibold tabular-nums text-slate-900">
            {overall}
            <span className="font-normal text-slate-400"> / 100</span>
          </p>
        </div>
        <div
          className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-200/70"
          role="progressbar"
          aria-valuenow={overall}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label="Overall score"
        >
          <div
            className="h-full rounded-full bg-indigo-500"
            style={{ width: `${overall}%` }}
          />
        </div>
      </section>

      {CATEGORIES.map((category) => {
        const data = result[category.key] ?? {};
        return (
          <ScoreCard
            key={category.key}
            title={category.label}
            icon={category.icon}
            score={data.score}
            suggestions={data.suggestions}
            iconClass={category.iconClass}
            barClass={category.barClass}
            scoreClass={category.scoreClass}
          />
        );
      })}
    </div>
  );
}

export default function ReviewResults({ status, result, onRetry }) {
  let content = <EmptyState />;

  if (status === "loading") {
    content = <LoadingState />;
  } else if (status === "error") {
    content = <ErrorState onRetry={onRetry} />;
  } else if (status === "success" && result) {
    content = <ResultView result={result} />;
  }

  return (
    <section
      className="rounded-lg border border-slate-200 bg-white shadow-sm"
      aria-live="polite"
    >
      <header className="border-b border-slate-100 px-4 py-3">
        <h2 className="text-sm font-semibold text-slate-900">Review Results</h2>
      </header>
      <div className="p-4">{content}</div>
    </section>
  );
}