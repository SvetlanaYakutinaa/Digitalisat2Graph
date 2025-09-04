import streamlit as st
st.set_page_config(layout="wide", page_title="Visualisierung")

import pandas as pd
import networkx as nx
from pyvis.network import Network
from collections import defaultdict
import os

# ---------- Styles ----------
st.markdown("""
<style>
.appview-container .main .block-container{
  max-width: 100%;
  padding: 2rem 1rem 3rem 1rem;
}
html, body, [class*="css"]  { font-size: 22px !important; line-height: 1.6; }
h1 { font-size: 34px !important; font-weight: 700 !important; line-height: 1.2; margin-bottom: .5rem; }
h2 { font-size: 28px !important; font-weight: 600 !important; line-height: 1.25; margin-top: 1.5rem; }
h3 { font-size: 26px !important; font-weight: 600 !important; line-height: 1.3; margin-top: 1rem; }
.hyphenate { hyphens: auto; -webkit-hyphens: auto; -ms-hyphens: auto; }
p { font-size: 1.05rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hyphenate" lang="de"><h1>Visualisierung</h1></div>', unsafe_allow_html=True)
st.divider()

# ---------- Daten laden ----------
BASE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.normpath(os.path.join(BASE, "..", "5.4.3_EL", "graphen_bereinigt.xlsx"))

if not os.path.exists(XLSX):
    st.error("Datei nicht gefunden.")
    ziel_ordner = os.path.join(BASE, "..", "5.4.3_EL")
    try:
        st.write("Inhalt von:", os.path.abspath(ziel_ordner))
        st.code("\n".join(sorted(os.listdir(ziel_ordner))))
    except Exception as e:
        st.write(f"Konnte Ordner nicht lesen: {e}")
    st.stop()

@st.cache_data(show_spinner=False)
def load_df(path):
    return pd.read_excel(path)

df = load_df(XLSX)

# ---------- Spalten robust ermitteln ----------
needed = {"subjekt", "subjekt_type", "prädikat", "objekt", "objekt_type"}
cols_map = {c.lower(): c for c in df.columns}
if not needed.issubset(cols_map):
    st.error("Erforderliche Spalten fehlen. Erwartet: " + ", ".join(sorted(needed)))
    st.stop()

s_col      = cols_map["subjekt"]
s_type_col = cols_map["subjekt_type"]
p_col      = cols_map["prädikat"]
o_col      = cols_map["objekt"]
o_type_col = cols_map["objekt_type"]

# ---------- Sidebar-Filter ----------
st.sidebar.header("Filter")
viz_h = st.sidebar.slider("Höhe Visualisierung (px)", 600, 2000, 1000, 50)

subj_types_all = sorted(df[s_type_col].dropna().astype(str).unique())
obj_types_all  = sorted(df[o_type_col].dropna().astype(str).unique())
preds_all      = sorted(df[p_col].dropna().astype(str).unique())

sel_subj_types = st.sidebar.multiselect("Subjekt-Typen", subj_types_all, default=subj_types_all)
sel_obj_types  = st.sidebar.multiselect("Objekt-Typen",  obj_types_all,  default=obj_types_all)
sel_preds      = st.sidebar.multiselect("Prädikate",      preds_all,      default=preds_all)
node_query     = st.sidebar.text_input("Knoten-Suche (optional, enthält)")

# ---------- DataFrame filtern ----------
f = df[
    df[s_type_col].astype(str).isin(sel_subj_types) &
    df[o_type_col].astype(str).isin(sel_obj_types) &
    df[p_col].astype(str).isin(sel_preds)
].copy()

if node_query:
    q = node_query.strip().lower()
    mask = (
        f[s_col].astype(str).str.lower().str.contains(q) |
        f[o_col].astype(str).str.lower().str.contains(q)
    )
    f = f[mask]

st.caption(f"Gefiltert: {len(f)} Kanten")

# ---------- Typ-Normalisierung ----------
def norm_type(x: str) -> str:
    return (x or "").strip().lower()

# ---------- Knoten-Typen sammeln (Mehrfach-Typen unterstützen) ----------
node_types = defaultdict(set)
for _, r in f[[s_col, s_type_col, o_col, o_type_col]].dropna(subset=[s_col, o_col]).iterrows():
    node_types[str(r[s_col])].add(norm_type(str(r[s_type_col])))
    node_types[str(r[o_col])].add(norm_type(str(r[o_type_col])))

def group_for(node: str) -> str:
    ts = sorted(t for t in node_types.get(node, set()) if t and t != "nan")
    if not ts:
        return "unbekannt"
    if len(ts) == 1:
        return ts[0]
    return "gemischt"

def tooltip_for(node: str) -> str:
    ts = sorted(node_types.get(node, set()))
    pretty = ", ".join(ts) if ts else "n/a"
    return f"{node} — Typ(en): {pretty}"

# ---------- Graph bauen ----------
G = nx.DiGraph()
for _, row in f[[s_col, p_col, o_col]].dropna(subset=[s_col, o_col]).iterrows():
    s, p, o = str(row[s_col]), str(row[p_col]), str(row[o_col])
    G.add_edge(s, o, label=p)  # Nodes entstehen implizit

# ---------- Farbzuordnung + Legende (eine Quelle für beides) ----------
COLOR_PRESET = {
    "person":       "#4e79a7",
    "organisation": "#f28e2b",
    "location":     "#59a14f",
    "weg":          "#e15759",
    "event":        "#edc948",
    "datum":        "#b07aa1",   # korrekt: 'datum'
    "tätigkeit":    "#76b7b2",
    "gemischt":     "#9e9e9e",
    "unbekannt":    "#bab0ac",
}
def color_for(group: str) -> str:
    return COLOR_PRESET.get(norm_type(group), "#7f7f7f")

groups_in_use = sorted({group_for(n) for n in G.nodes()})
group_colors = {g: color_for(g) for g in groups_in_use}

def legend_html(group_colors: dict) -> str:
    items = "".join(
        f'<div class="legend-item"><span class="legend-color" style="background:{c}"></span>{g}</div>'
        for g, c in group_colors.items()
    )
    return f"""
    <style>
      .legend {{ display:flex; flex-wrap:wrap; gap:.5rem 1rem; margin:.5rem 0 1rem; }}
      .legend-item {{ display:flex; align-items:center; gap:.5rem;
                      padding:.15rem .5rem; border-radius:999px;
                      background:rgba(0,0,0,.03); font-size:.95rem; }}
      .legend-color {{ width:14px; height:14px; border-radius:50%;
                       border:1px solid rgba(0,0,0,.25); }}
    </style>
    <div class="legend">{items}</div>
    """

st.markdown(legend_html(group_colors), unsafe_allow_html=True)

# ---------- PyVis erzeugen (Gruppenfarben explizit übergeben) ----------
net = Network(height=f"{viz_h}px", width="100%", directed=True, cdn_resources="in_line")

# Gruppenfarben an vis.js übergeben, damit Graph = Legende
group_opts = ",\n".join([f'"{g}": {{"color": "{c}"}}' for g, c in group_colors.items()])
net.set_options(f"""
{{
  "nodes": {{"size": 28, "borderWidth": 2, "font": {{"size": 22}}}},
  "edges": {{
    "width": 2,
    "smooth": false,
    "arrows": {{"to": {{"enabled": true, "scaleFactor": 0.8}}}},
    "font": {{"size": 16, "align": "top"}}
  }},
  "interaction": {{"zoomView": true, "dragView": true}},
  "physics": {{
    "barnesHut": {{"gravitationalConstant": -15000, "springLength": 260, "springConstant": 0.02}},
    "stabilization": {{"enabled": true, "iterations": 200}}
  }},
  "groups": {{ {group_opts} }}
}}
""")

# --- Knoten & Kanten nur einmal hinzufügen; KEIN color= am Knoten ---
for n in G.nodes():
    g = group_for(n)  # z. B. "datum", "person", ...
    net.add_node(n, label=n, title=tooltip_for(n), group=g)

for u, v, edata in G.edges(data=True):
    net.add_edge(u, v, label=str(edata.get("label", "")))

# ---------- Rendern ----------
html = net.generate_html()
st.components.v1.html(html, height=viz_h, scrolling=True)
