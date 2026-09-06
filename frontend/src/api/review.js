const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/+$/, "");

function normalizeScore(value) {
  const score = Number(value);
  if (!Number.isFinite(score)) return 0;
  return Math.min(100, Math.max(0, Math.round(score)));
}

function normalizeCategory(raw) {
  const category = raw && typeof raw === "object" ? raw : {};
  const suggestions = Array.isArray(category.suggestions)
    ? category.suggestions.filter((item) => typeof item === "string").slice(0, 12)
    : [];

  return {
    score: normalizeScore(category.score),
    suggestions,
  };
}

/**
 * Send code to the review API and return a normalized result.
 *
 * @param {{ code: string, language: string }} payload
 */
export async function reviewCode({ code, language }) {
  const response = await fetch(`${API_BASE_URL}/review`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code, language }),
  });

  if (!response.ok) {
    throw new Error(`Review request failed with status ${response.status}`);
  }

  const data = await response.json();

  return {
    readability: normalizeCategory(data.readability),
    security: normalizeCategory(data.security),
    bugs: normalizeCategory(data.bugs),
  };
}