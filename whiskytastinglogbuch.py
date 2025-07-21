import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# ===== HERRSCHAFTLICHES DESIGN =====
st.set_page_config(
    layout="wide", 
    page_title="🥃 Gentlemen's Whisky Journal", 
    page_icon="🧊",
    initial_sidebar_state="expanded"
)

# Einfacher, eleganter Hintergrund in warmem Braun
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lora:wght@400;700&display=swap');
:root {
    --whisky-gold: #d4af37;
    --leather-brown: #3d291a;
    --text-color: #e8e0cd;
}
body {
    background-color: var(--leather-brown);
    font-family: 'Lora', serif;
    color: var(--text-color);
}
h1, h2, h3, h4 {
    font-family: 'Cinzel', serif;
    color: var(--whisky-gold) !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    letter-spacing: 1px;
}
.stApp {
    background: rgba(61, 41, 26, 0.95) !important;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 0 25px rgba(0,0,0,0.7);
}
.stButton button {
    background: linear-gradient(180deg, var(--leather-brown), #1a1209) !important;
    border: 1px solid var(--whisky-gold) !important;
    border-radius: 4px !important;
    font-family: 'Cinzel' !important;
    letter-spacing: 1.5px;
    color: var(--text-color) !important;
    transition: all 0.3s ease !important;
}
.stButton button:hover {
    background: linear-gradient(180deg, #4d3a28, #2d2317) !important;
    transform: translateY(-2px);
    box-shadow: 0 0 15px var(--whisky-gold);
}
.leather-card {
    background: #4b3925;
    border: 1px solid var(--whisky-gold);
    border-radius: 6px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# ===== DATENSTRUKTUR =====
if 'whisky_log' not in st.session_state:
    st.session_state.whisky_log = pd.DataFrame(columns=[
        'Datum', 'Name', 'Destillerie', 'Alter', 'Region', 'Typ', 'Preis', 
        'Farbe', 'Nase', 'Geschmack', 'Abgang', 'Gesamt', 'Notizen', 'Bewertung'
    ])

# ===== DASHBOARD-KOPF =====
st.title("🥃 Gentlemen's Whisky Journal")
st.markdown("---")
st.subheader("Ein Logbuch für den kenntnisreichen Genießer")

# ===== NEUER EINTRAG =====
with st.expander("✍️ Neuen Whisky eintragen", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏷️ Whisky-Details")
        name = st.text_input("Name", "Macallan 18")
        destillerie = st.text_input("Destillerie", "The Macallan")
        jahre = st.slider("Reifezeit (Jahre)", 5, 50, 18)
        region = st.selectbox("Region", [
            "Speyside", "Highlands", "Islay", "Lowlands", 
            "Campbeltown", "Japan", "USA", "Kanada", "Irland"
        ], index=0)
        typ = st.radio("Typ", ["Single Malt", "Blended", "Bourbon", "Rye", "Andere"], index=0)
        preis = st.number_input("Preis (€)", min_value=0, value=220, step=10)
        
    with col2:
        st.markdown("### 🧪 Sensorische Bewertung")
        farbe = st.select_slider("Farbe", options=[
            "Blassgold", "Bernstein", "Kupfer", "Tiefes Rubin", "Mahagoni"
        ], value="Bernstein")
        
        col3, col4 = st.columns(2)
        with col3:
            nase = st.slider("Nase (1-10)", 1, 10, 8)
            geschmack = st.slider("Geschmack (1-10)", 1, 10, 9)
        with col4:
            abgang = st.slider("Abgang (1-10)", 1, 10, 8)
            gesamt = st.slider("Gesamteindruck (1-10)", 1, 10, 9)
        
        bewertung = (nase + geschmack + abgang + gesamt) / 4
        st.markdown(f"### ⭐ Bewertung: **{bewertung:.1f}/10**")
        
        notizen = st.text_area("Persönliche Notizen", "Vollmundig mit Noten von Trockenfrüchten, Vanille und leichter Eiche. Perfekte Balance.")

    if st.button("📖 Eintrag ins Logbuch", use_container_width=True):
        neuer_eintrag = pd.DataFrame([{
            'Datum': datetime.now().strftime("%d.%m.%Y"),
            'Name': name,
            'Destillerie': destillerie,
            'Alter': jahre,
            'Region': region,
            'Typ': typ,
            'Preis': preis,
            'Farbe': farbe,
            'Nase': nase,
            'Geschmack': geschmack,
            'Abgang': abgang,
            'Gesamt': gesamt,
            'Notizen': notizen,
            'Bewertung': bewertung
        }])
        
        st.session_state.whisky_log = pd.concat(
            [st.session_state.whisky_log, neuer_eintrag], 
            ignore_index=True
        )
        st.success("Eintrag gespeichert!")
        st.balloons()

# ===== VISUALISIERUNGEN =====
st.markdown("---")
st.header("📊 Whisky-Analysen")

if not st.session_state.whisky_log.empty:
    df = st.session_state.whisky_log
    
    # Top-Bewertungen
    top3 = df.nlargest(3, 'Bewertung')
    col1, col2, col3 = st.columns(3)
    for i, col in enumerate([col1, col2, col3]):
        if i < len(top3):
            with col:
                st.markdown(f"<div class='leather-card'>"
                            f"<h3>🥇 Top-{i+1}</h3>"
                            f"<h4>{top3.iloc[i]['Name']}</h4>"
                            f"<p>{top3.iloc[i]['Destillerie']}</p>"
                            f"<p>⭐ <strong>{top3.iloc[i]['Bewertung']:.1f}/10</strong></p>"
                            f"<p>💶 {top3.iloc[i]['Preis']}€</p>"
                            f"</div>", unsafe_allow_html=True)
    
    # Radar-Chart für Sensorik
    st.subheader("🧪 Sensorisches Profil")
    latest = df.iloc[-1]
    fig1 = px.line_polar(
        r=[latest['Nase'], latest['Geschmack'], latest['Abgang'], latest['Gesamt']],
        theta=['Nase', 'Geschmack', 'Abgang', 'Gesamteindruck'],
        line_close=True,
        range_r=[0,10],
        color_discrete_sequence=['#d4af37']
    )
    fig1.update_traces(fill='toself', line=dict(width=3))
    fig1.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,10])
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8e0cd')
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Regionenanalyse
    st.subheader("🗺️ Regionenvergleich")
    region_stats = df.groupby('Region').agg({
        'Bewertung': 'mean',
        'Preis': 'mean',
        'Name': 'count'
    }).reset_index().rename(columns={'Name': 'Anzahl'})
    
    fig2 = px.bar(
        region_stats, 
        x='Region', 
        y='Bewertung',
        color='Preis',
        color_continuous_scale='temps',
        title='Durchschnittliche Bewertung nach Region',
        hover_data=['Anzahl', 'Preis']
    )
    fig2.update_layout(
        xaxis_title="",
        yaxis_title="Bewertung (Ø)",
        plot_bgcolor='rgba(0,0,0,0.2)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8e0cd')
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Preis-Leistungs-Analyse
    st.subheader("💸 Preis-Leistungs-Verhältnis")
    fig3 = px.scatter(
        df,
        x='Preis',
        y='Bewertung',
        color='Alter',
        size='Alter',
        hover_name='Name',
        trendline='ols',
        trendline_color_override='#d4af37'
    )
    fig3.update_layout(
        xaxis_title="Preis (€)",
        yaxis_title="Bewertung",
        plot_bgcolor='rgba(0,0,0,0.2)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8e0cd'),
        legend=dict(
            title="Alter (Jahre)",
            bgcolor='rgba(61, 41, 26, 0.7)'
        )
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Vollständiges Logbuch
    st.subheader("📜 Vollständiges Tasting-Log")
    st.dataframe(
        df.sort_values('Datum', ascending=False).reset_index(drop=True),
        height=400,
        use_container_width=True
    )
    
else:
    st.info("ℹ️ Noch keine Einträge. Fülle dein erstes Tasting-Formular aus!")

# ===== WISSENSDATENBANK =====
with st.expander("📚 Whisky-Wissen für Gentlemen", expanded=True):
    tab1, tab2, tab3 = st.tabs(["Regionale Charaktere", "Degustationstechnik", "Aufbewahrung"])
    
    with tab1:
        st.markdown("""
        **Schottische Regionen:**
        - *Islay:* Torfig, rauchig, medizinisch (Laphroaig, Ardbeg)
        - *Highlands:* Fruchtig, malzig, ausgewogen (Glenmorangie, Oban)
        - *Speyside:* Süß, elegant, komplex (Macallan, Glenfiddich)
        
        **International:**
        - *Japan:* Präzise, rein, umami (Yamazaki, Hibiki)
        - *USA:* Vanille, Karamell, kräftig (Bulleit, Woodford Reserve)
        """)

    with tab2:
        st.markdown("""
        **Professionelles Tasting:**
        1. **Farbe:** Gegen das Licht halten - Alter anzeigend
        2. **Nase:** Erst aus Distanz, dann näher - Mehrfach riechen
        3. **Geschmack:** Kleiner Schluck, im Mund bewegen
        4. **Abgang:** Länge und Entwicklung notieren
        
        **Zugabe Wasser:** 1-2 Tropfen öffnen Aromen
        """)

    with tab3:
        st.markdown("""
        **Ideale Lagerung:**
        - Aufrecht stehend (Kork trocknet sonst aus)
        - Zimmertemperatur (15-20°C)
        - Vor Sonnenlicht schützen
        - Nach Öffnung innerhalb 6 Monate verbrauchen
        
        **Kein Gefrierschrank!** - Zerstört Aromen
        """)

# ===== EXPORT =====
st.markdown("---")
if 'whisky_log' in st.session_state and not st.session_state.whisky_log.empty:
    df = st.session_state.whisky_log
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Logbuch als CSV exportieren",
        data=csv_data,
        file_name='whisky_logbuch.csv',
        mime='text/csv',
        use_container_width=True
    )
else:
    st.info("ℹ️ Keine Daten zum Exportieren vorhanden.")

# ===== FOOTER =====
st.markdown("""
<div style="text-align:center; margin-top:50px; padding:20px; border-top:1px solid #d4af37">
    <p>🧊 Serviert bei Raumtemperatur - Mit oder ohne Tropfen Wasser</p>
    <p>🥃 Genieße verantwortungsvoll - In Maßen, nicht in Massen</p>
</div>
""", unsafe_allow_html=True)
