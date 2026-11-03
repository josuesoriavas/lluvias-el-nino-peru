# Lluvias y El Niño en el Perú (app de Streamlit)

Timelapse mes a mes (desde 1982) del índice de lluvia de 3 meses en los 1,890 distritos, con el ICEN, el RONI y los
eventos El Niño costero oficiales. Tiene dos pestañas: el timelapse interactivo y una pestaña con los datos
(descargables en CSV) y el método.

## Contenido

| Ruta | Qué es |
|---|---|
| `app.py` | La app de Streamlit |
| `componente/timelapse.html` | El timelapse interactivo (mapa en canvas + gráfico d3); la app le inyecta los datos |
| `datos/` | Los cuatro JSON que arma `scripts/06_timelapse_lluvia_enso.py` |
| `requirements.txt` | Dependencias para Streamlit Community Cloud |

## Probar en tu computadora

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar en Streamlit Community Cloud (gratis)

1. Crea un repositorio en GitHub y sube **el contenido de esta carpeta** (`app.py` debe quedar en la raíz o anota su ruta).
   Los datos pesan unos 2 MB.
2. Entra a <https://share.streamlit.io> con tu cuenta de GitHub y elige **Create app → Deploy a public app from GitHub**.
3. Selecciona el repositorio, la rama y el archivo principal `app.py`. Si quieres una dirección fija, cámbiala en **App URL**.
4. Pulsa **Deploy**. La primera vez tarda uno o dos minutos en instalar las dependencias.

Las apps públicas las puede abrir cualquiera con el enlace. Si el repositorio es privado, Streamlit permite limitar el
acceso a correos invitados desde **Settings → Sharing** de la app.

## Actualizar los datos

Cuando el IGP publique un nuevo ICEN (o NOAA un nuevo RONI), actualiza los archivos de origen y vuelve a correr, desde
la carpeta `FEN - DU`:

```bash
py -I -X utf8 scripts/06_timelapse_lluvia_enso.py streamlit_timelapse/datos
```

Luego sube los archivos cambiados al repositorio; Streamlit Cloud vuelve a desplegar la app solo.
