import os
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# 1. Configuração do Ambiente
st.set_page_config(page_title="Karakuria AI", page_icon="👁️", layout="centered")
st.title("⚡ Karakuria Core v2.1 (Modo Visão)")

load_dotenv()
chave = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
if not chave:
    st.error("Chave de API não encontrada.")
    st.stop()

cliente = Groq(api_key=chave.strip())

# DEBUG SEGURO (NÃO REVELA A CHAVE)
mascara = chave[:4] + "..." + chave[-4:] if len(chave) > 8 else "INVALIDA"
print(f"DEBUG: Chave carregada na memória: {mascara}")

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
        if isinstance(msg["content"], list):
            st.markdown(msg["content"][0]["text"])
        else:
            st.markdown(msg["content"])

# 5. Lógica de Roteamento Visual
if comando:
    with st.chat_message("user"):
        st.markdown(comando)
        
    conteudo_envio = None
    motor = "llama-3.1-8b-instant" 

    if imagem_anexada:
        bytes_imagem = imagem_anexada.getvalue()
        base64_imagem = base64.b64encode(bytes_imagem).decode('utf-8')
        tipo_mime = imagem_anexada.type
        
        conteudo_envio = [
            {"type": "text", "text": comando},
            {
                "type": "image_url",
                "image_url": {"url": f"data:{tipo_mime};base64,{base64_imagem}"}
            }
        ]
        motor = "meta-llama/llama-4-scout-17b-16e-instruct"
    else:
        conteudo_envio = comando

    st.session_state.historico.append({"role": "user", "content": conteudo_envio})

    # 6. Execução com Tratamento de Erro (O "SysAdmin Debug")
    try:
        with st.spinner(f"Analisando via {motor}..."):
            resposta = cliente.chat.completions.create(
                model=motor,
                messages=[{"role": "system", "content": "Você é a Karakuria, uma especialista em infraestrutura e programação. SEMPRE que for explicar arquiteturas, funcionamento de sistemas, fluxo de pacotes ou lógica de código, você DEVE ilustrar sua explicação desenhando diagramas detalhados usando arte ASCII dentro de blocos de código, além de usar tabelas para comparar dados."}] + st.session_state.historico
            )
            
            texto_resposta = resposta.choices[0].message.content
            st.session_state.historico.append({"role": "assistant", "content": texto_resposta})
            st.rerun()
            
    except Exception as e:
        st.error(f"Falha na comunicação com o motor: {e}")