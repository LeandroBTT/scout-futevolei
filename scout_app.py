# Protótipo de app para marcar eventos em vídeos de jogos (como pontos, erros, fundamentos)
# Requisitos: streamlit, opencv-python

import streamlit as st
import cv2
import pandas as pd
import tempfile
import time

st.title("Scout Interativo de Futevôlei")

if "eventos" not in st.session_state:
    st.session_state.eventos = []

uploaded_video = st.file_uploader("Envie o vídeo do jogo", type=["mp4", "mov"])

if uploaded_video:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())
    cap = cv2.VideoCapture(tfile.name)
    stframe = st.empty()

    eventos = st.session_state.eventos

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

if "marcar" not in st.session_state: st.session_state.marcar = False

if st.button("Marcar Evento Agora"): st.session_state.marcar = True

    salvar = st.button("Exportar Planilha")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_n = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_n += 1
        stframe.image(frame, channels="BGR")
        time.sleep(1.0 / fps)

if st.session_state.marcar:
    tempo = frame_n / fps
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
    st.session_state.marcar = False

        if salvar:
            df = pd.DataFrame(eventos)
            df.to_excel("Scout_Eventos_Jogo.xlsx", index=False)
            st.success("Planilha exportada como 'Scout_Eventos_Jogo.xlsx'")
            break

    cap.release()
