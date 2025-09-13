# Digitalisat2Graph

## Thema der Masterarbeit
*Von Digitalisaten zu Wissensgraphen: Eine automatisierte Extraktion und semantische Modellierung biographischer Daten am Beispiel von Lebensbeschreibungen der Herrnhuter Brüdergemeine*

## Kurzbeschreibung
Dieses Repository enthält den Python-Code zum Projekt **Digitalisat2Graph**, das im Rahmen der oben genannten Masterarbeit entstanden ist. Untersucht wird die automatisierte Überführung biographischer Texte der Herrnhuter Brüdergemeine in **strukturierte Wissensgraph-Repräsentationen**. Als Arbeitsmaterial dient ein Korpus aus **20 Lebensbeschreibungen (Primärdigitalisate)**.

Methodisch wird eine Pipeline realisiert:
1. **Texterkennung (OCR)**
2. **Erkennung benannter Entitäten (NER)** mit spaCy; das Modell wurde domänenspezifisch erweitert und auf synthetisch erzeugten Trainingsdaten nachtrainiert
3. **Relationsextraktion (RE)** mit Llama 3
4. **Entity Linking (EL)** mit Wikidata

Das resultierende Knoten-Kanten-Modell ermöglicht die semantische Analyse, Verknüpfung und Nachnutzung der biographischen Informationen.

## Aufbau

**Datenablage** 
Der Ordner `data/` enthält die für die Pipeline relevanten Materialien (z. B. Primärdigitalisate, OCR-Ausgaben sowie kuratierte Zwischenergebnisse). Für Nachvollziehbarkeit und Reproduzierbarkeit gilt folgende Unterstruktur:

- [5.2_OCR-Erkennung/jpg](data/5.2_OCR-Erkennung/jpg) – Primärdigitalisate als Seitenbilder (JPG).
- [5.2_OCR-Erkennung/txt](data/5.2_OCR-Erkennung/txt) – OCR-Ergebnisse (Plaintext, ggf. mit Seiten-/Zeilenmetadaten).
- [5.3_TEI-Modellierung](data/5.3_TEI-Modellierung) – TEI-XML (roh und bereinigt); bereinigte Dateien unter  
  [5.3_TEI_bereinigt](data/5.3_TEI-Modellierung/5.3_TEI_bereinigt/).
- [5.4.1_NER](data/5.4.1_NER) – NER-Modell und Trainingsressourcen  
  - [Skript zur Erstellung der Trainingsdaten](data/5.4.1_NER/ML_Trainingdaten.ipynb)  
  - [Trainingsdaten (JSONL)](data/5.4.1_NER/training_data.jsonl)  
  - [Feinabgestimmtes spaCy-Modell](data/5.4.1_NER/output/model-best/)
- [5.4.2_RE](data/5.4.2_RE) – Ergebnisse der Relationsextraktion.
- [5.4.3_EL](data/5.4.3_EL) – Entity-Linking-Ergebnisse (Wikidata-IDs, Mappings).

**Hinweise zur Ablage**  
- **Codebasis:** Der ausführbare Projektcode befindet sich primär im Notebook [`script.ipynb`](script.ipynb).  
- **Trainingsressourcen (NER):**
  **Trainingsmodell** und **Trainingsdaten** liegen gebündelt unter [`data/5.4.1_NER`](data/5.4.1_NER) (siehe Links oben).  
- **Ergebnisdateien und Zwischenstände:** Die weiteren Unterordner in `data/` enthalten Dateien, die im Verlauf der Arbeit entstanden sind (z. B. OCR-Outputs, bereinigte TEI-XML, Ergebnisse der Relationsextraktion und des Entity Linkings).

**Arbeitsweise**  
- **Notebook-getriebene Experimente:** [`script.ipynb`](script.ipynb) dokumentiert exemplarisch die Ausführung einzelner Pipeline-Schritte (OCR → NER → RE → EL) sowie explorative Analysen.


## Datenquelle
Die verwendeten Digitalisate der Zeitschrift *Nachrichten aus der Brüder-Gemeine* sind frei zugänglich über die **Digital Archives Initiative (DAI)** der [Memorial University of Newfoundland](https://dai.mun.ca/digital/nachrichten)  
Für die einzelnen Jahrgänge/Ausgaben stehen direkte PDF-Downloads bereit.
