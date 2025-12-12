import { createContext, useContext, useState, ReactNode } from "react";

interface ScoreMap {
  [key: string]: number;
}

interface EvaluationState {
  scores: ScoreMap;
  total: string | null;
  classification: string | null;
}

interface EvaluationContextType extends EvaluationState {
  setScores: (scores: ScoreMap, total?: string | null, classification?: string | null) => void;
}

const EvaluationContext = createContext<EvaluationContextType | undefined>(undefined);

export function EvaluationProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<EvaluationState>({ scores: {}, total: null, classification: null });

  const setScores = (scores: ScoreMap, total: string | null = null, classification: string | null = null) =>
    setState({ scores, total, classification });

  return <EvaluationContext.Provider value={{ ...state, setScores }}>{children}</EvaluationContext.Provider>;
}

export function useEvaluation() {
  const ctx = useContext(EvaluationContext);
  if (!ctx) throw new Error("useEvaluation must be used within EvaluationProvider");
  return ctx;
}
