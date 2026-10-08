import { sampleCase } from "../data/sampleCase";

export function analyzeCase(text) {
  if (!text || !text.trim()) {
    return {
      ...sampleCase,
      insights: []
    };
  }

  const lower = text.toLowerCase();

  const entities = sampleCase.entities.filter((entity) =>
    lower.includes(entity.name.toLowerCase())
  );

  const entityIds = new Set(entities.map((entity) => entity.id));

  const relationships = sampleCase.relationships.filter(
    ({ source, target }) => entityIds.has(source) && entityIds.has(target)
  );

  const connectionCounts = Object.fromEntries(
    entities.map((entity) => [entity.id, 0])
  );

  relationships.forEach(({ source, target }) => {
    connectionCounts[source] += 1;
    connectionCounts[target] += 1;
  });

  const rankedPeople = entities
    .filter((entity) => entity.type === "PERSON")
    .sort((a, b) => connectionCounts[b.id] - connectionCounts[a.id]);

  const keyEntity = rankedPeople[0];

  const insights = keyEntity
    ? [
        {
          entityId: keyEntity.id,
          title: "Potentially Significant Node",
          message: `${keyEntity.name} has the highest number of observed connections in this case.`,
          role: "Highly connected",
          connections: connectionCounts[keyEntity.id]
        }
      ]
    : [];

  return {
    entities,
    relationships,
    insights
  };
}