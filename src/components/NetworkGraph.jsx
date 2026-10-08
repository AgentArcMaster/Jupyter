import { useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

const NODE_WIDTH = 150;
const NODE_HEIGHT = 54;

function getNodeColor(type) {
  switch (type) {
    case "PERSON":
      return "#7c3aed";
    case "LOCATION":
      return "#0891b2";
    case "VEHICLE":
      return "#d97706";
    case "FINANCIAL":
      return "#059669";
    default:
      return "#475569";
  }
}

export default function NetworkGraph({
  entities = [],
  relationships = [],
  onNodeClick
}) {
  const { nodes, edges } = useMemo(() => {
    const people = entities.filter((item) => item.type === "PERSON");
    const others = entities.filter((item) => item.type !== "PERSON");

    const generatedNodes = [
      ...people.map((entity, index) => ({
        id: entity.id,
        position: {
          x: 120 + (index % 2) * 260,
          y: 100 + Math.floor(index / 2) * 130
        },
        data: {
          label: (
            <div className="graph-node">
              <strong>{entity.name}</strong>
              <span>{entity.type}</span>
            </div>
          )
        },
        style: {
          width: NODE_WIDTH,
          minHeight: NODE_HEIGHT,
          border: `1px solid ${getNodeColor(entity.type)}`,
          borderRadius: 10,
          background: "#111827",
          color: "#f8fafc",
          padding: 8
        }
      })),

      ...others.map((entity, index) => ({
        id: entity.id,
        position: {
          x: 40 + index * 190,
          y: 390
        },
        data: {
          label: (
            <div className="graph-node">
              <strong>{entity.name}</strong>
              <span>{entity.type}</span>
            </div>
          )
        },
        style: {
          width: NODE_WIDTH,
          minHeight: NODE_HEIGHT,
          border: `1px solid ${getNodeColor(entity.type)}`,
          borderRadius: 10,
          background: "#0f172a",
          color: "#f8fafc",
          padding: 8
        }
      }))
    ];

    const generatedEdges = relationships.map((relationship, index) => ({
      id: `edge-${index}`,
      source: relationship.source,
      target: relationship.target,
      label: relationship.type.replaceAll("_", " "),
      type: "smoothstep",
      animated: false,
      style: {
        stroke: "#64748b",
        strokeWidth: 1.5
      },
      labelStyle: {
        fill: "#94a3b8",
        fontSize: 9
      },
      labelBgStyle: {
        fill: "#0f172a"
      }
    }));

    return {
      nodes: generatedNodes,
      edges: generatedEdges
    };
  }, [entities, relationships]);

  return (
    <div className="network-graph">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        minZoom={0.4}
        maxZoom={1.8}
        onNodeClick={(_, node) => {
          const entity = entities.find((item) => item.id === node.id);
          if (entity) onNodeClick(entity);
        }}
      >
        <Background gap={24} size={1} />
        <Controls />
        <MiniMap
          pannable
          zoomable
          nodeColor={(node) =>
            getNodeColor(
              entities.find((item) => item.id === node.id)?.type
            )
          }
        />
      </ReactFlow>
    </div>
  );
}