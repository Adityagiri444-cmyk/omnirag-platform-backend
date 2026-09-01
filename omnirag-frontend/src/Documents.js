import { useState, useEffect } from "react";

function Documents() {
  const [documents, setDocuments] = useState([]);
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

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

  // Filter documents by filename, case-insensitive
  const filteredDocuments = documents.filter((doc) =>
    doc.filename.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">My Documents</h3>

      <form onSubmit={handleUpload} className="flex items-center gap-3 mb-4">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="text-sm text-gray-600 file:mr-3 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-blue-50 file:text-blue-600 file:font-medium hover:file:bg-blue-100"
        />
        <button
          type="submit"
          disabled={uploading || !file}
          className="px-4 py-2 bg-blue-500 text-white rounded-md font-medium hover:bg-blue-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {uploading ? "Uploading..." : "Upload PDF"}
        </button>
      </form>

      <input
        type="text"
        placeholder="Search documents by name..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
      />

      {error && <p className="text-red-500 text-sm mb-3">{error}</p>}

      <ul className="divide-y divide-gray-200">
        {filteredDocuments.map((doc) => (
          <li key={doc.id} className="flex items-center justify-between py-3">
            <span className="text-gray-700">{doc.filename}</span>
            <button
              onClick={() => handleDelete(doc.id)}
              className="px-3 py-1 text-sm bg-red-50 text-red-600 rounded-md hover:bg-red-100 transition-colors"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>

      {documents.length === 0 && (
        <p className="text-gray-400 text-sm text-center py-4">No documents uploaded yet.</p>
      )}
      {documents.length > 0 && filteredDocuments.length === 0 && (
        <p className="text-gray-400 text-sm text-center py-4">No documents match your search.</p>
      )}
    </div>
  );
}

export default Documents;