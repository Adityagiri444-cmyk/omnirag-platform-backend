import { useState } from "react";

function Query() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem("access_token");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setError("");
    setAnswer(null);
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/query/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Query failed");
      }

      const data = await response.json();
      setAnswer(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
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
          disabled={loading || !question.trim()}
          className="px-4 py-2 bg-blue-500 text-white rounded-md font-medium hover:bg-blue-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>

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