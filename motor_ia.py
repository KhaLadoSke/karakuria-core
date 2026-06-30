import os
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# 1. Configuração da Página Web
st.set_page_config(page_title="Karakuria AI", page_icon="🤖", layout="centered")
st.title("⚡ Karakuria Core v2.0")
st.caption("Sistema de Inteligência e Infraestrutura Operante (Módulo de Visão Ativo)")

# 2. Conexão com o Cofre e o Motor
load_dotenv()
chave_secreta = os.getenv("GROQ_API_KEY")
if chave_secreta:
    cliente = Groq(api_key=chave_secreta.strip())
else:
    st.error("Erro crítico: Chave de API não encontrada.")
    st.stop()

# 3. Gerenciamento da Memória no Servidor
if "historico" not in st.session_state:
    st.session_state.historico = [
        {"role": "system", "content": "Você é a Karakuria, uma assistente de infraestrutura e dados irônica, direta e altamente inteligente. Você também consegue ler e diagnosticar imagens."}
    ]

# 4. Renderização do Histórico (Desenhando o chat na tela)
for mensagem in st.session_state.historico:
    if mensagem["role"] != "system":
        with st.chat_message(mensagem["role"]):
            # Lógica para renderizar corretamente se houver imagem no histórico
            if isinstance(mensagem["content"], list):
                st.markdown(mensagem["content"][0]["text"])
                st.caption("📎 [Imagem processada nos logs]")
            else:
                st.markdown(mensagem["content"])

# 5. Interface de Input Híbrida (Texto + Upload)
# Colocamos o uploader na barra lateral (sidebar) para ficar mais organizado
with st.sidebar:
    st.header("Módulo de Sensores")
    imagem_anexada = st.file_uploader("Carregar captura de tela/log", type=["png", "jpg", "jpeg"])
    if imagem_anexada:
        st.image(imagem_anexada, caption="Pronto para análise.")

comando = st.chat_input("Fale com a Karakuria ou envie uma imagem...")

if comando:
    # Mostra a mensagem do usuário na tela
    with st.chat_message("user"):
        st.markdown(comando)

   # 6. O Roteamento de Dados (Texto vs. Imagem)
    if imagem_anexada:
        # Extraímos os bytes e convertemos para Base64
        bytes_imagem = imagem_anexada.getvalue()
        imagem_base64 = base64.b64encode(bytes_imagem).decode('utf-8')
        
        # Lemos dinamicamente se é PNG, JPEG, etc. (O pulo do gato!)
        tipo_arquivo = imagem_anexada.type 
        
        # Montamos o pacote com o tipo de arquivo correto
        conteudo_usuario = [
            {"type": "text", "text": comando},
            {
                "type": "image_url",
                "image_url": {"url": f"data:{tipo_arquivo};base64,{imagem_base64}"}
            }
        ]
        
        st.session_state.historico.append({"role": "user", "content": conteudo_usuario})
        motor_selecionado = "llama-3.2-11b-vision-preview" 
        
    else:
        # Modo texto puro e rápido
        st.session_state.historico.append({"role": "user", "content": comando})
        motor_selecionado = "llama-3.1-8b-instant"

    # 7. A Sinapse
    with st.spinner(f"Processando via {motor_selecionado}..."):
        resposta = cliente.chat.completions.create(
            model=motor_selecionado,
            messages=st.session_state.historico
        )
        
        conteudo_resposta = resposta.choices[0].message.content
        
        # Mostra a resposta da IA na tela
        with st.chat_message("assistant"):
            st.markdown(conteudo_resposta)
        
        # Salva a resposta na memória
        st.session_state.historico.append({"role": "assistant", "content": conteudo_resposta})