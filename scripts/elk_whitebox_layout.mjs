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
const VIEWPORT_POLICY_NAME = "viewport-readable";
const VIEWPORT_TARGET_ASPECT_RATIO = 1.15;
const VIEWPORT_PREFERRED_MAX_ASPECT_RATIO = 1.45;
const VIEWPORT_HARD_MAX_ASPECT_RATIO = 2.2;

const LAYOUT_CANDIDATES = [
  {
    name: "right-default",
    direction: "RIGHT",
    fallbackPenalty: 0,
    rootOptions: {},
    componentOptions: {},
  },
  {
    name: "right-balanced",
    direction: "RIGHT",
    fallbackPenalty: 8,
    rootOptions: {
      "elk.aspectRatio": String(VIEWPORT_TARGET_ASPECT_RATIO),
      "elk.spacing.nodeNode": "64",
      "elk.layered.spacing.nodeNodeBetweenLayers": "76",
      "elk.layered.spacing.edgeNodeBetweenLayers": "32",
    },
    componentOptions: {
      "elk.spacing.nodeNode": "48",
      "elk.layered.spacing.nodeNodeBetweenLayers": "70",
    },
  },
  {
    name: "right-wrapped",
    direction: "RIGHT",
    wrapping: "SINGLE_EDGE",
    fallbackPenalty: 58,
    rootOptions: {
      "elk.aspectRatio": String(VIEWPORT_TARGET_ASPECT_RATIO),
      "elk.spacing.nodeNode": "64",
      "elk.layered.spacing.nodeNodeBetweenLayers": "72",
      "elk.layered.spacing.edgeNodeBetweenLayers": "30",
      "elk.layered.wrapping.strategy": "SINGLE_EDGE",
    },
    componentOptions: {
      "elk.spacing.nodeNode": "46",
      "elk.layered.spacing.nodeNodeBetweenLayers": "68",
    },
  },
  {
    name: "down-balanced",
    direction: "DOWN",
    fallbackPenalty: 180,
    rootOptions: {
      "elk.aspectRatio": "1.0",
      "elk.spacing.nodeNode": "64",
      "elk.layered.spacing.nodeNodeBetweenLayers": "78",
      "elk.layered.spacing.edgeNodeBetweenLayers": "32",
    },
    componentOptions: {
      "elk.spacing.nodeNode": "48",
      "elk.layered.spacing.nodeNodeBetweenLayers": "70",
    },
  },
];

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

function buildGraph(model, candidate = LAYOUT_CANDIDATES[0]) {
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
      ...candidate.componentOptions,
    },
  };

  return {
    id: "whitebox-root",
    layoutOptions: {
      "elk.algorithm": "layered",
      "elk.direction": candidate.direction,
      "elk.hierarchyHandling": "INCLUDE_CHILDREN",
      "elk.edgeRouting": "ORTHOGONAL",
      "elk.padding": `[top=${ROOT_PADDING},left=${ROOT_PADDING},bottom=${ROOT_PADDING},right=${ROOT_PADDING}]`,
      "elk.spacing.nodeNode": "80",
      "elk.layered.spacing.nodeNodeBetweenLayers": "100",
      "elk.layered.spacing.edgeNodeBetweenLayers": "40",
      "elk.layered.considerModelOrder.strategy": "NODES_AND_EDGES",
      "elk.layered.crossingMinimization.strategy": "LAYER_SWEEP",
      "elk.layered.nodePlacement.strategy": "NETWORK_SIMPLEX",
      ...candidate.rootOptions,
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

function inferPortSide(portBox, ownerBox) {
  const portRight = portBox.x + portBox.width;
  const portBottom = portBox.y + portBox.height;
  const ownerRight = ownerBox.x + ownerBox.width;
  const ownerBottom = ownerBox.y + ownerBox.height;
  const verticalOverlap = portBox.y < ownerBottom && portBottom > ownerBox.y;
  const horizontalOverlap = portBox.x < ownerRight && portRight > ownerBox.x;
  if (portRight <= ownerBox.x && verticalOverlap) {
    return "left";
  }
  if (portBox.x >= ownerRight && verticalOverlap) {
    return "right";
  }
  if (portBottom <= ownerBox.y && horizontalOverlap) {
    return "top";
  }
  if (portBox.y >= ownerBottom && horizontalOverlap) {
    return "bottom";
  }
  const centerX = portBox.x + portBox.width / 2;
  const centerY = portBox.y + portBox.height / 2;
  const distances = {
    left: Math.abs(centerX - ownerBox.x),
    right: Math.abs(centerX - ownerRight),
    top: Math.abs(centerY - ownerBox.y),
    bottom: Math.abs(centerY - ownerBottom),
  };
  return Object.entries(distances).sort((left, right) => left[1] - right[1])[0][0];
}

function straddleOwnerBoundary(portBox, ownerBox) {
  const side = inferPortSide(portBox, ownerBox);
  if (side === "left") {
    return { ...portBox, x: ownerBox.x - Math.floor(portBox.width / 2) };
  }
  if (side === "right") {
    return { ...portBox, x: ownerBox.x + ownerBox.width - Math.floor(portBox.width / 2) };
  }
  if (side === "top") {
    return { ...portBox, y: ownerBox.y - Math.floor(portBox.height / 2) };
  }
  return { ...portBox, y: ownerBox.y + ownerBox.height - Math.floor(portBox.height / 2) };
}

function boxesOverlap(left, right) {
  return (
    left.x < right.x + right.width &&
    left.x + left.width > right.x &&
    left.y < right.y + right.height &&
    left.y + left.height > right.y
  );
}

function pushPeerBox(groups, parent, box) {
  if (!groups.has(parent)) {
    groups.set(parent, []);
  }
  groups.get(parent).push(box);
}

function renderedPeerGroups(layout) {
  const groups = new Map();
  pushPeerBox(groups, "root", { key: "component", ...layout.component });
  for (const [externalId, externalBox] of Object.entries(layout.externals ?? {})) {
    pushPeerBox(groups, "root", { key: `external:${externalId}`, ...externalBox });
  }
  for (const [portId, portBox] of Object.entries(layout.componentPorts ?? {})) {
    pushPeerBox(groups, "component", {
      key: `component-port:${portId}`,
      ...straddleOwnerBoundary(portBox, layout.component),
    });
  }
  for (const [partId, partBox] of Object.entries(layout.parts ?? {})) {
    pushPeerBox(groups, "component", { key: `part:${partId}`, ...partBox });
    for (const [portId, portBox] of Object.entries(layout.partPorts?.[partId] ?? {})) {
      pushPeerBox(groups, `part:${partId}`, {
        key: `part-port:${partId}.${portId}`,
        ...straddleOwnerBoundary(portBox, partBox),
      });
    }
  }
  return groups;
}

function layoutQualityFailures(layout) {
  const failures = [];
  for (const [parent, boxes] of renderedPeerGroups(layout)) {
    for (let index = 0; index < boxes.length; index += 1) {
      const left = boxes[index];
      if (left.width <= 0 || left.height <= 0) {
        failures.push(`${left.key} has nonpositive geometry`);
        continue;
      }
      for (const right of boxes.slice(index + 1)) {
        if (right.width <= 0 || right.height <= 0) {
          continue;
        }
        if (boxesOverlap(left, right)) {
          failures.push(`${left.key} overlaps ${right.key} under ${parent}`);
        }
      }
    }
  }
  return failures;
}

function emitLayout(model, graph, candidate, candidateSelection) {
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

  const canvas = {
    width: Math.ceil((graph.width ?? 0) + ROOT_PADDING),
    height: Math.ceil((graph.height ?? 0) + ROOT_PADDING),
  };
  return {
    backend: "elk",
    canvas,
    layoutPolicy: {
      policy: VIEWPORT_POLICY_NAME,
      selectedCandidate: candidate.name,
      direction: candidate.direction,
      wrapping: candidate.wrapping ?? "OFF",
      aspectRatio: roundMetric(canvas.width / Math.max(1, canvas.height), 3),
      score: roundMetric(candidateSelection.score, 2),
      candidateCount: candidateSelection.candidateCount,
      rejectedCandidateCount: candidateSelection.rejectedCandidateCount,
    },
    component: componentNode,
    componentPorts,
    parts: partNodes,
    partPorts,
    externals: externalNodes,
    edges,
  };
}

function roundMetric(value, digits) {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function layoutEdgeMetrics(layout) {
  let bendCount = 0;
  let routeLength = 0;
  for (const points of Object.values(layout.edges ?? {})) {
    if (!Array.isArray(points) || points.length < 2) {
      continue;
    }
    bendCount += Math.max(0, points.length - 2);
    for (let index = 1; index < points.length; index += 1) {
      const [leftX, leftY] = points[index - 1];
      const [rightX, rightY] = points[index];
      routeLength += Math.abs(rightX - leftX) + Math.abs(rightY - leftY);
    }
  }
  return { bendCount, routeLength };
}

function viewportReadabilityScore(candidate, layout) {
  const width = layout.canvas.width;
  const height = layout.canvas.height;
  const aspectRatio = width / Math.max(1, height);
  const shapePenalty = Math.abs(Math.log(aspectRatio / VIEWPORT_TARGET_ASPECT_RATIO)) * 120;
  const widePenalty = Math.max(0, aspectRatio - VIEWPORT_PREFERRED_MAX_ASPECT_RATIO) * 260;
  const hardWidePenalty = Math.max(0, aspectRatio - VIEWPORT_HARD_MAX_ASPECT_RATIO) * 900;
  const tallPenalty = Math.max(0, 0.72 - aspectRatio) * 70;
  const viewportWidthPenalty = width / 34;
  const areaPenalty = Math.sqrt(width * height) / 38;
  const { bendCount, routeLength } = layoutEdgeMetrics(layout);
  const routePenalty = bendCount * 4 + routeLength / 260;
  return (
    candidate.fallbackPenalty +
    shapePenalty +
    widePenalty +
    hardWidePenalty +
    tallPenalty +
    viewportWidthPenalty +
    areaPenalty +
    routePenalty
  );
}

async function layoutCandidate(elk, model, candidate) {
  const graph = buildGraph(model, candidate);
  const layout = await elk.layout(graph);
  const emitted = emitLayout(model, layout, candidate, {
    score: 0,
    candidateCount: LAYOUT_CANDIDATES.length,
    rejectedCandidateCount: 0,
  });
  const score = viewportReadabilityScore(candidate, emitted);
  const qualityFailures = layoutQualityFailures(emitted);
  if (qualityFailures.length > 0) {
    throw new Error(`layout quality check failed: ${qualityFailures.slice(0, 4).join("; ")}`);
  }
  return { candidate, graph: layout, layout: emitted, score };
}

async function selectViewportReadableLayout(elk, model) {
  const accepted = [];
  const rejected = [];
  for (const candidate of LAYOUT_CANDIDATES) {
    try {
      accepted.push(await layoutCandidate(elk, model, candidate));
    } catch (error) {
      rejected.push({ candidate: candidate.name, reason: error.message || String(error) });
    }
  }
  if (accepted.length === 0) {
    throw new Error(`all viewport-readable layout candidates failed: ${JSON.stringify(rejected)}`);
  }
  accepted.sort((left, right) => {
    const scoreDelta = left.score - right.score;
    if (Math.abs(scoreDelta) > 0.0001) {
      return scoreDelta;
    }
    return left.candidate.name.localeCompare(right.candidate.name);
  });
  const selected = accepted[0];
  return emitLayout(model, selected.graph, selected.candidate, {
    score: selected.score,
    candidateCount: LAYOUT_CANDIDATES.length,
    rejectedCandidateCount: rejected.length,
  });
}

async function main() {
  const input = await readStdin();
  const model = JSON.parse(input);
  const elk = new ELK();
  const layout = await selectViewportReadableLayout(elk, model);
  process.stdout.write(`${JSON.stringify(layout)}\n`);
}

main().catch((error) => {
  process.stderr.write(`ELK Whitebox layout failed: ${error.stack || error.message || error}\n`);
  process.exit(1);
});
