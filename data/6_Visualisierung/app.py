# app.py
import pandas as pd
import streamlit as st
import networkx as nx
from pyvis.network import Network

st.set_page_config(page_title="SPO-Netzwerk (einfach)", layout="wide")
st.title("🔎 Einfache interaktive SPO-Graph-Visualisierung")

uploaded = st.file_uploader("Datei hochladen (.xlsx oder .csv)", type=["xlsx", "csv"])

def load_df(file):
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file, sheet_name=0)

if uploaded:
    df = load_df(uploaded)

    # Minimalprüfung
    needed = {"subjekt", "p_wert", "objekt"}
    if not needed.issubset(df.columns.str.lower()):
        st.error("Erwartete Spalten: subjekt, p_wert, objekt")
        st.stop()

    # Spalten robust referenzieren (unabhängig von Groß/Kleinschreibung)
    cols = {c.lower(): c for c in df.columns}
    s_col, p_col, o_col = cols["subjekt"], cols["p_wert"], cols["objekt"]

    st.subheader("Datenvorschau")
    st.dataframe(df[[s_col, p_col, o_col]].head(20))

    # (Optionale) sehr einfache Filter
    preds = sorted(df[p_col].dropna().astype(str).unique())
    sel_preds = st.multiselect("Prädikate filtern (leer = alle):", preds, default=[])

    df_view = df if not sel_preds else df[df[p_col].astype(str).isin(sel_preds)]

    # NetworkX-Graph bauen
    G = nx.DiGraph()
    for _, row in df_view.iterrows():
        s, p, o = row[s_col], row[p_col], row[o_col]
        if pd.isna(s) or pd.isna(o):
            continue
        G.add_node(s, label=str(s))
        G.add_node(o, label=str(o))
        G.add_edge(s, o, label=str(p))

    # PyVis-Netz erstellen (einfach, ohne Tuning)
    net = Network(height="750px", width="100%", directed=True, cdn_resources="in_line")
    net.barnes_hut()  # Physik für schöne Verteilung

    # Nodes & Edges übertragen
    for n, data in G.nodes(data=True):
        net.add_node(str(n), label=data.get("label", str(n)))
    for u, v, edata in G.edges(data=True):
        net.add_edge(str(u), str(v), label=edata.get("label", ""))

    # HTML generieren und anzeigen
    html = net.generate_html()
    st.subheader("Interaktive Ansicht")
    st.components.v1.html(html, height=780, scrolling=True)

    # Optionaler Export
    st.download_button("📥 HTML exportieren", data=html, file_name="netzwerk_minimal.html", mime="text/html")

else:
    st.info("Bitte lade eine CSV/XLSX mit den Spalten: subjekt, p_wert, objekt hoch.")
