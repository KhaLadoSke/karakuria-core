import os
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

<<<<<<< HEAD
# 1. Configuração da Página Web
st.set_page_config(page_title="Karakuria AI", page_icon="🤖", layout="centered")
st.title("🕷️ Karakuria Core v2.0")
st.caption("Assistente pessoal")
=======
# 1. Configuração do Ambiente
st.set_page_config(page_title="Karakuria AI", page_icon="👁️", layout="centered")
st.title("⚡ Karakuria Core v2.1 (Modo Visão)")
>>>>>>> 049f83f (Adiciona log de debug para validacao da chave API)

load_dotenv()
chave = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
if not chave:
    st.error("Chave de API não encontrada.")
    st.stop()

cliente = Groq(api_key=chave.strip())

# 2. Estado da Memória
if "historico" not in st.session_state:
    st.session_state.historico = []

# 3. Módulo de Sensores (Upload)
with st.sidebar:
    st.header("Sensor de Imagem")
    imagem_anexada = st.file_uploader("Upload", type=["png", "jpg", "jpeg"])
    if imagem_anexada:
        st.image(imagem_anexada, caption="Imagem carregada")

comando = st.chat_input("Pergunte algo sobre a imagem ou apenas converse...")

# 4. Renderização
for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        # Tratamento de exibição para texto ou listas (imagens)
        if isinstance(msg["content"], list):
            st.markdown(msg["content"][0]["text"])
        else:
            st.markdown(msg["content"])

# 5. Lógica de Roteamento Visual
if comando:
    with st.chat_message("user"):
        st.markdown(comando)
        
    conteudo_envio = None
    motor = "llama-3.1-8b-instant" # Padrão para texto

    if imagem_anexada:
        # Converter para Base64
        bytes_imagem = imagem_anexada.getvalue()
        base64_imagem = base64.b64encode(bytes_imagem).decode('utf-8')
        tipo_mime = imagem_anexada.type
        
        # Estrutura do Pacote Visual (O "Olho" da IA)
        conteudo_envio = [
            {"type": "text", "text": comando},
            {
                "type": "image_url",
                "image_url": {"url": f"data:{tipo_mime};base64,{base64_imagem}"}
            }
        ]
        motor = "llama-3.2-11b-vision-instruct" # Modelo de Visão
    else:
        conteudo_envio = comando

    # Salvar no histórico
    st.session_state.historico.append({"role": "user", "content": conteudo_envio})

    # 6. Execução com Tratamento de Erro (O "SysAdmin Debug")
    try:
        with st.spinner(f"Analisando via {motor}..."):
            resposta = cliente.chat.completions.create(
                model=motor,
                messages=[{"role": "system", "content": "Você é um especialista em infraestrutura."}] + st.session_state.historico
            )
            
            texto_resposta = resposta.choices[0].message.content
            st.session_state.historico.append({"role": "assistant", "content": texto_resposta})
            st.rerun()
            
    except Exception as e:
        st.error(f"Falha na comunicação com o motor: {e}")