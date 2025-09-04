import streamlit as st
st.set_page_config(layout="wide", page_title="karte")

import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit.components.v1 import html
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
/* Sidebar sichtbar breiter machen */
section[data-testid="stSidebar"] { width: 420px !important; }
div[data-testid="stSidebarContent"] { width: 420px !important; }

/* In der Sidebar: Schrift minimal kleiner für bessere Sichtbarkeit */
section[data-testid="stSidebar"] * { font-size: 18px !important; }

/* Multiselect in der Sidebar: volle Breite nutzen, Tags nicht zu stark abschneiden */
section[data-testid="stSidebar"] div[data-baseweb="select"] { min-width: 100% !important; }
section[data-testid="stSidebar"] div[data-baseweb="tag"] { max-width: 100% !important; }
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

# ---------- Prüfen, ob nötige Spalten existieren ----------
required_cols = {"objekt_type", "lat", "lon", "prädikat"}
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Fehlende Spalten: {', '.join(missing)}")
    st.stop()

# ---------- Orte auf Karte (objekt_type == "location"; Farbe/Filter nach "prädikat") ----------
st.subheader("Orte auf der Karte (farblich & filterbar nach »prädikat«)")

# 1) Filtern & bereinigen (nur Locations)
locs = df[df["objekt_type"].astype(str).str.lower().eq("location")].copy()
for col in ["lat", "lon"]:
    locs[col] = pd.to_numeric(locs[col], errors="coerce")
locs = locs.dropna(subset=["lat", "lon"])
locs = locs[locs["lat"].between(-90, 90) & locs["lon"].between(-180, 180)]

if locs.empty:
    st.warning("Keine gültigen Orte gefunden (objekt_type='location' mit lat/lon).")
    st.stop()

# 2) Kategorien + Farben einmalig festlegen (stabile Farben)
locs["__cat"] = locs["prädikat"].fillna("Unbekannt").astype(str)
unique_all = sorted(locs["__cat"].unique())
palette = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173",
    "#3182bd", "#e6550d", "#31a354", "#756bb1", "#636363"
]
color_map = {cat: palette[i % len(palette)] for i, cat in enumerate(unique_all)}
locs["__color"] = locs["__cat"].map(color_map)

# 3) Sidebar-Filter
st.sidebar.header("Filter")
selected = st.sidebar.multiselect(
    "Prädikat auswählen",
    options=unique_all,
    default=unique_all,
    help="Wähle eine oder mehrere Kategorien; die Karte aktualisiert sich automatisch."
)

if not selected:
    st.info("Bitte mindestens eine Kategorie im Filter wählen.")
    st.stop()

locs_f = locs[locs["__cat"].isin(selected)].copy()

# 4) Karte bauen
center = [float(locs_f["lat"].median()), float(locs_f["lon"].median())]
m = folium.Map(
    location=center,
    zoom_start=5,
    tiles="OpenStreetMap",
    control_scale=True,
    width="100%",
    height="100%"
)

cluster = MarkerCluster(name="Orte").add_to(m)

# 5) Marker erzeugen
popup_cols = [c for c in ["prädikat", "objekt_type"] if c in locs_f.columns]

for _, row in locs_f.iterrows():
    tooltip = f"{row.get('prädikat', '—')}"
    html_info = "<b>Info</b><br>" + "<br>".join(
        f"<b>{c}:</b> {row.get(c, '')}" for c in popup_cols
    )
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=6,
        weight=1,
        fill=True,
        fill_opacity=0.9,
        color=row["__color"],
        fill_color=row["__color"],
        tooltip=tooltip,
        popup=folium.Popup(html_info, max_width=300),
    ).add_to(cluster)

# 6) Legende (nur ausgewählte Kategorien anzeigen, Farben bleiben stabil)
legend_html = """<div style="position: fixed; bottom: 20px; left: 20px; z-index:9999;
background: white; padding: 10px 14px; border:1px solid #ddd; border-radius: 8px;
box-shadow: 0 2px 10px rgba(0,0,0,.1); font-size:14px; max-height: 50vh; overflow:auto;">
<b>Prädikat</b><br>{items}</div>"""
items = "".join(
    f'<span style="display:inline-block;width:12px;height:12px;background:{color_map[c]};'
    f'margin-right:8px;border-radius:50%;"></span>{c}<br>'
    for c in selected
)
m.get_root().html.add_child(folium.Element(legend_html.format(items=items)))

# 7) Karte einbetten
map_html = m.get_root().render()
html(map_html, height=650, scrolling=False)

st.caption(f"{len(locs_f):,} Orte dargestellt • {len(selected)} ausgewählte Kategorie(n)")
