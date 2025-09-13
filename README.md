# Digitalisat2Graph

## Thema der Masterarbeit
*Von Digitalisaten zu Wissensgraphen: Eine automatisierte Extraktion und semantische Modellierung biographischer Daten am Beispiel von Lebensbeschreibungen der Herrnhuter Brüdergemeine*

## Kurzbeschreibung
Dieses Repository enthält den Python-Code zum Projekt **Digitalisat2Graph**, das im Rahmen der oben genannten Masterarbeit entstanden ist. Untersucht wird die automatisierte Überführung biographischer Texte der Herrnhuter Brüdergemeine in **strukturierte Wissensgraph-Repräsentationen**. Als Arbeitsmaterial dient ein Korpus aus **20 Primärdigitalisaten** (Lebensbeschreibungen).

Methodisch wird eine Pipeline realisiert:
1. **Texterkennung (OCR)**, 
2. **Erkennung benannter Entitäten** mittels **spaCy-NER** (um ein domänenspezifisch erweitertes Modell ergänzt, trainiert auf **synthetisch erzeugten Trainingsdaten**),
3. **Relationsextraktion** mit **Llama 3** sowie 
4. **Entity Linking** gegen **Wikidata** integriert. 

Das resultierende Knoten-Kanten-Modell ermöglicht die semantische Analyse, Verknüpfung und Nachnutzung der biographischen Informationen.

## Aufbau
**Datenablage (`data/`)**  
Der Ordner `data/` enthält die für die Pipeline relevanten Materialien (z. B. Primärdigitalisate der Lebensbeschreibungen, OCR-Ausgaben und ggf. kuratierte Zwischenergebnisse). Für Nachvollziehbarkeit und Reproduzierbarkeit empfiehlt sich folgende Unterstruktur (Richtlinie):

- `data/raw/` – Primärdigitalisate (z. B. PDF/IMG) bzw. unveränderte Quelltexte.  
- `data/ocr/` – OCR-Ergebnisse (Plaintext, ggf. mit Seiten-/Zeilenmetadaten).  
- `data/processed/` – bereinigte/normalisierte Texte (Satzsegmentierung, Orthographievarianten).  
- `data/annotations/` – NER/RE-Annotationen, synthetische Trainingsdaten (JSONL/CSV).  
- `data/linked/` – Entity-Linking-Ergebnisse (Wikidata-IDs, Mappings).  

**Arbeitsweise**  
- **Notebook-getriebene Experimente:** `script.ipynb` dokumentiert exemplarisch die Ausführung einzelner Pipeline-Schritte (OCR → NER → RE → EL) sowie explorative Analysen.  




