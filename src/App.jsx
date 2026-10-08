import { useState } from "react";
import Dashboard from "./components/Dashboard";
import { sampleCase } from "./data/sampleCase";
import { analyzeCase } from "./utils/analyzer";
import "./styles.css";

export default function App() {
  const [analysis, setAnalysis] = useState({
    ...sampleCase,
    insights: [
      {
        entityId: "p2",
        title: "Potentially Significant Node",
        message:
          "Arjun has the highest number of observed connections in this case.",
        role: "Highly connected",
        connections: 3
      }
    ]
  });

  const [selectedEntity, setSelectedEntity] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (text) => {
    setLoading(true);
    setSelectedEntity(null);

    // Small delay makes the prototype feel like an analysis pipeline.
    await new Promise((resolve) => setTimeout(resolve, 450));

    const result = analyzeCase(text);
    setAnalysis(result);
    setLoading(false);
  };

  return (
    <Dashboard
      entities={analysis.entities}
      relationships={analysis.relationships}
      insights={analysis.insights}
      selectedEntity={selectedEntity}
      onAnalyze={handleAnalyze}
      onNodeClick={setSelectedEntity}
      loading={loading}
    />
  );
}