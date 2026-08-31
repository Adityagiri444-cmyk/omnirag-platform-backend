import { useState, useEffect } from "react";

function Documents() {
  const [documents, setDocuments] = useState([]);
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);

  const token = localStorage.getItem("access_token");

  const fetchDocuments = async () => {
    try {
      const response = await fetch("http://localhost:8000/documents/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      setDocuments(data);
    } catch (err) {
      setError("Failed to load documents");
    }
  };

  useEffect(() => {
    fetchDocuments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setError("");
    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/documents/upload", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Upload failed");
      }

      setFile(null);
      fetchDocuments(); // refresh the list
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/documents/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Delete failed");
      }

      fetchDocuments(); // refresh the list
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ maxWidth: "500px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h3>My Documents</h3>

      <form onSubmit={handleUpload} style={{ marginBottom: "20px" }}>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit" disabled={uploading || !file} style={{ marginLeft: "10px" }}>
          {uploading ? "Uploading..." : "Upload PDF"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {documents.map((doc) => (
          <li
            key={doc.id}
            style={{
              display: "flex",
              justifyContent: "space-between",
              padding: "8px",
              borderBottom: "1px solid #444",
            }}
          >
            <span>{doc.filename}</span>
            <button onClick={() => handleDelete(doc.id)} style={{ cursor: "pointer" }}>
              Delete
            </button>
          </li>
        ))}
      </ul>

      {documents.length === 0 && <p>No documents uploaded yet.</p>}
    </div>
  );
}

export default Documents;