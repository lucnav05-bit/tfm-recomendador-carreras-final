import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Configuración básica
st.set_page_config(page_title="Recomendador de carreras/estudios — TFM", layout="centered")

# Archivo del dataset 
DATASET_FILE = Path("dataset_tfm_recomendacion_carreras.csv")

# Columnas de intereses (12) y columna objetivo
FEATURES = [f"Interes_{i}" for i in range(1, 13)]
TARGET = "Carrera_Asignada"

# Nombres visibles (en el mismo orden que Interes_1..Interes_12)
INTEREST_LABELS = [
    "Matemáticas / Cálculo",
    "Física / Experimentación",
    "Biología / Salud",
    "Química / Laboratorio",
    "Programación / Computación",
    "Diseño / Creatividad",
    "Comunicación / Redacción",
    "Idiomas / Humanidades",
    "Economía / Negocios",
    "Derecho / Normativa",
    "Psicología / Social",
    "Arte / Expresión",
]

# Preguntas (3 por cada interés → 36 ítems)
QUESTION_BANK = {
    "Interes_1": [
        "Disfruto resolviendo problemas matemáticos.",
        "Me atraen el cálculo y el álgebra.",
        "Me siento cómodo/a con fórmulas y números."
    ],
    "Interes_2": [
        "Me gusta la experimentación física.",
        "Me interesan los fenómenos del mundo real (fuerzas, energía...).",
        "Me divierte construir y probar dispositivos."
    ],
    "Interes_3": [
        "Me atraen la biología y las ciencias de la salud.",
        "Me gustaría trabajar en ámbitos sanitarios o investigación biomédica.",
        "Sigo contenidos de medicina, fisiología o genética."
    ],
    "Interes_4": [
        "Me resulta interesante el laboratorio químico.",
        "Disfruto analizando sustancias y reacciones.",
        "Soy detallista con protocolos y seguridad."
    ],
    "Interes_5": [
        "Me gusta programar o automatizar tareas.",
        "Me atraen la IA, los datos o el desarrollo de software.",
        "Disfruto aprendiendo nuevos lenguajes/tecnologías."
    ],
    "Interes_6": [
        "Me gusta diseñar y crear cosas nuevas.",
        "Me atraen el diseño gráfico, UX o producto.",
        "Disfruto con herramientas creativas."
    ],
    "Interes_7": [
        "Se me da bien comunicar ideas por escrito.",
        "Disfruto hablando en público o contando historias.",
        "Me atrae el periodismo, la publicidad o los medios."
    ],
    "Interes_8": [
        "Me gustan los idiomas y las humanidades.",
        "Me interesa la historia, filosofía o literatura.",
        "Disfruto analizando textos y contextos culturales."
    ],
    "Interes_9": [
        "Me atraen los negocios y la economía.",
        "Disfruto analizando mercados y tomando decisiones.",
        "Me interesan finanzas, marketing o emprendimiento."
    ],
    "Interes_10": [
        "Me interesa el derecho y la normativa.",
        "Me gusta argumentar y estructurar casos.",
        "Soy riguroso/a con procesos y detalle legal."
    ],
    "Interes_11": [
        "Me interesan la psicología y el comportamiento humano.",
        "Disfruto ayudando a las personas.",
        "Me gusta investigar aspectos sociales."
    ],
    "Interes_12": [
        "Me atraen el arte y la expresión.",
        "Disfruto con música, cine, teatro o artes visuales.",
        "Me motiva crear y explorar lenguajes artísticos."
    ],
}

# Carga de datos 
if not DATASET_FILE.exists():
    st.error(
        "No se encontró el archivo `dataset_tfm_recomendacion_carreras.csv`.\n\n"
        "Súbelo a la carpeta principal del repositorio, junto a `app.py`."
    )
    st.stop()

df = pd.read_csv(DATASET_FILE)

# Comprobación mínima de columnas
missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
if missing:
    st.error(f"Faltan columnas en el CSV: {', '.join(missing)}")
    st.stop()

# Convertimos a numérico por si acaso y limitamos a 1..5
df[FEATURES] = df[FEATURES].apply(pd.to_numeric, errors="coerce").fillna(3).clip(1, 5)

# Perfiles de carrera (modelo sencillo) 
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(df[FEATURES].values)

df_scaled = pd.DataFrame(X_scaled, columns=FEATURES)
df_scaled[TARGET] = df[TARGET].values

# Perfil promedio por carrera (en escala 0–1)
profiles = df_scaled.groupby(TARGET)[FEATURES].mean()
career_names = profiles.index.tolist()

# Interfaz 
st.title("Recomendador de carreras/estudios")
st.caption("TFM — Prototipo basado en intereses (perfil promedio + similitud coseno).")

with st.expander("Cómo usar esta aplicación", expanded=True):
    st.write(
        "- Responde 36 afirmaciones (1 = muy en desacuerdo, 5 = muy de acuerdo).\n"
        "- Se calcula tu perfil en 12 intereses y se compara con cada carrera.\n"
        "- La afinidad se basa en una medida de semejanza entre vectores (similitud coseno).\n"
        "- En la pestaña *Datos* puedes ver una muestra del dataset."
    )

tab_app, tab_data = st.tabs(["Recomendador", "Datos"])

with tab_app:
    st.subheader("1) Cuestionario (36 ítems)")

    with st.form("form_intereses"):
        cols = st.columns(3)
        raw_answers = {}
        # Pintamos 3 preguntas por cada interés
        for idx, (feat, questions) in enumerate(QUESTION_BANK.items(), start=1):
            with cols[(idx - 1) % 3]:
                st.markdown(f"**{INTEREST_LABELS[idx - 1]}**")
                for q_i, q_text in enumerate(questions, start=1):
                    key = f"{feat}_q{q_i}"
                    raw_answers[key] = st.slider(q_text, 1, 5, 3, key=key)
                st.divider()
        submitted = st.form_submit_button("Calcular recomendaciones")

    # Si se envía el formulario, hacemos la media (3 preguntas → 1 valor por interés)
    if submitted:
        user_vals = []
        for feat in FEATURES:
            vals = [raw_answers[f"{feat}_q{j}"] for j in range(1, 4)]
            user_vals.append(int(round(sum(vals) / 3)))
    else:
        user_vals = [3] * len(FEATURES)  # valores por defecto

    user = np.array(user_vals).reshape(1, -1)
    user_scaled = scaler.transform(user)

    st.subheader("2) Recomendaciones")
    top_n = st.slider("¿Cuántas recomendaciones quieres ver?", 1, min(10, len(career_names)), 5)

    sims = cosine_similarity(user_scaled, profiles.values)[0]
    order = np.argsort(sims)[::-1]

    rows = []
    for rank in range(top_n):
        j = order[rank]
        carrera = profiles.index[j]
        score = float(sims[j])

        # Explicación simple: intereses que más aportan
        contrib = user_scaled[0] * profiles.values[j]
        idx_top = np.argsort(contrib)[::-1][:3]
        feats = [INTEREST_LABELS[k] for k in idx_top]

        with st.container(border=True):
            st.markdown(
                f"### {rank+1}. **{carrera}** — Afinidad: "
                f"<span style='background:#e8fff1;border-radius:6px;padding:2px 6px'><b>{score*100:.1f}%</b></span>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**¿Por qué?** Mayor coincidencia en: {', '.join(feats)}.")

        rows.append({
            "rank": rank+1,
            "carrera": carrera,
            "afinidad": score,
            "explicacion_top3": ", ".join(feats)
        })

    # Gráfica sencilla para la carrera con mayor afinidad
    st.subheader("3) Explicación visual (Top-1)")
    if len(order) > 0:
        top1_idx = order[0]
        contrib_top1 = user_scaled[0] * profiles.values[top1_idx]
        pares = sorted(zip(INTEREST_LABELS, contrib_top1), key=lambda x: x[1], reverse=True)[:6]
        labels_plot, vals_plot = zip(*pares)
        chart_df = pd.DataFrame({"Contribución": vals_plot}, index=labels_plot)
        st.bar_chart(chart_df.sort_values("Contribución"))
        st.caption(f"Factores que más suman → **{profiles.index[top1_idx]}**")

    # Descargas en CSV (sencillas)
    st.divider()
    st.subheader("Descargar resultados (CSV)")

    recs_df = pd.DataFrame(rows)
    st.download_button(
        "Descargar recomendaciones (CSV)",
        data=recs_df.to_csv(index=False).encode("utf-8"),
        file_name="recomendaciones_usuario.csv",
        mime="text/csv",
        use_container_width=True,
    )

    perfil_df = pd.DataFrame([dict(zip(INTEREST_LABELS, user_vals))])
    st.download_button(
        "Descargar mi perfil (12 intereses) (CSV)",
        data=perfil_df.to_csv(index=False).encode("utf-8"),
        file_name="perfil_usuario.csv",
        mime="text/csv",
        use_container_width=True,
    )

with tab_data:
    st.subheader("Vista previa del dataset")
    st.dataframe(df.sample(min(10, len(df)), random_state=42), use_container_width=True)

    st.subheader("Perfiles medios por carrera (primeras 10)")
    st.dataframe(profiles.head(10), use_container_width=True)

st.divider()
st.caption(
    "TFM — Prototipo de recomendación basado en intereses. "
    "Perfiles promedio por carrera + comparación por similitud coseno."
)
