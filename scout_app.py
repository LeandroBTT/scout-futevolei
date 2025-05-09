# Protótipo de app para marcar eventos em vídeos de jogos (como pontos, erros, fundamentos)
# Requisitos: streamlit, opencv-python

import streamlit as st
import cv2
import pandas as pd
import tempfile

st.title("Scout Interativo de Futevôlei")

# Estado inicial
if "eventos" not in st.session_state:
    st.session_state.eventos = []

if "frame_n" not in st.session_state:
    st.session_state.frame_n = 0

if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False

uploaded_video = st.file_uploader("Envie o vídeo do jogo", type=["mp4", "mov"])

if uploaded_video and not st.session_state.video_loaded:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())
    st.session_state.cap = cv2.VideoCapture(tfile.name)
    st.session_state.fps = st.session_state.cap.get(cv2.CAP_PROP_FPS)
    st.session_state.video_loaded = True

if st.session_state.video_loaded:
    cap = st.session_state.cap
    cap.set(cv2.CAP_PROP_POS_FRAMES, st.session_state.frame_n)
    ret, frame = cap.read()

    if ret:
        st.image(frame, channels="BGR")
        st.write(f"Frame: {st.session_state.frame_n}")

        col1, col2 = st.columns(2)
        with col1:
            jogador = st.selectbox("Jogador", ["Joao", "Jojo"])
            fundamento = st.selectbox("Fundamento", ["Recepção", "Levantamento", "Ataque", "Defesa", "Saque", "Cobertura"])
            acao = st.text_input("Ação usada")

        with col2:
            resultado = st.selectbox("Resultado", ["Ponto a favor", "Ponto contra", "Continua"])
            erro = st.selectbox("Erro", ["Sim", "Não"])
            observacoes = st.text_input("Observações")

        if st.button("Marcar Evento Agora"):
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

        col3, col4, col5 = st.columns(3)

        if col3.button("Avançar +20 Frames"):
            st.session_state.frame_n += 20
            st.rerun()

        if col4.button("Avançar +40 Frames"):
            st.session_state.frame_n += 40
            st.rerun()

        if col5.button("Exportar Planilha"):
            df = pd.DataFrame(st.session_state.eventos)
            df.to_excel("Scout_Eventos_Jogo.xlsx", index=False)
            st.success("Planilha exportada como 'Scout_Eventos_Jogo.xlsx'")

    else:
        st.warning("Fim do vídeo.")