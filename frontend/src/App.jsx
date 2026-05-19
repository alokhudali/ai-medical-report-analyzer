import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a medical report");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(
        "https://backend.cutegirlsdmme.xyz/analyze",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data.analysis);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze report");
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk) => {
    switch (risk?.toLowerCase()) {
      case "high":
        return "#ff4d4f";
      case "medium":
        return "#faad14";
      default:
        return "#52c41a";
    }
  };

  const tableHeader = {
    border: "1px solid #ddd",
    padding: "10px",
    background: "#1677ff",
    color: "white",
    textAlign: "left",
  };

  const tableCell = {
    border: "1px solid #ddd",
    padding: "10px",
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#f4f6f9",
        padding: "40px",
        fontFamily: "Arial",
      }}
    >
      <div
        style={{
          maxWidth: "1100px",
          margin: "auto",
          background: "white",
          padding: "30px",
          borderRadius: "12px",
          boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
        }}
      >
        <h1 style={{ textAlign: "center", marginBottom: "30px" }}>
          AI-Powered Medical Report Analyzer
        </h1>

        <div
          style={{
            display: "flex",
            gap: "10px",
            marginBottom: "30px",
          }}
        >
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFile(e.target.files[0])}
            style={{ flex: 1 }}
          />

          <button
            onClick={handleUpload}
            style={{
              padding: "10px 20px",
              background: "#1677ff",
              color: "white",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
            }}
          >
            Analyze Report
          </button>
        </div>

        {loading && (
          <div
            style={{
              textAlign: "center",
              fontSize: "18px",
              marginBottom: "20px",
            }}
          >
            Analyzing report...
          </div>
        )}

        {error && (
          <div
            style={{
              color: "red",
              marginBottom: "20px",
            }}
          >
            {error}
          </div>
        )}

        {result && (
          <div>
            <div
              style={{
                background: getRiskColor(result.risk_level),
                color: "white",
                padding: "15px",
                borderRadius: "8px",
                marginBottom: "20px",
              }}
            >
              <h2>Risk Level: {result.risk_level}</h2>
              <p>
                <strong>Patient:</strong> {result.patient_name}
              </p>
            </div>

            <div
              style={{
                background: "#fafafa",
                padding: "20px",
                borderRadius: "8px",
                marginBottom: "20px",
              }}
            >
              <h2>Summary</h2>
              <p>{result.summary}</p>
            </div>

            <div
              style={{
                background: "#fafafa",
                padding: "20px",
                borderRadius: "8px",
                marginBottom: "20px",
                overflowX: "auto",
              }}
            >
              <h2>Abnormalities</h2>

              <table
                style={{
                  width: "100%",
                  borderCollapse: "collapse",
                }}
              >
                <thead>
                  <tr>
                    <th style={tableHeader}>Test</th>
                    <th style={tableHeader}>Value</th>
                    <th style={tableHeader}>Reference</th>
                    <th style={tableHeader}>Finding</th>
                  </tr>
                </thead>

                <tbody>
                  {result.abnormalities?.map((item, index) => (
                    <tr key={index}>
                      <td style={tableCell}>{item.test}</td>
                      <td style={tableCell}>{item.value}</td>
                      <td style={tableCell}>{item.reference_range}</td>
                      <td style={tableCell}>{item.finding}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div
              style={{
                background: "#fafafa",
                padding: "20px",
                borderRadius: "8px",
              }}
            >
              <h2>Precautions</h2>

              <ul>
                {result.precautions?.map((item, index) => (
                  <li key={index} style={{ marginBottom: "10px" }}>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
