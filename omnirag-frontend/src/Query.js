import { useState, useRef } from "react";
import { authFetch } from "./api";

const STEPS = ["planner", "retrieval", "summarizer", "evaluator"];
const STEP_LABELS = {
  planner: "Planner",
  retrieval: "Retrieval",
  summarizer: "Summarizer",
  evaluator: "Evaluator",
};

function Query() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [error, setError] = useState("");
  const [running, setRunning] = useState(false);
  const [completedSteps, setCompletedSteps] = useState([]);
  const [currentStep, setCurrentStep] = useState(null);
  const pollRef = useRef(null);

  const pollStatus = (taskId) => {
    pollRef.current = setInterval(async () => {
      try {
        const response = await authFetch(`http://localhost:8000/query/status/${taskId}`);
        const data = await response.json();

        setCompletedSteps(data.completed_steps || []);
        setCurrentStep(data.current_step);

        if (data.done) {
          clearInterval(pollRef.current);
          setRunning(false);
          if (data.error) {
            setError(data.error);
          } else {
            setAnswer(data);
          }
        }
      } catch (err) {
        clearInterval(pollRef.current);
        setRunning(false);
        setError("Failed to check status");
      }
    }, 2000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setError("");
    setAnswer(null);
    setCompletedSteps([]);
    setCurrentStep(null);
    setRunning(true);

    try {
      const response = await authFetch("http://localhost:8000/query/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to start query");
      }

      const data = await response.json();
      pollStatus(data.task_id);
    } catch (err) {
      setError(err.message);
      setRunning(false);
    }
  };

  const getStepStatus = (step) => {
    if (completedSteps.includes(step)) return "done";
    if (currentStep === step) return "active";
    return "pending";
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Ask OmniRAG</h3>

      <form onSubmit={handleSubmit} className="flex items-center gap-3 mb-4">
        <input
          type="text"
          placeholder="Ask a question about your documents..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          type="submit"
          disabled={running || !question.trim()}
          className="px-4 py-2 bg-blue-500 text-white rounded-md font-medium hover:bg-blue-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {running ? "Thinking..." : "Ask"}
        </button>
      </form>

      {running && (
        <div className="flex items-center justify-between mb-4 px-2">
          {STEPS.map((step, i) => {
            const status = getStepStatus(step);
            return (
              <div key={step} className="flex items-center flex-1">
                <div
                  className={`flex flex-col items-center flex-1 ${
                    status === "active" ? "scale-110" : ""
                  } transition-transform`}
                >
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold border-2 ${
                      status === "done"
                        ? "bg-green-500 border-green-500 text-white"
                        : status === "active"
                        ? "bg-blue-500 border-blue-500 text-white animate-pulse"
                        : "bg-gray-100 border-gray-300 text-gray-400"
                    }`}
                  >
                    {status === "done" ? "✓" : i + 1}
                  </div>
                  <span
                    className={`text-xs mt-1 ${
                      status === "active" ? "font-bold text-blue-600" : "text-gray-500"
                    }`}
                  >
                    {STEP_LABELS[step]}
                  </span>
                </div>
                {i < STEPS.length - 1 && (
                  <div
                    className={`h-0.5 flex-1 -mt-4 ${
                      completedSteps.includes(step) ? "bg-green-400" : "bg-gray-200"
                    }`}
                  />
                )}
              </div>
            );
          })}
        </div>
      )}

      {error && <p className="text-red-500 text-sm mb-3">{error}</p>}

      {answer && (
        <div className="border border-gray-200 rounded-md p-4 bg-gray-50">
          <p className="text-gray-800 mb-2">{answer.answer}</p>
          <p className="text-xs text-gray-400">
            Evaluation: {answer.evaluation} · Attempts: {answer.attempts}
          </p>
        </div>
      )}
    </div>
  );
}

export default Query;