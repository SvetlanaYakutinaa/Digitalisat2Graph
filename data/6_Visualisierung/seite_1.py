import streamlit as st

st.set_page_config(layout="wide", page_title="Über das Projekt")

# Typografie + Layout
st.markdown("""
<style>
/* Zentrale Contentbreite und Luft */
main .block-container{
  max-width: 980px;      /* angenehme Zeilenlänge */
  padding-top: 2rem;
  padding-bottom: 3rem;
}

/* Grundschrift & Lesbarkeit */
html, body, [class*="css"]  {
  font-size: 22px !important;   /* Standard-Text */ 
  line-height: 1.6;
}

/* Überschriften */
h1 { font-size: 34px !important; font-weight: 700 !important; line-height: 1.2; margin-bottom: .5rem; }
h2 { font-size: 28px !important; font-weight: 600 !important; line-height: 1.25; margin-top: 1.5rem; }
h3 { font-size: 26px !important; font-weight: 600 !important; line-height: 1.3;  margin-top: 1rem; }

/* Deutsche Silbentrennung */
.hyphenate { hyphens: auto; -webkit-hyphens: auto; -ms-hyphens: auto; }

/* Minimal größere Absatzschrift */
p { font-size: 1.05rem; }
</style>
""", unsafe_allow_html=True)

# 3) HERO: mittige Spalte mit H1 (kein zusätzliches st.title mehr)
_, center, _ = st.columns([1, 4, 1])
with center:
    st.markdown(
        """
        <div class="hyphenate" lang="de">
          <h1>Von Digitalisaten zu Wissensgraphen: Eine automatisierte Extraktion
          und semantische Modellierung biographischer Daten am Beispiel von
          Lebensbeschreibungen der Herrnhuter Brüdergemeine</h1>
          
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# 4) Abschnitt darunter: sinnvolle Spalten (2:1)
left, right = st.columns([2, 1], gap="large")

with left:
    st.subheader("Über das Projekt")
    st.markdown(
        """
        In dieser Anwendung kannst du Texte, Bilder und Diagramme einfügen.
        Für reine Texte ist eine einzelne Spalte meist am schönsten.
        Spalten eignen sich eher für **Inhalt + Begleitinfo**.
        """
    )

with right:
    st.info("💡 Tipp: Nutze Spalten für Karten, KPIs, kleine Bilder oder Hinweise – nicht für Fließtext.")
    st.markdown("**Nächste Schritte**")
    st.markdown("- Daten laden\n- Vorschau prüfen\n- Graph erzeugen")
