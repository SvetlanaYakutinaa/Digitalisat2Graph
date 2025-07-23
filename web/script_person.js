function escapeHTML(str) {
  return str ? str.replace(/[&<>"']/g, match => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  })[match]) : '';
}

function getColor(type) {
  switch (type) {
    case "person": return "#652d2b";
    case "organisation": return "#eee8d2";
    case "location": return "#497f7f";
    default: return "#b85c38";
  }
}

let allNodes, allEdges, rawData;
let nodesView, edgesView;
let relationFilterValue = "";
let nodeTypeFilterValue = "";

fetch("../personen_.json")
  .then(response => response.json())
  .then(data => {
    rawData = data;
    const nodesMap = new Map();
    const edgeData = [];

    rawData.forEach(entry => {
      const subjId = entry.q_subjekt || `subj:${entry.subjekt}`;
      const objId = (entry.q_objekt && typeof entry.q_objekt === "string" && entry.q_objekt.startsWith("Q"))
        ? entry.q_objekt
        : (entry.objekt ? `obj:${entry.objekt}` : null);

      const subjLabel = entry.subjekt;
      const objLabel = entry.objekt;
      const prädikat = entry.prädikat;
      const zeit = entry.zeit;

      if (!nodesMap.has(subjId)) {
        nodesMap.set(subjId, {
          id: subjId,
          label: subjLabel,
          title: subjLabel,
          type: entry.subjekt_type || "",
          link: entry.subjekt_ref || null,
          color: getColor(entry.subjekt_type)
        });
      }

      const isSimpleDateRelation = zeit && (!objLabel || objLabel === "" || objLabel === null)
        && ["Geburtsdatum", "Sterbedatum"].includes(prädikat);

      if (isSimpleDateRelation) {
        const dateNodeId = `datum:${subjId}:${prädikat}:${zeit}`;
        nodesMap.set(dateNodeId, {
          id: dateNodeId,
          label: zeit,
          shape: "box",
          type: "date",
          color: "#fdd835"
        });

        edgeData.push({
          from: subjId,
          to: dateNodeId,
          label: prädikat,
          arrows: "to",
          relation: prädikat,
          color: { color: "#607d8b" }
        });
        return;
      }

      if (objId && !nodesMap.has(objId)) {
        nodesMap.set(objId, {
          id: objId,
          label: objLabel,
          title: objLabel,
          type: entry.objekt_type || "",
          link: entry.objekt_ref || null,
          color: getColor(entry.objekt_type)
        });
      }

      if (objId && prädikat) {
        edgeData.push({
          from: subjId,
          to: objId,
          label: prädikat,
          arrows: "to",
          relation: prädikat,
          color: { color: "#2c3e50" }
        });
      }
    });

    allNodes = new vis.DataSet(Array.from(nodesMap.values()));
    allEdges = new vis.DataSet(edgeData);

    nodesView = new vis.DataView(allNodes, { filter: nodeFilter });
    edgesView = new vis.DataView(allEdges, { filter: edgeFilter });

    const container = document.getElementById("mynetwork");
    const network = new vis.Network(container, {
      nodes: nodesView,
      edges: edgesView
    }, {
      edges: { smooth: true, font: { align: "middle" } },
      nodes: { shape: "dot", size: 20 },
      physics: { stabilization: true }
    });

    document.getElementById("relationFilter").addEventListener("change", e => {
      relationFilterValue = e.target.value;
      edgesView.refresh();
    });

    document.getElementById("nodeTypeFilter").addEventListener("change", e => {
      nodeTypeFilterValue = e.target.value;
      nodesView.refresh();
    });

    const detailsPanel = document.getElementById("detailsPanel");
    const card = document.getElementById("card");

    network.on("click", function (params) {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const node = allNodes.get(nodeId);

        const related = rawData.filter(entry =>
          (entry.q_subjekt || `subj:${entry.subjekt}`) === nodeId ||
          (typeof entry.q_objekt === "string" && entry.q_objekt === nodeId) ||
          (`obj:${entry.objekt}` === nodeId)
        );

        if (related.length === 0) {
          detailsPanel.classList.remove("visible");
          return;
        }

        let description = "";
        related.forEach(entry => {
          description += `
            <div class="detail-block">
              <strong>Quelle:</strong>
              ${entry.ref ? `<a href="${entry.ref}" target="_blank">${escapeHTML(entry.nbg || "Quelle")}</a>` : escapeHTML(entry.nbg || "Quelle")}
              <br><br>
              ${escapeHTML(entry.text)}<br><br>
              <strong>Personen- und Ortsnamen:</strong><br>
              ${entry.subjekt_ref ? `<a href="${entry.subjekt_ref}" target="_blank">${escapeHTML(entry.subjekt)}</a><br>` : `${escapeHTML(entry.subjekt)}<br>`}
              ${entry.objekt ? (entry.objekt_ref ? `<a href="${entry.objekt_ref}" target="_blank">${escapeHTML(entry.objekt)}</a><br>` : `${escapeHTML(entry.objekt)}<br>`) : ""}
            </div><hr>
          `;
        });

        document.getElementById("name").textContent = node.label;
        document.getElementById("description").innerHTML = description;
        card.style.display = "block";
        detailsPanel.classList.add("visible");
      } else {
        detailsPanel.classList.remove("visible");
        card.style.display = "none";
      }
    });
  })
  .catch(error => {
    console.error("Fehler beim Laden der JSON-Datei:", error);
    document.getElementById("mynetwork").innerHTML = "Fehler beim Laden der Daten.";
  });

function edgeFilter(edge) {
  return relationFilterValue === "" || edge.relation === relationFilterValue;
}

function nodeFilter(node) {
  return nodeTypeFilterValue === "" || node.type === nodeTypeFilterValue;
}
