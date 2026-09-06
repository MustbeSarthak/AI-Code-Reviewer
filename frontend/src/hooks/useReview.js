import { useCallback, useReducer } from "react";
import { reviewCode } from "../api/review";

const initialState = {
  status: "idle", // "idle" | "loading" | "success" | "error"
  result: null,
  error: null,
};

function reducer(state, action) {
  switch (action.type) {
    case "start":
      return { status: "loading", result: null, error: null };
    case "success":
      return { status: "success", result: action.payload, error: null };
    case "error":
      return { status: "error", result: null, error: action.payload };
    case "reset":
      return initialState;
    default:
      return state;
  }
}

/** Small state machine that drives the review lifecycle. */
export function useReview() {
  const [state, dispatch] = useReducer(reducer, initialState);

  const runReview = useCallback(async ({ code, language }) => {
    if (!code?.trim()) return;

    dispatch({ type: "start" });
    try {
      const result = await reviewCode({ code, language });
      dispatch({ type: "success", payload: result });
    } catch (error) {
      dispatch({ type: "error", payload: error });
    }
  }, []);

  const reset = useCallback(() => dispatch({ type: "reset" }), []);

  return {
    status: state.status,
    result: state.result,
    error: state.error,
    runReview,
    reset,
  };
}