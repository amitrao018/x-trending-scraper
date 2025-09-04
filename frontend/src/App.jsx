import { useState } from "react";
import axios from "axios";
import { FaFire, FaGlobe, FaExclamationCircle } from "react-icons/fa";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import "./styles.css";

function App() {
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchTrends = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await axios.post(process.env.REACT_APP_API_URL);// POST to trigger scraper
      setTrends(res.data);
    } catch (err) {
      setError("Failed to fetch trends. Please try again.");
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>
        <FaFire style={{ verticalAlign: "middle", marginRight: "8px" }} />
        X Trending Topics
      </h1>

      <button onClick={fetchTrends} disabled={loading}>
        {loading ? (
          <span className="loading">
            <AiOutlineLoading3Quarters
              className="spin"
              size={18}
              style={{ marginRight: "6px" }}
            />
            Fetching Trends...
          </span>
        ) : (
          "Fetch Latest Trends"
        )}
      </button>

      {error && (
        <div className="error">
          <FaExclamationCircle style={{ marginRight: "6px" }} />
          {error}
        </div>
      )}

      {trends && (
        <div className="trends">
          <p>
            <strong>Run Time:</strong> {trends.run_time}
          </p>
          <p>
            <FaGlobe size={14} style={{ marginRight: "4px" }} />
            <strong>IP Address:</strong> {trends.ip_address}
          </p>
          <ol>
            {["trend1", "trend2", "trend3", "trend4", "trend5"].map(
              (key, index) =>
                trends[key] && (
                  <li key={key} className="trend-card">
                    <span className="trend-rank">#{index + 1}</span>{" "}
                    {trends[key]}
                  </li>
                )
            )}
          </ol>
        </div>
      )}
    </div>
  );
}

export default App;
