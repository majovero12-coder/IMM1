import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# ========== CONFIGURACIÓN DE LA APP ==========
st.set_page_config(page_title="Texto a Audio", layout="centered")

# ======== ESTILOS PERSONALIZADOS (VISIBLES) ========
st.markdown("""
<style>
/* Fondo principal con degradado */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #FFE0B2 0%, #FFCDD2 100%);
    color: #3E2723;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FFF3E0;
    color: #BF360C;
    font-weight: bold;
}

/* Contenedor principal */
.block-container {
    background-color: #FFFFFFE6;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 0 25px rgba(0,0,0,0.1);
}

/* Títulos */
h1 {
    color: #E65100;
    text-align: center;
    font-family: 'Trebuchet MS', sans-serif;
}

h2, h3, p, label, span {
    color: #4E342E;
    font-family: 'Verdana';
}

/* Botones */
div.stButton > button {
    background: linear-gradient(90deg, #FF7043, #F4511E);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: bold;
    transition: 0.3s;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #F4511E, #E64A19);
    transform: scale(1.05);
}

/* Área de texto */
textarea {
    border-radius: 10px !important;
    border: 2px solid #FF7043 !important;
}

/* Enlace de descarga */
a {
    color: #E64A19 !important;
    font-weight: bold;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# ======== TÍTULO PRINCIPAL ========
st.title("🎙️ Conversión de Texto a Audio")

image = Image.open('gato_raton.png')
st.image(image, width=350)

with st.sidebar:
    st.subheader("📚 Instrucciones")
    st.write("Escribe o selecciona un texto y escucha su narración.")
    st.write("Puedes cambiar el idioma para practicar pronunciación.")

# ======== CREAR CARPETA TEMPORAL ========
os.makedirs("temp", exist_ok=True)

# ======== TEXTO DE EJEMPLO ========
st.subheader("🐭 Una pequeña Fábula")
st.write(
    '¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. '
    'Al principio era tan grande que le tenía miedo. Corría y corría y por cierto que me alegraba ver esos muros, '
    'a diestra y siniestra, en la distancia. Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto '
    'y ahí en el rincón está la trampa sobre la cual debo pasar. "Todo lo que debes hacer es cambiar de rumbo", '
    'dijo el gato... y se lo comió. – *Franz Kafka*.'
)

st.markdown("🎧 ¿Quieres escucharlo? Copia el texto o escribe el tuyo abajo:")

# ======== ENTRADA DE TEXTO ========
text = st.text_area("✍️ Escribe aquí el texto que deseas convertir a audio:")

# ======== SELECCIÓN DE IDIOMA ========
option_lang = st.selectbox("🌎 Selecciona el idioma:", ("Español", "English"))
lg = 'es' if option_lang == "Español" else 'en'

# ======== FUNCIÓN PRINCIPAL DE AUDIO ========
def text_to_speech(text, lg):
    if not text.strip():
        st.warning("Por favor ingresa un texto antes de convertirlo.")
        return None, None

    tts = gTTS(text, lang=lg)
    my_file_name = text[:20] if len(text) > 0 else "audio"
    audio_path = f"temp/{my_file_name}.mp3"
    tts.save(audio_path)
    return audio_path, text

# ======== BOTÓN DE CONVERSIÓN ========
if st.button("🔊 Convertir a Audio"):
    audio_path, output_text = text_to_speech(text, lg)
    if audio_path:
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()
        st.markdown("## 🎵 Tu audio está listo:")
        st.audio(audio_bytes, format="audio/mp3")

        with open(audio_path, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(audio_path)}">⬇️ Descargar audio</a>'
        st.markdown(href, unsafe_allow_html=True)

# ======== LIMPIAR ARCHIVOS ANTIGUOS ========
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

