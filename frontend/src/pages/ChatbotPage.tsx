import { FormEvent, useMemo, useState } from "react";
import api from "../services/api";
import { useEvaluation } from "../context/EvaluationContext";
import { RUBRIC_ITEMS } from "../data/rubric";

interface EvalResponse {
  id: number;
  evaluator_id: number;
  evaluatee_id: number;
  total_score: string;
  classification?: string;
  status: string;
  scores: Record<string, number>;
}

export default function ChatbotPage() {
  const { setScores } = useEvaluation();
  const [evaluateeId, setEvaluateeId] = useState(101);
  const [scores, setLocalScores] = useState<Record<string, number>>(() =>
    Object.fromEntries(RUBRIC_ITEMS.map((item) => [item.key, 3]))
  );
  const [message, setMessage] = useState<string | null>(null);

  const grouped = useMemo(
    () => ({
      technical: RUBRIC_ITEMS.filter((i) => i.type === "technical"),
      attitude: RUBRIC_ITEMS.filter((i) => i.type === "attitude")
    }),
    []
  );

  const handleScore = (key: string, value: number) => {
    setLocalScores((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMessage(null);
    try {
      const res = await api.post<EvalResponse>("/evaluations", { evaluatee_id: Number(evaluateeId), scores });
      setScores(res.data.scores, res.data.total_score, res.data.classification ?? null);
      setMessage(`Total ${res.data.total_score}${res.data.classification ? ` (${res.data.classification})` : ""}`);
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      setMessage(detail || "Error al crear evaluación");
    }
  };

  return (
    <section className="bg-gray-900 p-6 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold mb-4">Evaluación Conversacional (25 ítems)</h2>
      <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
        <input
          className="p-2 rounded bg-gray-800 border border-gray-700"
          value={evaluateeId}
          onChange={(e) => setEvaluateeId(Number(e.target.value))}
          placeholder="ID evaluado"
        />

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <h3 className="font-semibold text-sm mb-2 text-gray-200">Técnicas (CT)</h3>
            <div className="flex flex-col gap-2">
              {grouped.technical.map((item) => (
                <label key={item.key} className="text-sm text-gray-200 flex items-center gap-2">
                  <span className="w-20 font-mono">{item.key}</span>
                  <span className="flex-1">{item.name}</span>
                  <input
                    type="number"
                    min={1}
                    max={5}
                    value={scores[item.key]}
                    onChange={(e) => handleScore(item.key, Number(e.target.value))}
                    className="w-16 p-1 rounded bg-gray-800 border border-gray-700 text-center"
                  />
                </label>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-sm mb-2 text-gray-200">Actitudinales (CA)</h3>
            <div className="flex flex-col gap-2">
              {grouped.attitude.map((item) => (
                <label key={item.key} className="text-sm text-gray-200 flex items-center gap-2">
                  <span className="w-20 font-mono">{item.key}</span>
                  <span className="flex-1">{item.name}</span>
                  <input
                    type="number"
                    min={1}
                    max={5}
                    value={scores[item.key]}
                    onChange={(e) => handleScore(item.key, Number(e.target.value))}
                    className="w-16 p-1 rounded bg-gray-800 border border-gray-700 text-center"
                  />
                </label>
              ))}
            </div>
          </div>
        </div>

        <button className="bg-emerald-500 hover:bg-emerald-600 text-white font-semibold py-2 rounded" type="submit">
          Guardar
        </button>
      </form>
      {message && <p className="mt-3 text-sm text-gray-200">{message}</p>}
    </section>
  );
}
