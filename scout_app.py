# Protótipo de app para marcar eventos em vídeos de jogos (como pontos, erros, fundamentos)
# Requisitos: streamlit, opencv-python

import streamlit as st
import cv2
import pandas as pd
import tempfile
import time

st.set_page_config(layout="wide")  # evita scroll lateral
st.title("Scout Interativo de Futevôlei")

# Inicialização dos estados
if "eventos" not in st.session_state:
    st.session_state.eventos = []
if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False
if "cap" not in st.session_state:
    st.session_state.cap = None
if "fps" not in st.session_state:
    st.session_state.fps = 30
if "frame_n" not in st.session_state:
    st.session_state.frame_n = 0
if "total_frames" not in st.session_state:
    st.session_state.total_frames = 0
if "play" not in st.session_state:
    st.session_state.play = False

# Upload do vídeo
uploaded_video = st.file_uploader("Envie o vídeo do jogo", type=["mp4", "mov"])
if uploaded_video and not st.session_state.video_loaded:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())
    st.session_state.cap = cv2.VideoCapture(tfile.name)
    st.session_state.fps = st.session_state.cap.get(cv2.CAP_PROP_FPS)
    st.session_state.total_frames = st.session_state.cap.get(cv2.CAP_PROP_FRAME_COUNT)
    st.session_state.video_loaded = True

# Exibição do vídeo
stframe = st.empty()

if st.session_state.cap:
    # Controles de Play/Pause e Retroceder
    colPlay1, colPlay2, colPlay3 = st.columns(3)
    with colPlay1:
        if st.button("<< Voltar 5s"):
            st.session_state.frame_n = max(0, st.session_state.frame_n - int(5 * st.session_state.fps))
            st.experimental_rerun()
    with colPlay2:
        if not st.session_state.play:
            if st.button("▶️ Play"):
                st.session_state.play = True
                st.experimental_rerun()
        else:
            if st.button("⏸️ Pause"):
                st.session_state.play = False
    with colPlay3:
        if st.button(">> Avançar 5s"):
            st.session_state.frame_n = min(
                int(st.session_state.total_frames - 1),
                st.session_state.frame_n + int(5 * st.session_state.fps)
            )
            st.experimental_rerun()

    # Play contínuo
    if st.session_state.play:
        while st.session_state.frame_n < st.session_state.total_frames:
            st.session_state.cap.set(cv2.CAP_PROP_POS_FRAMES, st.session_state.frame_n)
            ret, frame = st.session_state.cap.read()
            if not ret:
                break
            stframe.image(frame, channels="BGR", use_column_width=True)
            st.session_state.frame_n += 1
            time.sleep(1 / st.session_state.fps)
        st.session_state.play = False
        st.experimental_rerun()
    else:
        st.session_state.cap.set(cv2.CAP_PROP_POS_FRAMES, st.session_state.frame_n)
        ret, frame = st.session_state.cap.read()
        if ret:
            stframe.image(frame, channels="BGR", use_column_width=True)

    # Formulário de marcação
    st.markdown("---")
    st.markdown("### Comandos para Marcar Eventos")
    col1, col2 = st.columns(2)
    with col1:
        jogador = st.selectbox("Jogador", ["Joao", "Jojo"])
        fundamento = st.selectbox("Fundamento", ["Recepção", "Levantamento", "Ataque", "Defesa", "Saque", "Cobertura"])
        acao = st.text_input("Ação usada")
    with col2:
        resultado = st.selectbox("Resultado", ["Ponto a favor", "Ponto contra", "Continua"])
        erro = st.selectbox("Erro", ["Sim", "Não"])
        observacoes = st.text_input("Observações")

    col3, col4, col5 = st.columns(3)
    if col3.button("Marcar Evento Agora"):
        tempo = st.session_state.frame_n / st.session_state.fps
        st.session_state.eventos.append({
            "tempo_segundos": round(tempo, 2),
            "jogador": jogador,
            "fundamento": fundamento,
            "acao_usada": acao,
            "resultado": resultado,
            "erro": erro,
            "observacoes": observacoes
        })
        st.success(f"Evento marcado aos {round(tempo, 2)} segundos")

    if col4.button("Exportar Planilha Final"):
        df = pd.DataFrame(st.session_state.eventos)
        df.to_excel("Scout_Eventos_Jogo.xlsx", index=False)
        st.success("Planilha exportada como 'Scout_Eventos_Jogo.xlsx'")

    if col5.button("Salvar Parcial"):
        df = pd.DataFrame(st.session_state.eventos)
        df.to_excel("Scout_Eventos_Jogo_Parcial.xlsx", index=False)
        st.success("Planilha parcial salva como 'Scout_Eventos_Jogo_Parcial.xlsx'")

    # Controles de frame
    st.markdown("---")
    st.markdown("### Navegar por Frames")
    col7, col8, col9, col10 = st.columns(4)
    if col7.button("Frame +10"):
        st.session_state.frame_n = min(
            int(st.session_state.total_frames - 1),
            st.session_state.frame_n + 10
        )
        st.experimental_rerun()
    if col8.button("Frame +20"):
        st.session_state.frame_n = min(
            int(st.session_state.total_frames - 1),
            st.session_state.frame_n + 20
        )
        st.experimental_rerun()
    if col9.button("Frame +40"):
        st.session_state.frame_n = min(
            int(st.session_state.total_frames - 1),
            st.session_state.frame_n + 40
        )
        st.experimental_rerun()
    if col10.button("Frame +15s"):
        st.session_state.frame_n = min(
            int(st.session_state.total_frames - 1),
            st.session_state.frame_n + int(15 * st.session_state.fps)
        )
        st.experimental_rerun()

    col11, col12 = st.columns(2)
    if col11.button("Frame +30s"):
        st.session_state.frame_n = min(
            int(st.session_state.total_frames - 1),
            st.session_state.frame_n + int(30 * st.session_state.fps)
        )
        st.experimental_rerun()