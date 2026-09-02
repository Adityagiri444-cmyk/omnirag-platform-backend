import { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import { authFetch } from "./api";

function Analytics() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await authFetch("http://localhost:8000/documents/stats");
        if (!response.ok) throw new Error("Failed to load stats");
        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError(err.message);
      }
    };
    fetchStats();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!stats) return <p>Loading analytics...</p>;

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h3>Analytics</h3>
      <p>Total Documents: {stats.total_documents}</p>

      {stats.upload_history.length > 0 && (
        <>
          <h4>Uploads (Last 7 Days)</h4>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={stats.upload_history}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#61dafb" />
            </BarChart>
          </ResponsiveContainer>
        </>
      )}

      {stats.documents_per_user.length > 0 && (
        <>
          <h4>Documents Per User</h4>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={stats.documents_per_user}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="user" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </>
      )}
    </div>
  );
}

export default Analytics;