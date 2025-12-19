import { FormEvent, useState, useMemo } from "react";
import api from "../services/api";
import { useEvaluation } from "../context/EvaluationContext";
import { RUBRIC_ITEMS, RubricItem } from "../data/rubric";

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
  const [currentIndex, setCurrentIndex] = useState(0);
  const [scores, setLocalScores] = useState<Record<string, number>>(() =>
    Object.fromEntries(RUBRIC_ITEMS.map((item) => [item.key, 3]))
  );
  const [message, setMessage] = useState<string | null>(null);
  const [chatMessages, setChatMessages] = useState<string[]>([
    "¡Hola! Voy a ayudarte a completar tu evaluación de desempeño. Iremos paso a paso por cada criterio."
  ]);

  const currentItem = RUBRIC_ITEMS[currentIndex];
  const totalItems = RUBRIC_ITEMS.length;
  const completedItems = currentIndex;
  const progressPercent = Math.round((completedItems / totalItems) * 100);

  // Determinar etapa actual
  const currentStage = useMemo(() => {
    if (currentItem.type === "technical") {
      const techIndex = RUBRIC_ITEMS.filter(i => i.type === "technical").findIndex(i => i.key === currentItem.key);
      return `Competencias Técnicas (${techIndex + 1}/11)`;
    } else {
      const attIndex = RUBRIC_ITEMS.filter(i => i.type === "attitude").findIndex(i => i.key === currentItem.key);
      return `Competencias Actitudinales (${attIndex + 1}/14)`;
    }
  }, [currentItem]);

  // Feedback educativo según el ítem y puntuación
  const generateFeedback = (item: RubricItem, score: number): string => {
    const feedbackMap: Record<string, Record<number, string>> = {
      "CT1": {
        1: "Necesitas mejorar en técnica aséptica. Recorda siempre lavarte las manos antes y después.",
        2: "Bien, pero podés mejorar. Repasá el protocolo de curaciones del hospital.",
        3: "Desempeño aceptable. Mantené la consistencia en la técnica.",
        4: "Muy bien! Tu técnica es sólida. Segui así.",
        5: "Excelente! Sos un referente en cuidado de heridas para el equipo."
      },
      "CT2": {
        1: "Importante: revisá siempre los 5 correctos antes de administrar medicación.",
        2: "Bien, pero hay espacio para mejorar. Practicá el cálculo de dosis.",
        3: "Buen nivel. Mantené la precisión.",
        4: "Muy seguro en la administración. ¡Felicitaciones!",
        5: "Ejemplar. Tu dominio en farmacología es destacado."
      },
      // Feedback genérico para otros ítems
      "default": {
        1: "Necesitás mejorar en este aspecto. Hablaremos de cómo desarrollarlo.",
        2: "Vas bien, pero hay oportunidades de mejora.",
        3: "Desempeño satisfactorio. Seguí así.",
        4: "Muy buen nivel. Seguí desarrollándote.",
        5: "¡Excelente! Sos un ejemplo para el equipo."
      }
    };

    const feedback = feedbackMap[item.key] || feedbackMap["default"];
    return feedback[score] || feedback[3];
  };

  const handleScoreChange = (value: number) => {
    setLocalScores((prev) => ({ ...prev, [currentItem.key]: value }));
    
    // Agregar feedback del chatbot
    const feedback = generateFeedback(currentItem, value);
    setChatMessages(prev => [...prev, `Tú: Puntaje ${value}/5`, `Asistente: ${feedback}`]);
  };

  const handleNext = () => {
    if (currentIndex < totalItems - 1) {
      setCurrentIndex(prev => prev + 1);
      setChatMessages(prev => [
        ...prev,
        `Asistente: Perfecto! Pasemos al siguiente criterio: "${RUBRIC_ITEMS[currentIndex + 1].name}"`
      ]);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
      setChatMessages(prev => [
        ...prev,
        `Asistente: Volvamos al criterio anterior: "${RUBRIC_ITEMS[currentIndex - 1].name}"`
      ]);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMessage(null);
    try {
      const res = await api.post<EvalResponse>("/evaluations", { 
        evaluatee_id: Number(evaluateeId), 
        scores 
      });
      setScores(res.data.scores, res.data.total_score, res.data.classification ?? null);
      setMessage(`✅ Evaluación guardada! Total: ${res.data.total_score}${res.data.classification ? ` (${res.data.classification})` : ""}`);
      setChatMessages(prev => [
        ...prev,
        `Asistente: ¡Evaluación completada y guardada exitosamente! 🎉`
      ]);
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      setMessage("❌ " + (detail || "Error al crear evaluación"));
    }
  };

  return (
    <div className="bg-gray-900 p-6 rounded-lg shadow-lg flex flex-col gap-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-semibold mb-2">📊 Evaluación de Desempeño</h2>
        <p className="text-sm text-gray-400">Sistema conversacional con rúbrica validada (25 criterios)</p>
      </div>

      {/* Barra de Progreso */}
      <div className="bg-gray-800 p-4 rounded-lg">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-semibold">📈 Progreso General</span>
          <span className="text-sm text-gray-400">{completedItems}/{totalItems} criterios</span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
          <div 
            className="bg-gradient-to-r from-emerald-500 to-emerald-400 h-3 rounded-full transition-all duration-500"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
        <p className="text-xs text-gray-400 mt-1 text-right">{progressPercent}% completado</p>
      </div>

      {/* Indicador de Etapa */}
      <div className="bg-gradient-to-r from-blue-900 to-blue-800 p-3 rounded-lg border border-blue-700">
        <p className="text-sm font-semibold">🎯 Etapa actual: {currentStage}</p>
      </div>

      {/* Contenido Principal: 2 Columnas */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Columna 1: Formulario del Criterio Actual */}
        <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <div className="mb-4">
            <span className="inline-block bg-gray-700 px-3 py-1 rounded text-sm font-mono mb-2">
              {currentItem.key}
            </span>
            <h3 className="text-xl font-semibold">{currentItem.name}</h3>
            <p className="text-xs text-gray-400 mt-1">
              {currentItem.type === "technical" ? "Competencia Técnica" : "Competencia Actitudinal"}
            </p>
          </div>

          <div className="flex flex-col gap-4">
            <label className="text-sm text-gray-300">Calificación (1-5):</label>
            <div className="flex gap-2">
              {[1, 2, 3, 4, 5].map((val) => (
                <button
                  key={val}
                  type="button"
                  onClick={() => handleScoreChange(val)}
                  className={`flex-1 py-3 rounded font-semibold transition-all ${
                    scores[currentItem.key] === val
                      ? "bg-emerald-500 text-white shadow-lg scale-105"
                      : "bg-gray-700 text-gray-300 hover:bg-gray-600"
                  }`}
                >
                  {val}
                </button>
              ))}
            </div>
            <div className="text-xs text-gray-400 flex justify-between">
              <span>1 = Insuficiente</span>
              <span>5 = Excelente</span>
            </div>
          </div>

          {/* Navegación */}
          <div className="flex gap-3 mt-6">
            <button
              type="button"
              onClick={handlePrevious}
              disabled={currentIndex === 0}
              className="flex-1 py-2 rounded bg-gray-700 hover:bg-gray-600 disabled:opacity-30 disabled:cursor-not-allowed"
            >
              ← Anterior
            </button>
            <button
              type="button"
              onClick={handleNext}
              disabled={currentIndex === totalItems - 1}
              className="flex-1 py-2 rounded bg-blue-600 hover:bg-blue-500 disabled:opacity-30 disabled:cursor-not-allowed"
            >
              Siguiente →
            </button>
          </div>
        </div>

        {/* Columna 2: Chatbot Asistente */}
        <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 flex flex-col">
          <h3 className="text-lg font-semibold mb-4">🤖 Asistente Educativo</h3>
          
          <div className="flex-1 bg-gray-900 rounded-lg p-4 overflow-y-auto max-h-96 space-y-3">
            {chatMessages.map((msg, idx) => {
              const isBot = msg.startsWith("Asistente:");
              return (
                <div key={idx} className={`flex ${isBot ? "justify-start" : "justify-end"}`}>
                  <div className={`max-w-[80%] p-3 rounded-lg ${
                    isBot 
                      ? "bg-blue-900 text-blue-100" 
                      : "bg-emerald-900 text-emerald-100"
                  }`}>
                    <p className="text-sm">{msg.replace("Asistente: ", "").replace("Tú: ", "")}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Formulario Final */}
      <form onSubmit={handleSubmit} className="bg-gray-800 p-4 rounded-lg border border-gray-700">
        <div className="flex gap-4 items-end">
          <div className="flex-1">
            <label className="text-sm text-gray-300 block mb-2">ID del Evaluado:</label>
            <input
              type="number"
              className="w-full p-2 rounded bg-gray-900 border border-gray-700"
              value={evaluateeId}
              onChange={(e) => setEvaluateeId(Number(e.target.value))}
              placeholder="ID evaluado"
            />
          </div>
          <button 
            type="submit"
            className="px-6 py-2 bg-emerald-500 hover:bg-emerald-600 text-white font-semibold rounded transition-colors"
          >
            💾 Guardar Evaluación Completa
          </button>
        </div>
        {message && (
          <p className={`mt-3 text-sm ${
            message.startsWith("✅") ? "text-emerald-400" : "text-red-400"
          }`}>
            {message}
          </p>
        )}
      </form>
    </div>
  );
}
