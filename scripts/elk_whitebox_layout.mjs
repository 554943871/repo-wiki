#!/usr/bin/env node
import ELK from "elkjs/lib/elk.bundled.js";

const SIMPLE_TEXT_WIDTH = 7;
const ROOT_PADDING = 80;
const PORT_WIDTH = 120;
const PORT_HEIGHT = 44;
const PART_PORT_WIDTH = 138;
const PART_PORT_HEIGHT = 34;
const EXTERNAL_WIDTH = 150;
const EXTERNAL_HEIGHT = 64;

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      data += chunk;
    });
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}

function textWidth(label, minimum, padding = 34) {
  return Math.max(minimum, String(label).length * SIMPLE_TEXT_WIDTH + padding);
}

function portInterfaceCount(port) {
  const provides = Array.isArray(port.provides) ? port.provides.length : 0;
  const requires = Array.isArray(port.requires) ? port.requires.length : 0;
  return provides + requires;
}

function nodeId(kind, id) {
  return `${kind}:${id}`;
}

function componentPortId(componentId, portId) {
  return `component-port:${componentId}:${portId}`;
}

function partPortId(partId, portId) {
  return `part-port:${partId}:${portId}`;
}

function endpointTargetId(endpoint, componentId) {
  if (typeof endpoint === "string") {
    if (!endpoint.includes(".")) {
      return nodeId("external", endpoint);
    }
    const [ownerId, portId] = endpoint.split(".", 2);
    if (ownerId === componentId) {
      return componentPortId(componentId, portId);
    }
    return partPortId(ownerId, portId);
  }
  if (String(endpoint.owner) === componentId) {
    return componentPortId(componentId, endpoint.port);
  }
  return partPortId(endpoint.owner, endpoint.port);
}

function buildPort(ownerId, port, minimumWidth, height, padding = 34) {
  const roleCount = portInterfaceCount(port);
  return {
    id: ownerId.includes(":")
      ? partPortId(ownerId.split(":")[1], port.id)
      : componentPortId(ownerId, port.id),
    width: textWidth(port.label, minimumWidth, padding),
    height,
    labels: [{ text: String(port.label) }],
    layoutOptions: {
      "elk.portConstraints": "FREE",
    },
    properties: {
      roleCount,
    },
  };
}

function sortedById(items) {
  return [...items].sort((left, right) => String(left.id).localeCompare(String(right.id)));
}

function buildGraph(model) {
  const component = model.component;
  const componentId = String(component.id);
  const componentPorts = sortedById(Array.isArray(component.ports) ? component.ports : []);
  const parts = sortedById(Array.isArray(model.parts) ? model.parts : []);
  const externals = sortedById(Array.isArray(model.externals) ? model.externals : []);
  const connectors = sortedById(Array.isArray(model.connectors) ? model.connectors : []);
  const componentPortSlotHeight = PORT_HEIGHT + 28;
  const componentMinimumHeight = Math.max(220, 120 + componentPorts.length * componentPortSlotHeight);

  const componentNode = {
    id: nodeId("component", componentId),
    labels: [{ text: String(component.label) }],
    width: Math.max(360, textWidth(component.label, 0, 80)),
    height: componentMinimumHeight,
    ports: componentPorts.map((port) => buildPort(componentId, port, PORT_WIDTH, PORT_HEIGHT)),
    children: parts.map((part) => {
      const ports = sortedById(Array.isArray(part.ports) ? part.ports : []);
      const maxRoleCount = Math.max(1, ...ports.map(portInterfaceCount));
      return {
        id: nodeId("part", part.id),
        labels: [{ text: String(part.label) }],
        width: Math.max(190, textWidth(part.label, 0, 56)),
        height: Math.max(118, 72 + ports.length * Math.max(44, 34 + (maxRoleCount - 1) * 26)),
        ports: ports.map((port) => buildPort(`part:${part.id}`, port, PART_PORT_WIDTH, PART_PORT_HEIGHT)),
        layoutOptions: {
          "elk.portConstraints": "FREE",
        },
      };
    }),
    layoutOptions: {
      "elk.padding": "[top=64,left=120,bottom=80,right=140]",
      "elk.portConstraints": "FREE",
      "elk.layered.spacing.nodeNodeBetweenLayers": "90",
      "elk.spacing.nodeNode": "60",
    },
  };

  return {
    id: "whitebox-root",
    layoutOptions: {
      "elk.algorithm": "layered",
      "elk.direction": "RIGHT",
      "elk.hierarchyHandling": "INCLUDE_CHILDREN",
      "elk.edgeRouting": "ORTHOGONAL",
      "elk.padding": `[top=${ROOT_PADDING},left=${ROOT_PADDING},bottom=${ROOT_PADDING},right=${ROOT_PADDING}]`,
      "elk.spacing.nodeNode": "80",
      "elk.layered.spacing.nodeNodeBetweenLayers": "100",
      "elk.layered.spacing.edgeNodeBetweenLayers": "40",
      "elk.layered.considerModelOrder.strategy": "NODES_AND_EDGES",
      "elk.layered.crossingMinimization.strategy": "LAYER_SWEEP",
      "elk.layered.nodePlacement.strategy": "NETWORK_SIMPLEX",
    },
    children: [
      ...externals.map((external) => ({
        id: nodeId("external", external.id),
        labels: [{ text: String(external.label) }],
        width: textWidth(external.label, EXTERNAL_WIDTH),
        height: EXTERNAL_HEIGHT,
      })),
      componentNode,
    ],
    edges: connectors.map((connector) => ({
      id: `connector:${connector.id}`,
      sources: [endpointTargetId(connector.from, componentId)],
      targets: [endpointTargetId(connector.to, componentId)],
    })),
  };
}

function absoluteChildren(node, offsetX = 0, offsetY = 0, nodes = new Map(), ports = new Map()) {
  const x = offsetX + (node.x ?? 0);
  const y = offsetY + (node.y ?? 0);
  nodes.set(node.id, { x, y, width: node.width ?? 0, height: node.height ?? 0 });
  for (const port of node.ports ?? []) {
    ports.set(port.id, {
      x: x + (port.x ?? 0),
      y: y + (port.y ?? 0),
      width: port.width ?? 0,
      height: port.height ?? 0,
    });
  }
  for (const child of node.children ?? []) {
    absoluteChildren(child, x, y, nodes, ports);
  }
  return { nodes, ports };
}

function edgePoints(edge, offsetX = 0, offsetY = 0) {
  const section = edge.sections?.[0];
  if (!section) {
    return [];
  }
  const points = [];
  if (section.startPoint) {
    points.push(section.startPoint);
  }
  for (const bend of section.bendPoints ?? []) {
    points.push(bend);
  }
  if (section.endPoint) {
    points.push(section.endPoint);
  }
  return points.map((point) => [Math.round(point.x + offsetX), Math.round(point.y + offsetY)]);
}

function endpointIsInsideComponent(endpoint) {
  return typeof endpoint !== "string" || endpoint.includes(".");
}

function emitLayout(model, graph) {
  const component = model.component;
  const componentId = String(component.id);
  const { nodes, ports } = absoluteChildren(graph);
  const componentNode = nodes.get(nodeId("component", componentId));
  if (!componentNode) {
    throw new Error(`ELK layout did not return component node ${componentId}`);
  }

  const componentPorts = {};
  for (const port of sortedById(Array.isArray(component.ports) ? component.ports : [])) {
    const portId = componentPortId(componentId, port.id);
    if (!ports.has(portId)) {
      throw new Error(`ELK layout did not return component port ${componentId}.${port.id}`);
    }
    componentPorts[String(port.id)] = ports.get(portId);
  }

  const partNodes = {};
  const partPorts = {};
  for (const part of sortedById(Array.isArray(model.parts) ? model.parts : [])) {
    const partId = String(part.id);
    const partNode = nodes.get(nodeId("part", partId));
    if (!partNode) {
      throw new Error(`ELK layout did not return part node ${partId}`);
    }
    partNodes[partId] = partNode;
    partPorts[partId] = {};
    for (const port of sortedById(Array.isArray(part.ports) ? part.ports : [])) {
      const portId = partPortId(partId, port.id);
      if (!ports.has(portId)) {
        throw new Error(`ELK layout did not return part port ${partId}.${port.id}`);
      }
      partPorts[partId][String(port.id)] = ports.get(portId);
    }
  }

  const externalNodes = {};
  for (const external of sortedById(Array.isArray(model.externals) ? model.externals : [])) {
    const externalId = String(external.id);
    const externalNode = nodes.get(nodeId("external", externalId));
    if (!externalNode) {
      throw new Error(`ELK layout did not return external node ${externalId}`);
    }
    externalNodes[externalId] = externalNode;
  }

  const connectorsById = new Map(
    (Array.isArray(model.connectors) ? model.connectors : []).map((connector) => [
      `connector:${connector.id}`,
      connector,
    ])
  );
  const edges = {};
  for (const edge of graph.edges ?? []) {
    if (!edge.id?.startsWith("connector:")) {
      continue;
    }
    const connector = connectorsById.get(edge.id);
    const relativeToComponent =
      connector && endpointIsInsideComponent(connector.from) && endpointIsInsideComponent(connector.to);
    edges[edge.id.slice("connector:".length)] = edgePoints(
      edge,
      relativeToComponent ? componentNode.x : 0,
      relativeToComponent ? componentNode.y : 0
    );
  }

  return {
    backend: "elk",
    canvas: {
      width: Math.ceil((graph.width ?? 0) + ROOT_PADDING),
      height: Math.ceil((graph.height ?? 0) + ROOT_PADDING),
    },
    component: componentNode,
    componentPorts,
    parts: partNodes,
    partPorts,
    externals: externalNodes,
    edges,
  };
}

async function main() {
  const input = await readStdin();
  const model = JSON.parse(input);
  const elk = new ELK();
  const graph = buildGraph(model);
  const layout = await elk.layout(graph);
  process.stdout.write(`${JSON.stringify(emitLayout(model, layout))}\n`);
}

main().catch((error) => {
  process.stderr.write(`ELK Whitebox layout failed: ${error.stack || error.message || error}\n`);
  process.exit(1);
});
