export default function SuggestionList({ items }) {
  if (!Array.isArray(items) || items.length === 0) {
    return (
      <p className="mt-2 text-sm text-slate-500">
        Nothing specific found for this category.
      </p>
    );
  }

  return (
    <ul className="mt-2 space-y-1.5">
      {items.map((item, index) => (
        <li
          key={index}
          className="flex items-start gap-2.5 text-sm leading-5 text-slate-600"
        >
          <span
            className="mt-[7px] h-1 w-1 shrink-0 rounded-full bg-slate-300"
            aria-hidden="true"
          />
          {item}
        </li>
      ))}
    </ul>
  );
}