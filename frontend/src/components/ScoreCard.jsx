import SuggestionList from "./SuggestionList";

export default function ScoreCard({
  title,
  icon: Icon,
  score = 0,
  suggestions = [],
  iconClass = "border-slate-200 bg-slate-100 text-slate-600",
  barClass = "bg-slate-600",
  scoreClass = "text-slate-700",
}) {
  const safeScore = Number.isFinite(Number(score))
    ? Math.min(100, Math.max(0, Math.round(Number(score))))
    : 0;

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <span
            className={`inline-flex h-7 w-7 shrink-0 items-center justify-center rounded-md border ${iconClass}`}
          >
            <Icon className="h-4 w-4" aria-hidden="true" />
          </span>
          <h3 className="text-sm font-semibold text-slate-900">{title}</h3>
        </div>
        <p className={`text-sm font-semibold tabular-nums ${scoreClass}`}>
          {safeScore}
          <span className="font-normal text-slate-400"> / 100</span>
        </p>
      </div>

      <div
        className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-100"
        role="progressbar"
        aria-valuenow={safeScore}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`${title} score`}
      >
        <div
          className={`h-full rounded-full ${barClass}`}
          style={{ width: `${safeScore}%` }}
        />
      </div>

      <div className="mt-4">
        <p className="text-[11px] font-semibold uppercase tracking-wide text-slate-400">
          Suggestions
        </p>
        <SuggestionList items={suggestions} />
      </div>
    </section>
  );
}