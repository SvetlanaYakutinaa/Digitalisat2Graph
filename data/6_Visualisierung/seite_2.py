
import streamlit as st
st.set_page_config(layout="wide", page_title="Visualisierung")

import pandas as pd
import networkx as nx
from pyvis.network import Network
import os


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

st.set_page_config(layout="wide", page_title="Visualisierung")


st.markdown(
        """
        <div class="hyphenate" lang="de">
          <h1>Visualisierung</h1>
          
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()



# Pfad RELATIV zur aktuellen Skriptdatei ermitteln
BASE = os.path.dirname(os.path.abspath(__file__)) 
XLSX = os.path.normpath(os.path.join(BASE, "..", "5.4.3_EL", "graphen_bereinigt.xlsx"))


if not os.path.exists(XLSX):
    st.error("Datei nicht gefunden.")
    # Zeig, was im erwarteten Ordner liegt (prüfe Ordner- und Dateinamen!)
    ziel_ordner = os.path.join(BASE, "..", "5.4.3_EL")
    try:
        st.write("Inhalt von:", os.path.abspath(ziel_ordner))
        st.code("\n".join(sorted(os.listdir(ziel_ordner))))
    except Exception as e:
        st.write(f"Konnte Ordner nicht lesen: {e}")
    st.stop()

# Laden (erstes Sheet)
df = pd.read_excel(XLSX)  

# Spalten prüfen (case-insensitive)
needed = {"subjekt", "p_wert", "objekt"}
cols_map = {c.lower(): c for c in df.columns}
if not needed.issubset(cols_map):
    st.stop()

s_col, p_col, o_col = cols_map["subjekt"], cols_map["p_wert"], cols_map["objekt"]


# NetworkX-Graph bauen 
G = nx.DiGraph()
for _, row in df[[s_col, p_col, o_col]].dropna(subset=[s_col, o_col]).iterrows():
    s, p, o = str(row[s_col]), str(row[p_col]), str(row[o_col])
    G.add_node(s, label=s)
    G.add_node(o, label=o)
    G.add_edge(s, o, label=p)

# PyVis-Netz erzeugen
net = Network(height="750px", width="100%", directed=True, cdn_resources="in_line")
net.barnes_hut()

# Nodes zuerst
for n, data in G.nodes(data=True):
    net.add_node(str(n), label=str(data.get("label", n)))

# Dann Edges
for u, v, edata in G.edges(data=True):
    net.add_edge(str(u), str(v), label=str(edata.get("label", "")))

# HTML erzeugen und einbetten
html = net.generate_html()
st.components.v1.html(html, height=780, scrolling=True)



