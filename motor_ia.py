import os
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# 1. Configuração da Página Web
st.set_page_config(page_title="Karakuria AI", page_icon="🤖", layout="centered")
st.title("🦇 Karakuria Core v2.0")
st.caption("Sistema de Inteligência e Infraestrutura Operante")

# 2. Conexão com o Cofre (Modo Robusto)
load_dotenv()
chave_secreta = None

if "GROQ_API_KEY" in st.secrets:
    chave_secreta = st.secrets["GROQ_API_KEY"]
else:
    chave_secreta = os.getenv("GROQ_API_KEY")

if not chave_secreta:
    st.error("Erro crítico: Chave de API não configurada.")
    st.stop()

cliente = Groq(api_key=chave_secreta.strip())

# 3. Gerenciamento da Memória
if "historico" not in st.session_state:
    st.session_state.historico = [
        {"role": "system", "content": "Você é a Karakuria, uma assistente de infraestrutura e dados irônica e direta."}
    ]

# 4. Renderização
for mensagem in st.session_state.historico:
    if mensagem["role"] != "system":
        with st.chat_message(mensagem["role"]):
            if isinstance(mensagem["content"], list):
                st.markdown(mensagem["content"][0]["text"])
                st.caption("📎 [Imagem processada]")
            else:
                st.markdown(mensagem["content"])

# 5. Módulo de Sensores
with st.sidebar:
    st.header("Módulo de Sensores")
    imagem_anexada = st.file_uploader("Upload", type=["png", "jpg", "jpeg"])

comando = st.chat_input("Fale com a Karakuria...")

if comando:
    with st.chat_message("user"):
        st.markdown(comando)

    # 6. Lógica de Roteamento (Visão vs Texto)
    if imagem_anexada:
        bytes_imagem = imagem_anexada.getvalue()
        imagem_base64 = base64.b64encode(bytes_imagem).decode('utf-8')
        conteudo_usuario = [
            {"type": "text", "text": comando},
            {"type": "image_url", "image_url": {"url": f"data:{imagem_anexada.type};base64,{imagem_base64}"}}
        ]
        st.session_state.historico.append({"role": "user", "content": conteudo_usuario})
        motor_selecionado = "llama-3.2-11b-vision-instruct" 
    else:
        st.session_state.historico.append({"role": "user", "content": comando})
        motor_selecionado = "llama-3.1-8b-instant"

    # 7. Execução
    with st.spinner("Processando..."):
        resposta = cliente.chat.completions.create(
            model=motor_selecionado,
            messages=st.session_state.historico
        )
        conteudo_resposta = resposta.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(conteudo_resposta)
        st.session_state.historico.append({"role": "assistant", "content": conteudo_resposta})