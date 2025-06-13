// Farbzuweisung basierend auf dem Typ
const typeColors = {
  "person": "#652d2b",
  "location": "#231f20",
  "organisation": "#cabea8",
  "date": "#a69f8d",
  "tätigkeit": "orange"
};

// Funktion zur Erstellung der Knoten und Kanten
function createNetworkData(jsonData) {
  let nodes = new vis.DataSet([]);
  let edges = new vis.DataSet([]);
  let details = {};
  let nodeMap = {}; // Ein Objekt, um bereits erstellte Knoten zu verfolgen

  jsonData.forEach((entry) => {
    entry.graph.forEach((relation) => {
      // Falls das Subjekt oder Objekt "nicht spezifiziert" ist, überspringen
      if (relation.subjekt === "nicht spezifiziert" || relation.objekt === "nicht spezifiziert") {
        return; // Knoten überspringen
      }

      // Subjekt-Knoten erstellen oder wiederverwenden
      let fromNode = nodeMap[relation.subjekt];
      if (!fromNode) {
        fromNode = nodes.length + 1;
        const color = typeColors[relation.subjekt_type] || "gray"; // Standardfarbe "gray", falls der Typ unbekannt ist
        nodes.add({ id: fromNode, label: relation.subjekt, color: color });
        nodeMap[relation.subjekt] = fromNode;
      }

      // Objekt-Knoten erstellen oder wiederverwenden
      let toNode = nodeMap[relation.objekt];
      if (!toNode) {
        toNode = nodes.length + 1;
        const color = typeColors[relation.objekt_type] || "gray"; // Standardfarbe "gray", falls der Typ unbekannt ist
        nodes.add({ id: toNode, label: relation.objekt, color: color });
        nodeMap[relation.objekt] = toNode;
      }

      // Kante basierend auf dem Prädikat
      edges.add({
        from: fromNode,
        to: toNode,
        label: relation.prädikat // Das Prädikat als Kantenlabel
      });

      // Details speichern (Autor und Text)
      details[fromNode] = {
        name: relation.subjekt,
        description: entry.text,
        image: "https://via.placeholder.com/300x200?text=" + encodeURIComponent(relation.subjekt)
      };

      details[toNode] = {
        name: relation.objekt,
        description: entry.text,
        image: "https://via.placeholder.com/300x200?text=" + encodeURIComponent(relation.objekt)
      };
    });
  });

  return { nodes, edges, details };
}

// JSON-Datei laden
fetch('test.json') // Den richtigen Pfad zu deiner JSON-Datei hier angeben
  .then(response => response.json())
  .then(jsonData => {
    const { nodes, edges, details } = createNetworkData(jsonData);

    // Vis.js Netzwerk erstellen
    const container = document.getElementById("network");
    const data = { nodes, edges };
    const options = {
      nodes: {
        shape: 'dot',
        size: 16,
        font: { size: 14 }
      },
      edges: {
        smooth: true,
        color: '#555'
      },
      physics: {
        stabilization: true
      }
    };
    const network = new vis.Network(container, data, options);

    const detailsPanel = document.getElementById("details");
    const card = document.getElementById("card");

    // Knoten auswählen
    network.on("selectNode", function (params) {
      const id = params.nodes[0];

      const info = details[id];
      document.getElementById("name").innerText = info.name;
      document.getElementById("description").innerText = info.description;
      document.getElementById("photo").src = info.image;

      detailsPanel.classList.add("visible");
      card.style.display = "block";
    });

    // Knoten abwählen
    network.on("deselectNode", function () {
      detailsPanel.classList.remove("visible");
      card.style.display = "none";
    });

    // Interaktive Legende: Klicken auf Legendenitems zeigt nur die entsprechenden Knoten
    document.getElementById("personLegend").addEventListener("click", function() {
      filterPersonRelations(nodes, edges);
    });

  })
  .catch(error => {
    console.error('Fehler beim Laden der JSON-Datei:', error);
  });

// Funktion zur Filterung von Beziehungen zwischen Personen
function filterPersonRelations(nodes, edges) {
  // Zeige nur Knoten vom Typ "Person"
  nodes.forEach(node => {
    if (node.color.color === typeColors["person"]) {
      nodes.update({ id: node.id, hidden: false }); // Zeige alle "Personen"-Knoten
    } else {
      nodes.update({ id: node.id, hidden: true }); // Verstecke alle nicht-Personen-Knoten
    }
  });

}
