import CaseInput from "./CaseInput";
import EntityPanel from "./EntityPanel";
import NetworkGraph from "./NetworkGraph";

function getConnectionCount(entityId, relationships) {
  return relationships.filter(
    ({ source, target }) => source === entityId || target === entityId
  ).length;
}

export default function Dashboard({
  entities,
  relationships,
  insights,
  selectedEntity,
  onAnalyze,
  onNodeClick,
  loading
}) {
  const selectedConnectionCount = selectedEntity
    ? getConnectionCount(selectedEntity.id, relationships)
    : 0;

  const people = entities.filter((entity) => entity.type === "PERSON");

  return (
    <main className="dashboard">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">N</div>

          <div>
            <h1>NEXUS</h1>
            <p>INTELLIGENCE ANALYSIS PLATFORM</p>
          </div>
        </div>

        <div className="case-id">
          <span>ACTIVE CASE</span>
          <strong>#CN-001</strong>
        </div>
      </header>

      <section className="workspace">
        <section className="evidence-column">
          <CaseInput onAnalyze={onAnalyze} loading={loading} />

          <EntityPanel
            entity={selectedEntity}
            connectionCount={selectedConnectionCount}
          />
        </section>

        <section className="graph-column">
          <div className="panel-heading">
            <div>
              <span className="section-label">RELATIONSHIP NETWORK</span>
              <h2>Case Network</h2>
            </div>

            <div className="live-indicator">
              <span />
              ANALYSIS READY
            </div>
          </div>

          <NetworkGraph
            entities={entities}
            relationships={relationships}
            onNodeClick={onNodeClick}
          />
        </section>
      </section>

      <section className="stats-grid">
        <div className="stat-card">
          <span>ENTITIES</span>
          <strong>{entities.length}</strong>
        </div>

        <div className="stat-card">
          <span>CONNECTIONS</span>
          <strong>{relationships.length}</strong>
        </div>

        <div className="stat-card">
          <span>PEOPLE</span>
          <strong>{people.length}</strong>
        </div>

        <div className="stat-card">
          <span>KEY NODES</span>
          <strong>{insights.length}</strong>
        </div>
      </section>

      <section className="insights-section">
        <div className="section-label">POTENTIALLY SIGNIFICANT CONNECTIONS</div>

        {insights.length === 0 ? (
          <div className="empty-insight">
            No potentially significant patterns identified.
          </div>
        ) : (
          <div className="insight-list">
            {insights.map((insight) => {
              const entity = entities.find(
                (item) => item.id === insight.entityId
              );

              return (
                <button
                  key={insight.entityId}
                  className="insight-row"
                  onClick={() => entity && onNodeClick(entity)}
                >
                  <div>
                    <strong>{entity?.name ?? "Unknown entity"}</strong>
                    <span>{insight.role}</span>
                  </div>

                  <div className="insight-connections">
                    {insight.connections} connections
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </section>
    </main>
  );
}