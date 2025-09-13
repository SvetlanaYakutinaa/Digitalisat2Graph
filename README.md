# Digitalisat2Graph

# Digitalisat2Graph

## Thema der Masterarbeit
*Von Digitalisaten zu Wissensgraphen: Eine automatisierte Extraktion und semantische Modellierung biographischer Daten am Beispiel von Lebensbeschreibungen der Herrnhuter Brüdergemeine*

## Kurzbeschreibung
Dieses Repository enthält den Python-Code zum Projekt **Digitalisat2Graph**, das im Rahmen der oben genannten Masterarbeit entstanden ist. Untersucht wird die automatisierte Überführung biographischer Texte der Herrnhuter Brüdergemeine in **strukturierte Wissensgraph-Repräsentationen**. Als Arbeitsmaterial dient ein Korpus aus **20 Primärdigitalisaten** (Lebensbeschreibungen).

Methodisch wird eine Pipeline realisiert, die (1) **Texterkennung (OCR)**, (2) **Erkennung benannter Entitäten** mittels **spaCy-NER** (um ein domänenspezifisch erweitertes Modell ergänzt, trainiert auf **synthetisch erzeugten Trainingsdaten**), (3) **Relationsextraktion** mit **Llama 3** sowie (4) **Entity Linking** gegen **Wikidata** integriert. Das resultierende Knoten-Kanten-Modell ermöglicht die semantische Analyse, Verknüpfung und Nachnutzung der biographischen Informationen.


