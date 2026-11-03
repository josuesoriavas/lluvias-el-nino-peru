"""
App de Streamlit: timelapse de lluvias y El Niño en el Perú.

El timelapse interactivo es un componente HTML (componente/timelapse.html) que recibe los datos de la carpeta
datos/ (los arma scripts/06_timelapse_lluvia_enso.py). Si hay MP4 en videos/, se muestran en su pestaña.

Uso local:
    pip install -r requirements.txt
    streamlit run app.py
"""
import json
from pathlib import Path

import pandas as pd
import streamlit as st

BASE = Path(__file__).parent
ARCHIVOS = {"lluvia": "lluvia_distrital_3m.json", "limites": "limites_distritales.json",
            "indices": "indices_enso_mensual.json", "eventos": "eventos_el_nino_costero.json"}

st.set_page_config(page_title="Lluvias y El Niño en el Perú", layout="wide")


@st.cache_data
def cargar():
    return {k: json.loads((BASE / "datos" / f).read_text(encoding="utf-8")) for k, f in ARCHIVOS.items()}


def pagina():
    datos = json.dumps(cargar(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return (BASE / "componente" / "timelapse.html").read_text(encoding="utf-8").replace("__DATOS__", datos)


datos = cargar()
ind = pd.DataFrame(datos["indices"])
ev = pd.DataFrame(datos["eventos"])
con_lluvia = ind[ind.pct_muy_humedo.notna()]

st.title("Lluvias y El Niño en el Perú")
st.markdown(
    f"Mes a mes desde {ind.mes.iloc[0][:4]}: cuánto llovió en cada distrito en los últimos tres meses comparado con lo "
    "habitual, junto al **ICEN** (mar frente a la costa) y el **RONI** (Pacífico central). "
    f"Lluvia hasta {con_lluvia.mes.iloc[-1]}; índices hasta {ind.mes.iloc[-1]}."
)

tab_tl, tab_video, tab_datos = st.tabs(["Timelapse", "Videos", "Datos y método"])

with tab_tl:
    st.iframe(pagina(), height="content")

with tab_video:
    videos = sorted((BASE / "videos").glob("*.mp4"))
    if not videos:
        st.info("Todavía no hay videos en la carpeta videos/. Se generan con scripts/07_video_timelapse.py.")
    for v in videos:
        st.subheader("Todos los meses" if "mensual" in v.stem else "Solo temporadas feb–abr")
        st.video(str(v))

with tab_datos:
    st.subheader("Cómo se calcula")
    st.markdown(
        """
- **Índice de lluvia.** En cada distrito se suma la lluvia PISCOp v3.0 (SENAMHI) del mes y de los dos anteriores, y se
  compara con la misma ventana de todos los años 1982–2025 en ese distrito: se ordenan los años, el rango pasa a
  probabilidad (Gringorten) y luego a una normal estándar. Verde es más lluvia que lo habitual; marrón, menos.
- **Muy húmedo y muy seco.** El índice supera una desviación estándar por encima o por debajo de lo normal. Donde casi
  nunca llueve en esa época (la costa en invierno) los años empatan y el índice queda cerca de cero.
- **Temporadas clave.** Las temporadas feb–abr de los grandes eventos El Niño (1983, 1998, 2017 y 2023) y las vecinas
  (1997, 2016 y 2024), para comparar el antes y el después de cada uno.
- **ICEN.** Índice Costero El Niño oficial del IGP/ENFEN (región Niño 1+2). El último mes viene del informe del ENFEN y es provisional.
- **RONI.** Índice relativo del Niño oceánico de NOAA-CPC (Pacífico central), asignado al mes central de su trimestre.
- **Eventos.** Lista oficial de eventos El Niño costero del IGP/ENFEN. El evento de 2026 aún no tiene categoría
  oficial: se marca desde que el ICEN pasó el umbral cálido.
"""
    )
    st.subheader("Índices y lluvia nacional por mes")
    tabla = ind.rename(columns={"mes": "Mes", "icen": "ICEN", "icen_provisional": "ICEN provisional", "roni": "RONI",
                                "pct_muy_humedo": "% distritos muy húmedos", "pct_muy_seco": "% distritos muy secos",
                                "evento": "Evento El Niño costero", "temporada_clave": "Temporada clave"})
    st.dataframe(tabla, hide_index=True, width="stretch", height=320)
    st.download_button("Descargar índices (CSV)", tabla.to_csv(index=False).encode("utf-8-sig"),
                       "indices_enso_mensual.csv", "text/csv")
    st.subheader("Eventos El Niño costero")
    st.dataframe(ev.rename(columns={"id": "Código", "etiqueta": "Evento", "magnitud": "Magnitud", "inicio": "Inicio",
                                    "fin": "Fin", "icen_pico": "ICEN máximo"}), hide_index=True, width="stretch")
    st.download_button("Descargar eventos (CSV)", ev.to_csv(index=False).encode("utf-8-sig"),
                       "eventos_el_nino_costero.csv", "text/csv")
    st.caption("Fuentes: PISCOp v3.0 (SENAMHI); ICEN y lista de eventos (IGP/ENFEN); RONI (NOAA-CPC); "
               "límites distritales del V Censo Nacional Económico.")
