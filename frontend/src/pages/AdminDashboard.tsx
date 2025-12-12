import { useEvaluation } from "../context/EvaluationContext";

export default function AdminDashboard() {
  const { scores, total, classification } = useEvaluation();

  return (
    <section className="bg-gray-900 p-6 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold mb-4">Dashboard Supervisor (demo)</h2>
      <div className="text-sm text-gray-200 space-y-2">
        <p>Total calculado: {total ?? "-"}</p>
        <p>Clasificación: {classification ?? "-"}</p>
        <p>Scores: {Object.keys(scores).length ? JSON.stringify(scores) : "sin datos"}</p>
      </div>
    </section>
  );
}
