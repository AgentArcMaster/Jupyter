export default function EntityPanel({ entity, connectionCount = 0 }) {
  if (!entity) {
    return (
      <aside className="entity-panel empty-panel">
        <div className="section-label">ENTITY INTELLIGENCE</div>
        <p>Select a node in the network to inspect it.</p>
      </aside>
    );
  }

  const isPotentiallySignificant =
    entity.type === "PERSON" && connectionCount >= 2;

  return (
    <aside className="entity-panel">
      <div className="section-label">ENTITY INTELLIGENCE</div>

      <div className="entity-heading">
        <div>
          <h2>{entity.name}</h2>
          <span className="entity-type">{entity.type}</span>
        </div>
      </div>

      <div className="entity-metrics">
        <div>
          <span>Connections</span>
          <strong>{connectionCount}</strong>
        </div>

        <div>
          <span>Network Role</span>
          <strong>
            {isPotentiallySignificant ? "Bridge / Hub" : "Observed Entity"}
          </strong>
        </div>
      </div>

      <div className="insight-box">
        <span>INSIGHT</span>
        <p>
          {isPotentiallySignificant
            ? "This entity has multiple observed relationships and may warrant investigator review."
            : "This entity appears in the current evidence set."}
        </p>
      </div>

      {isPotentiallySignificant && (
        <div className="review-warning">
          ⚠ Requires investigator review
        </div>
      )}
    </aside>
  );
}