import { useState } from "react";
import { sampleCaseText } from "../data/sampleCase";

export default function CaseInput({ onAnalyze, loading = false }) {
  const [text, setText] = useState(sampleCaseText);

  const handleSubmit = (event) => {
    event.preventDefault();
    onAnalyze(text);
  };

  return (
    <form className="case-input" onSubmit={handleSubmit}>
      <div className="section-label">CASE EVIDENCE</div>

      <textarea
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Paste investigation evidence..."
        aria-label="Case evidence"
      />

      <div className="input-actions">
        <button type="submit" disabled={loading}>
          {loading ? "ANALYZING..." : "ANALYZE CASE"}
        </button>

        <button
          type="button"
          className="secondary-button"
          onClick={() => setText(sampleCaseText)}
        >
          LOAD SAMPLE
        </button>
      </div>
    </form>
  );
}